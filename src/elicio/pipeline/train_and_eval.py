"""Train and evaluate the network family (plus a same-channel baseline
rerun) for one or more subjects, using the same cross-session protocol
as the earlier LDA/SVM/HistGBT baseline: train on session 1, test on
session 2 and session 3 separately.

Reads one subject_NN.npz per subject (produced by prepare_subjects.py):
  windows        float32 [n_windows, 410, 16]  raw signal, forearm-16
  features       float32 [n_windows, 80]        5 features x 16 channels
  feature_names  [80]  e.g. "F3_MAV"
  labels         int32 [n_windows]  gesture id, 1..17
  sessions       [n_windows]  "session1" / "session2" / "session3"
  channel_names  [16]  "F1".."F16"

For each subject, tries three channel sets (16 forearm channels, the
best 8, the best 3 by train-only F-score) and, per set, three neural
networks (Temporal_CNN, GRU, Transformer) plus the three baseline
classifiers (LDA, Linear_SVM, Gradient_Boosted_Trees) re-run on that
subject so every row in the final table used the identical
train/test windows.

Writes one row per (subject, model, channel_set, test_session) to a
CSV in ./results/.
"""
from __future__ import annotations

import argparse
import csv
import os
import time
from types import SimpleNamespace

import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score, f1_score

from .config import (
    DEFAULT_DATA_DIR,
    DEFAULT_EPOCHS,
    DEFAULT_TRAIN_RESULTS_CSV,
)
from .models import build_models, fit_and_score, select_channels_by_fscore
from .net_models import build_networks
from .splits import cross_session_split

N_GESTURE_CLASSES = 17  # gesture ids 1..17 (17 = rest)


def session_mask(sessions: np.ndarray, name: str) -> np.ndarray:
    return sessions == name


def channel_configs(features, labels, feature_names, channel_names, train_idx):
    """Return {config_name: (chosen_channel_names, feature_col_idx)}."""
    configs = {}
    configs["forearm_16"] = (list(channel_names), list(range(len(feature_names))))
    for n_ch, key in [(8, "best_8"), (3, "best_3")]:
        chosen, cols = select_channels_by_fscore(
            features[train_idx], labels[train_idx], feature_names, channel_names,
            n_channels=n_ch, largest=True,
        )
        configs[key] = (chosen, cols)
    return configs


def train_torch_model(model, X_train, y_train, epochs=15, batch_size=256, lr=1e-3):
    device = torch.device("cpu")
    model.to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    Xtr = torch.tensor(X_train, dtype=torch.float32)
    ytr = torch.tensor(y_train, dtype=torch.long)
    n = Xtr.shape[0]
    model.train()
    for _ in range(epochs):
        perm = torch.randperm(n)
        for i in range(0, n, batch_size):
            idx = perm[i:i + batch_size]
            xb, yb = Xtr[idx], ytr[idx]
            opt.zero_grad()
            out = model(xb)
            loss = loss_fn(out, yb)
            loss.backward()
            opt.step()
    return model


def eval_torch_model(model, X_test, y_test, n_timing=200):
    model.eval()
    Xte = torch.tensor(X_test, dtype=torch.float32)
    with torch.no_grad():
        logits = model(Xte)
    preds = logits.argmax(dim=1).numpy()
    acc = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds, average="macro")

    # per-window inference time: single-example forward passes, batch=1,
    # matching how a real-time decoder would call the model.
    n_timing = min(n_timing, X_test.shape[0])
    timing_idx = np.random.choice(X_test.shape[0], size=n_timing, replace=False)
    t0 = time.time()
    with torch.no_grad():
        for i in timing_idx:
            _ = model(torch.tensor(X_test[i:i + 1], dtype=torch.float32))
    elapsed = time.time() - t0
    ms_per_window = (elapsed / n_timing) * 1000.0
    return acc, f1, ms_per_window


def eval_sklearn_model(model, X_train, y_train, X_test, y_test, n_timing=200):
    metrics = fit_and_score(model, X_train, y_train, X_test, y_test)
    n_timing = min(n_timing, X_test.shape[0])
    timing_idx = np.random.choice(X_test.shape[0], size=n_timing, replace=False)
    t0 = time.time()
    for i in timing_idx:
        model.predict(X_test[i:i + 1])
    elapsed = time.time() - t0
    ms_per_window = (elapsed / n_timing) * 1000.0
    return metrics["accuracy"], metrics["macro_f1"], ms_per_window


def process_subject(npz_path: str, writer: csv.DictWriter, epochs: int):
    data = np.load(npz_path)
    windows = data["windows"]          # [n, 410, 16]
    features = data["features"]        # [n, 80]
    feature_names = list(data["feature_names"])
    labels = data["labels"]            # gesture id 1..17
    sessions = data["sessions"]
    subjects = data["subjects"]
    channel_names = list(data["channel_names"])
    subject_id = os.path.basename(npz_path).replace(".npz", "").replace("subject_", "participant")

    split_metadata = SimpleNamespace(
        sessions=sessions.tolist(),
        subjects=subjects.tolist(),
    )
    train_idx, session2_idx = cross_session_split(
        split_metadata,
        train_sessions=["session1"],
        test_sessions=["session2"],
    )
    _, session3_idx = cross_session_split(
        split_metadata,
        train_sessions=["session1"],
        test_sessions=["session3"],
    )
    test_idx = {
        "session2": session2_idx,
        "session3": session3_idx,
    }
    if len(train_idx) == 0 or any(len(v) == 0 for v in test_idx.values()):
        print(f"[{subject_id}] SKIP: missing a session", flush=True)
        return

    configs = channel_configs(features, labels, feature_names, channel_names, train_idx)

    for config_name, (chosen_channels, feat_cols) in configs.items():
        chan_idx = [channel_names.index(c) for c in chosen_channels]
        n_ch = len(chan_idx)

        Xtr_win = windows[train_idx][:, :, chan_idx].transpose(0, 2, 1)  # (n, n_ch, T)
        ytr = (labels[train_idx] - 1).astype(np.int64)
        Xtr_feat = features[train_idx][:, feat_cols]

        # Per-channel z-score, fit on train only: raw sEMG channels can
        # differ by an order of magnitude in scale, which starves a GRU
        # or transformer of usable gradient signal even though a
        # BatchNorm'd CNN tolerates it. mean/std are computed once on
        # the training window set and reused for every test session.
        ch_mean = Xtr_win.mean(axis=(0, 2), keepdims=True)
        ch_std = Xtr_win.std(axis=(0, 2), keepdims=True) + 1e-6
        Xtr_win_n = (Xtr_win - ch_mean) / ch_std

        nets = build_networks(n_ch, N_GESTURE_CLASSES)
        for net_name, net in nets.items():
            t0 = time.time()
            train_torch_model(net, Xtr_win_n, ytr, epochs=epochs)
            train_s = time.time() - t0
            for sess_name, idx in test_idx.items():
                Xte_win = windows[idx][:, :, chan_idx].transpose(0, 2, 1)
                Xte_win = (Xte_win - ch_mean) / ch_std
                yte = (labels[idx] - 1).astype(np.int64)
                acc, f1, ms = eval_torch_model(net, Xte_win, yte)
                writer.writerow({
                    "subject": subject_id, "model": net_name, "channel_set": config_name,
                    "n_channels": n_ch, "test_session": sess_name,
                    "accuracy": acc, "macro_f1": f1, "n_train": len(train_idx),
                    "n_test": len(idx), "inference_ms_per_window": ms,
                    "train_time_s": train_s,
                })
                print(f"[{subject_id}] {net_name} {config_name} vs {sess_name}: "
                      f"acc={acc:.3f} f1={f1:.3f} inf_ms={ms:.3f}", flush=True)

        baselines = build_models()
        for model_name, model in baselines.items():
            t0 = time.time()
            for sess_name, idx in test_idx.items():
                Xte_feat = features[idx][:, feat_cols]
                yte = (labels[idx] - 1).astype(np.int64)
                acc, f1, ms = eval_sklearn_model(model, Xtr_feat, ytr, Xte_feat, yte)
                writer.writerow({
                    "subject": subject_id, "model": model_name, "channel_set": config_name,
                    "n_channels": n_ch, "test_session": sess_name,
                    "accuracy": acc, "macro_f1": f1, "n_train": len(train_idx),
                    "n_test": len(idx), "inference_ms_per_window": ms,
                    "train_time_s": time.time() - t0,
                })
                print(f"[{subject_id}] {model_name} {config_name} vs {sess_name}: "
                      f"acc={acc:.3f} f1={f1:.3f} inf_ms={ms:.3f}", flush=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--data-dir",
        default=DEFAULT_DATA_DIR,
        help="dir with subject_NN.npz files",
    )
    ap.add_argument("--subjects", type=int, nargs="+", required=True)
    ap.add_argument("--epochs", type=int, default=DEFAULT_EPOCHS)
    ap.add_argument("--out", default=DEFAULT_TRAIN_RESULTS_CSV)
    args = ap.parse_args(argv)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    fieldnames = ["subject", "model", "channel_set", "n_channels", "test_session",
                  "accuracy", "macro_f1", "n_train", "n_test",
                  "inference_ms_per_window", "train_time_s"]
    with open(args.out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for subject in args.subjects:
            npz_path = os.path.join(args.data_dir, f"subject_{subject:02d}.npz")
            if not os.path.exists(npz_path):
                print(f"[subject {subject}] SKIP: {npz_path} not found", flush=True)
                continue
            t0 = time.time()
            process_subject(npz_path, writer, args.epochs)
            f.flush()
            print(f"[subject {subject}] done in {time.time()-t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
