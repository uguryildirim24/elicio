# sEMG research pipeline

This package prepares public GRABMyo forearm recordings, trains gesture decoders and evaluates across different recording sessions. It does not decode auricular EMG or connect research predictions to the action gate.

No result CSVs, model checkpoints or measured accuracy reports are included here. Earlier imported research summaries are not supported by tracked result artifacts. See [research provenance](../../../docs/RESEARCH_PROVENANCE.md).

## Run from the repository root

Python >=3.11 is required. Research dependencies include WFDB, scikit-learn and PyTorch. These commands download data and run substantial training workloads. Check storage and compute capacity first.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[research]'
.venv/bin/elicio-emg prepare --subjects 1 2 3 --out-dir results
.venv/bin/elicio-emg train --data-dir results --subjects 1 2 3 \
    --epochs 20 --out results/train_results.csv
.venv/bin/elicio-emg evaluate --data-dir results --subjects 1 2 3 \
    --epochs 20 --out results/six_best_rest.csv
```

No `PYTHONPATH` setting is needed after installation. Use `elicio-emg prepare --help`, `train --help` or `evaluate --help` for options.

`load.py` fetches PhysioNet/WFDB records from `grabmyo/1.1.0`. Preparation writes `subject_NN.npz` files. Training and evaluation read those files and write CSVs. `results/` is ignored. The dataset is not bundled or relicensed by Elicio. Synthetic test fixtures are the only committed sample data.

## Layout

| Module | Purpose |
| --- | --- |
| `config.py` | Shared window, feature, channel and training defaults |
| `load.py` | `Recording` contract and public WFDB loader |
| `features.py` | Windowing and MAV, WL, ZC, SSC and RMS features |
| `splits.py` | Cross-session split and leakage guard |
| `models.py` | LDA, linear SVM and gradient-boosted tree baselines |
| `net_models.py` | Temporal CNN, GRU and Transformer models |
| `prepare_subjects.py` | Per-subject window and feature files |
| `train_and_eval.py` | Full-gesture model comparison |
| `six_best_rest.py` | Reduced gesture-set evaluation |
| `cli.py` | `prepare`, `train` and `evaluate` commands |

## New recordings

The preparation CLI accepts public GRABMyo records only. A device-data preparation path must supply the `Recording` fields defined in `load.py` and write the same NPZ fields as `prepare_subjects.py`: `windows`, `features`, `feature_names`, `labels`, `subjects`, `sessions`, `channel_names`, `sample_rate`. Receiver output is not an already trained decoder or a complete labeled training dataset.

Keep raw recordings and participant metadata in ignored `recordings/`. Use distinct session identifiers for different acquisition sessions. All evaluation must pass through `cross_session_split` and `assert_no_session_leakage`.

Training is not fully seeded, so exact repeated scores are not guaranteed. Software feature and split checks do not establish biological performance. Research download and training commands were not rerun during publication cleanup.
