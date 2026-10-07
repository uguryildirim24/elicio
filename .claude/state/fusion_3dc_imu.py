"""EMG vs EMG+IMU fusion at reduced channel counts, on the 3DC Armband dataset.

PROTOCOL CAVEAT: the 3DC train/test split is WITHIN-SESSION (5 min pause, armbands
never removed). This cannot measure cross-session robustness. Results here are an
upper bound on real-world performance.
"""
from __future__ import annotations

import glob
import os
import sys

import numpy as np
from scipy import signal
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

ROOT = "/tmp/3dc/Source_code_plus_dataset/Dataset"
FS_EMG = 1000.0
WIN = 250          # 250 ms @ 1000 sps (paper 4.2)
STEP = 25          # paper's size_non_overlap for the 3DC
HP_CUT = 20.0      # paper: 20 Hz 4th-order Butterworth high-pass
ZC_SSC_THR = 0.1   # paper's extract_features.py default, raw ADC units
N_EMG_CH = 10
N_GESTURES = 11
N_CYCLES = 4

GESTURES = ["Neutral", "Radial Deviation", "Wrist Flexion", "Ulnar Deviation",
            "Wrist Extension", "Supination", "Pronation", "Power Grip",
            "Open Hand", "Chuck Grip", "Pinch Grip"]

SOS = signal.butter(N=4, Wn=HP_CUT / (0.5 * FS_EMG), btype="highpass", output="sos")


def emg_features(win: np.ndarray) -> np.ndarray:
    """win: (nwin, WIN, nch) -> (nwin, nch*5). MAV, WL, ZC, SSC, RMS."""
    mav = np.abs(win).mean(axis=1)
    wl = np.abs(np.diff(win, axis=1)).sum(axis=1)
    rms = np.sqrt((win ** 2).mean(axis=1))
    a, b = win[:, :-1, :], win[:, 1:, :]
    zc = ((a * b < 0) & (np.abs(a - b) >= ZC_SSC_THR)).sum(axis=1)
    c, p, n = win[:, 1:-1, :], win[:, :-2, :], win[:, 2:, :]
    ssc = (((c - p) * (c - n)) >= ZC_SSC_THR).sum(axis=1)
    return np.concatenate([mav, wl, zc, ssc, rms], axis=1).astype(np.float32)


def imu_features(quat: np.ndarray, starts: np.ndarray, ratio: float) -> np.ndarray:
    """Per EMG window, summarise the orientation quaternion covering it."""
    out = np.empty((len(starts), 12), dtype=np.float32)
    n = len(quat)
    for i, s in enumerate(starts):
        lo = min(int(s / ratio), n - 1)
        hi = min(max(int((s + WIN) / ratio), lo + 1), n)
        seg = quat[lo:hi]
        out[i, 0:4] = seg.mean(axis=0)
        out[i, 4:8] = seg.std(axis=0)
        out[i, 8:12] = seg[-1] - seg[0]
    return out


def load_trial(emg_path: str, imu_path: str):
    emg = np.loadtxt(emg_path, delimiter=",", dtype=np.float64)
    if emg.ndim != 2 or emg.shape[1] != N_EMG_CH or len(emg) < WIN:
        return None
    raw = [ln.strip().strip("()") for ln in open(imu_path) if ln.strip()]
    quat = np.array([[float(v) for v in ln.split(",")] for ln in raw], dtype=np.float64)
    if len(quat) < 2:
        return None
    # drop the leading all-zero placeholder sample
    if not quat[0].any():
        quat = quat[1:]
    if len(quat) < 2:
        return None

    filt = signal.sosfilt(SOS, emg, axis=0)
    nwin = (len(filt) - WIN) // STEP + 1
    starts = np.arange(nwin) * STEP
    win = np.lib.stride_tricks.sliding_window_view(filt, WIN, axis=0)[::STEP]
    win = np.transpose(win, (0, 2, 1))          # (nwin, WIN, nch)
    ratio = len(filt) / len(quat)
    return emg_features(win), imu_features(quat, starts, ratio)


def load_split(pdir: str, split: str):
    Xe, Xi, y = [], [], []
    for cyc in range(N_CYCLES):
        for g in range(N_GESTURES):
            e = f"{pdir}/{split}/3dc/EMG/3dc_EMG_gesture_{cyc}_{g}.txt"
            i = f"{pdir}/{split}/3dc/IMU/3dc_IMU_gesture_{cyc}_{g}.txt"
            if not (os.path.exists(e) and os.path.exists(i)):
                continue
            r = load_trial(e, i)
            if r is None:
                continue
            fe, fi = r
            Xe.append(fe)
            Xi.append(fi)
            y.append(np.full(len(fe), g, dtype=np.int32))
    if not Xe:
        return None
    return np.vstack(Xe), np.vstack(Xi), np.concatenate(y)


def emg_cols(nch: int) -> np.ndarray:
    """Evenly spaced electrodes around the band, and their 5 feature blocks."""
    picks = np.linspace(0, N_EMG_CH, nch, endpoint=False).astype(int)
    return np.concatenate([picks + b * N_EMG_CH for b in range(5)])


def score(Xtr, ytr, Xte, yte) -> float:
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd[sd == 0] = 1.0
    clf = LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto")
    clf.fit((Xtr - mu) / sd, ytr)
    return float(clf.score((Xte - mu) / sd, yte))


def main() -> int:
    pdirs = sorted(glob.glob(f"{ROOT}/Participant*"),
                   key=lambda p: int(p.rsplit("Participant", 1)[1]))
    gesture_sets = {
        "all 11": list(range(11)),
        "3-class (Neutral/Flex/Ext)": [0, 2, 4],
        "4-class (+Pronation)": [0, 2, 4, 6],
        "2-class (Flex vs Ext only)": [2, 4],
    }
    channel_counts = [10, 6, 4, 3, 2]
    # Absolute orientation drifts across the 5 min pause; cols 4:12 (std + within-window
    # delta) are drift-invariant, so they give the fusion idea its fairest shot.
    imu_variants = {"IMU abs+delta": slice(0, 12), "IMU delta-only": slice(4, 12)}
    results: dict[tuple[str, str, int], list[float]] = {}

    for k, pdir in enumerate(pdirs, 1):
        tr = load_split(pdir, "train")
        te = load_split(pdir, "test")
        if tr is None or te is None:
            print(f"  SKIP {os.path.basename(pdir)}", file=sys.stderr)
            continue
        Etr, Itr, ytr = tr
        Ete, Ite, yte = te
        for gname, gids in gesture_sets.items():
            mtr = np.isin(ytr, gids)
            mte = np.isin(yte, gids)
            for nch in channel_counts:
                cols = emg_cols(nch)
                e_tr, e_te = Etr[mtr][:, cols], Ete[mte][:, cols]
                results.setdefault((gname, "EMG", nch), []).append(
                    score(e_tr, ytr[mtr], e_te, yte[mte]))
                for iname, isl in imu_variants.items():
                    f_tr = np.hstack([e_tr, Itr[mtr][:, isl]])
                    f_te = np.hstack([e_te, Ite[mte][:, isl]])
                    results.setdefault((gname, f"EMG+{iname}", nch), []).append(
                        score(f_tr, ytr[mtr], f_te, yte[mte]))
            for iname, isl in imu_variants.items():
                results.setdefault((gname, f"{iname} only", 0), []).append(
                    score(Itr[mtr][:, isl], ytr[mtr], Ite[mte][:, isl], yte[mte]))
        print(f"  done {os.path.basename(pdir)} ({k}/{len(pdirs)})", file=sys.stderr)

    print()
    print("3DC Armband, LDA, 250 ms windows, WITHIN-SESSION split (5 min pause, band not removed)")
    print(f"n = {len(pdirs)} participants; cells are mean accuracy % +/- std across participants")
    for gname, gids in gesture_sets.items():
        print()
        print(f"### {gname}   chance = {100.0/len(gids):.1f}%")
        print(f"{'channels':>9} | {'EMG only':>13} | {'+IMU abs+delta':>20} | "
              f"{'+IMU delta-only':>20}")
        print(f"{'-'*9}-+-{'-'*13}-+-{'-'*20}-+-{'-'*20}")
        for nch in channel_counts:
            a = np.array(results[(gname, "EMG", nch)]) * 100
            row = f"{nch:>9} | {a.mean():>6.1f} +/-{a.std():>4.1f} |"
            for iname in imu_variants:
                b = np.array(results[(gname, f"EMG+{iname}", nch)]) * 100
                row += f" {b.mean():>6.1f} +/-{b.std():>4.1f} ({b.mean()-a.mean():>+5.1f}) |"
            print(row)
        row = f"{'IMU alone':>9} | {'':>13} |"
        for iname in imu_variants:
            c = np.array(results[(gname, f"{iname} only", 0)]) * 100
            row += f" {c.mean():>6.1f} +/-{c.std():>4.1f} {'':>8}|"
        print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
