"""Data-prep job: stream GRABMyo (16 forearm channels) directly from
PhysioNet's public S3-backed WFDB store, window it, compute the 5
standard sEMG features, and save one .npz per subject to ./results/.

No bulk download of the 9.4 GB archive is needed -- wfdb.rdrecord with
pn_dir= streams one record at a time from PhysioNet's open S3 bucket.
Runs a bounded thread pool per subject to parallelize the network
fetches (I/O bound), then processes and writes to disk before moving
to the next subject, so peak memory stays near one subject's data.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import os
import time

import numpy as np

from .config import (
    GRABMYO_PN_DIR_ROOT,
    GRABMYO_SESSIONS,
    STEP_MS,
    WINDOW_MS,
)
from .features import compute_features, window_recordings
from .load import (
    GRABMYO_FOREARM_CHANNELS,
    GRABMYO_GESTURE_NAMES,
    GRABMYO_N_GESTURES,
    GRABMYO_N_TRIALS,
    Recording,
    wfdb,
)

MAX_RETRIES = 4
POOL_SIZE = 24


def fetch_one(session: int, subject: int, gesture_id: int, trial: int):
    if wfdb is None:
        raise RuntimeError(
            "preparing GRABMyo data requires the research dependency: "
            "pip install 'elicio[research]'"
        )
    stem = f"session{session}_participant{subject}_gesture{gesture_id}_trial{trial}"
    pn_dir = (
        f"{GRABMYO_PN_DIR_ROOT}/Session{session}/"
        f"session{session}_participant{subject}"
    )
    last_err = None
    for attempt in range(MAX_RETRIES):
        try:
            rec = wfdb.rdrecord(stem, pn_dir=pn_dir)
            signal = np.asarray(rec.p_signal, dtype=np.float32)
            channel_names = list(rec.sig_name)
            idx = [channel_names.index(c) for c in GRABMYO_FOREARM_CHANNELS]
            signal = signal[:, idx]
            gesture_name = GRABMYO_GESTURE_NAMES[gesture_id - 1]
            labels = np.full(signal.shape[0], gesture_id, dtype=np.int32)
            return Recording(
                signal=signal,
                labels=labels,
                sample_rate=float(rec.fs),
                channel_names=list(GRABMYO_FOREARM_CHANNELS),
                subject=f"participant{subject}",
                session=f"session{session}",
                gesture_name=gesture_name,
                trial=trial,
            )
        except Exception as e:  # noqa: BLE001 -- retry on any transient fetch error
            last_err = e
            time.sleep(0.5 * (attempt + 1))
    print(f"[fetch] FAILED session{session} participant{subject} "
          f"gesture{gesture_id} trial{trial}: {last_err}", flush=True)
    return None


def load_subject(subject: int, sessions=GRABMYO_SESSIONS):
    jobs = [
        (s, subject, g, t)
        for s in sessions
        for g in range(1, GRABMYO_N_GESTURES + 1)
        for t in range(1, GRABMYO_N_TRIALS + 1)
    ]
    recordings = []
    with cf.ThreadPoolExecutor(max_workers=POOL_SIZE) as ex:
        futs = [ex.submit(fetch_one, *j) for j in jobs]
        for fut in cf.as_completed(futs):
            rec = fut.result()
            if rec is not None:
                recordings.append(rec)
    return recordings


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--subjects", type=int, nargs="+", required=True)
    ap.add_argument("--out-dir", default="results")
    args = ap.parse_args(argv)

    os.makedirs(args.out_dir, exist_ok=True)

    for subject in args.subjects:
        t0 = time.time()
        recordings = load_subject(subject)
        n_expected = len(GRABMYO_SESSIONS) * GRABMYO_N_GESTURES * GRABMYO_N_TRIALS
        print(f"[subject {subject}] fetched {len(recordings)}/{n_expected} recordings "
              f"in {time.time()-t0:.1f}s", flush=True)
        if not recordings:
            print(f"[subject {subject}] SKIP: no recordings loaded", flush=True)
            continue

        window_set = window_recordings(
            recordings,
            window_ms=WINDOW_MS,
            step_ms=STEP_MS,
        )
        window_set = compute_features(window_set)

        out_path = os.path.join(args.out_dir, f"subject_{subject:02d}.npz")
        np.savez_compressed(
            out_path,
            windows=window_set.windows,
            features=window_set.features,
            feature_names=np.array(window_set.feature_names),
            labels=window_set.labels,
            subjects=np.array(window_set.subjects),
            sessions=np.array(window_set.sessions),
            channel_names=np.array(window_set.channel_names),
            sample_rate=window_set.sample_rate,
        )
        print(f"[subject {subject}] saved {out_path}: "
              f"{window_set.windows.shape[0]} windows, "
              f"windows shape {window_set.windows.shape}, "
              f"features shape {window_set.features.shape} "
              f"(total {time.time()-t0:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
