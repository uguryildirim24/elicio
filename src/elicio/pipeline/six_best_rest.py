"""Evaluate the 'best 6 gestures + rest' subset on every subject, using
the SAME cross-session protocol and forearm-16 channel set as the main
run. The subset of 6 non-rest gestures is chosen from TRAINING data
only (a held-out slice of session 1), so no test-session label
information leaks into which gestures get kept -- a stricter version
of the same idea used in the 2-subject baseline (which had picked the
subset using test-session F1, a shortcut noted as a limitation there).

For each subject:
  1. Split session-1 (train) windows 80/20 with a seeded shuffle over
     all training rows, to avoid picking a subset that only looks
     good on the exact rows used to build the model.
  2. Fit a Gradient-Boosted-Trees model on the 80% slice, score
     per-class F1 on the 20% slice.
  3. Take the 6 highest-F1 non-rest gestures, add rest (17) --> 7
     classes total.
  4. Refit Gradient-Boosted-Trees AND the winning neural network
     (Temporal_CNN) on the FULL session-1 rows restricted to those 7
     classes, evaluate cross-session on session2 and session3
     restricted to the same 7 classes.
"""
from __future__ import annotations

import argparse
import csv
import os
from types import SimpleNamespace

import numpy as np
from sklearn.metrics import accuracy_score, f1_score

from .config import (
    DEFAULT_DATA_DIR,
    DEFAULT_EPOCHS,
    DEFAULT_EVALUATE_RESULTS_CSV,
)
from .models import build_models
from .net_models import build_networks
from .splits import cross_session_split
from .train_and_eval import eval_torch_model, train_torch_model

REST_ID = 17


def pick_best6(features, labels, train_idx, feature_names, seed=0):
    rng = np.random.RandomState(seed)
    idx = train_idx.copy()
    rng.shuffle(idx)
    cut = int(len(idx) * 0.8)
    fit_idx, score_idx = idx[:cut], idx[cut:]

    model = build_models()["Gradient_Boosted_Trees"]
    model.fit(features[fit_idx], labels[fit_idx])
    preds = model.predict(features[score_idx])
    classes = np.unique(labels[score_idx])
    per_class_f1 = f1_score(labels[score_idx], preds, average=None, labels=classes)
    class_f1 = dict(zip(classes, per_class_f1))
    non_rest = [c for c in classes if c != REST_ID]
    ranked = sorted(non_rest, key=lambda c: class_f1.get(c, 0.0), reverse=True)
    best6 = ranked[:6]
    return sorted(best6 + [REST_ID])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=DEFAULT_DATA_DIR)
    ap.add_argument("--subjects", type=int, nargs="+", required=True)
    ap.add_argument("--epochs", type=int, default=DEFAULT_EPOCHS)
    ap.add_argument("--out", default=DEFAULT_EVALUATE_RESULTS_CSV)
    args = ap.parse_args(argv)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    fieldnames = ["subject", "model", "test_session", "gestures_kept",
                  "accuracy", "macro_f1", "n_train", "n_test"]
    with open(args.out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for subject in args.subjects:
            npz_path = os.path.join(args.data_dir, f"subject_{subject:02d}.npz")
            if not os.path.exists(npz_path):
                print(f"[subject {subject}] SKIP: not found", flush=True)
                continue
            data = np.load(npz_path)
            windows = data["windows"]
            features = data["features"]
            labels = data["labels"]
            sessions = data["sessions"]
            subjects = data["subjects"]
            feature_names = list(data["feature_names"])
            subject_id = f"participant{subject:02d}"

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
            best7 = pick_best6(features, labels, train_idx, feature_names)
            print(f"[{subject_id}] kept gestures {best7}", flush=True)

            keep_mask_train = np.isin(labels[train_idx], best7)
            tr = train_idx[keep_mask_train]
            gesture_str = ",".join(str(g) for g in best7)

            # remap labels to 0..6 for the classifiers
            label_map = {g: i for i, g in enumerate(best7)}
            ytr = np.array([label_map[y] for y in labels[tr]], dtype=np.int64)

            # Gradient-Boosted-Trees on features
            gbt = build_models()["Gradient_Boosted_Trees"]
            gbt.fit(features[tr], ytr)
            for sess_name, idx in test_idx.items():
                keep_mask_test = np.isin(labels[idx], best7)
                te = idx[keep_mask_test]
                yte = np.array([label_map[y] for y in labels[te]], dtype=np.int64)
                preds = gbt.predict(features[te])
                acc = accuracy_score(yte, preds)
                f1 = f1_score(yte, preds, average="macro")
                writer.writerow({
                    "subject": subject_id, "model": "Gradient_Boosted_Trees",
                    "test_session": sess_name, "gestures_kept": gesture_str,
                    "accuracy": acc, "macro_f1": f1, "n_train": len(tr), "n_test": len(te),
                })
                print(f"[{subject_id}] GBT vs {sess_name}: acc={acc:.3f} f1={f1:.3f}", flush=True)

            # Temporal_CNN on raw windows (best-performing network from the main run)
            Xtr_win = windows[tr].transpose(0, 2, 1)
            ch_mean = Xtr_win.mean(axis=(0, 2), keepdims=True)
            ch_std = Xtr_win.std(axis=(0, 2), keepdims=True) + 1e-6
            Xtr_win_n = (Xtr_win - ch_mean) / ch_std
            net = build_networks(Xtr_win.shape[1], len(best7))["Temporal_CNN"]
            train_torch_model(net, Xtr_win_n, ytr, epochs=args.epochs)
            for sess_name, idx in test_idx.items():
                keep_mask_test = np.isin(labels[idx], best7)
                te = idx[keep_mask_test]
                yte = np.array([label_map[y] for y in labels[te]], dtype=np.int64)
                Xte_win = windows[te].transpose(0, 2, 1)
                Xte_win = (Xte_win - ch_mean) / ch_std
                acc, f1, ms = eval_torch_model(net, Xte_win, yte)
                writer.writerow({
                    "subject": subject_id, "model": "Temporal_CNN",
                    "test_session": sess_name, "gestures_kept": gesture_str,
                    "accuracy": acc, "macro_f1": f1, "n_train": len(tr), "n_test": len(te),
                })
                print(f"[{subject_id}] Temporal_CNN vs {sess_name}: acc={acc:.3f} f1={f1:.3f}",
                      flush=True)
            f.flush()


if __name__ == "__main__":
    main()
