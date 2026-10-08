# Research provenance and evidence limits

`src/elicio/pipeline/` was migrated from Rolf's Claude Science research project. Private workspace identifiers and local storage paths are not public provenance and have been removed.

The migrated package includes the loader, feature extraction, configuration, split guard, classical models, neural models, subject preparation and evaluation entry points. Engineering changes included package-relative imports, argument forwarding, output-directory handling, optional-dependency messages and routing evaluation through the cross-session split API. Model architectures and feature formulas were preserved during migration.

## Public input data

`load.py` requests WFDB records from the PhysioNet database path `grabmyo/1.1.0`. It selects forearm channels. `elicio-emg prepare` downloads the selected records and writes per-subject window/feature files under ignored `results/`. See the [pipeline README](../src/elicio/pipeline/README.md) for exact commands.

Public forearm recordings are not auricular recordings. They do not validate the proposed earpiece, personal calibration or on-body action control. Dataset terms are separate from the project MIT license.

## What is available here

- Research implementations and feature/split checks.
- Synthetic signal and binary transport fixtures.
- Policy, audit and harmless local-action demonstrations.
- Hardware design snapshots and CAD manifests with nominal geometry checks.

Earlier private reports contained accuracy and inference-timing summaries. The underlying result CSVs, checkpoints and reports are not tracked here. Those numbers have been removed from public claims rather than treated as independently reproducible evidence.

Training uses unseeded model initialization and batch shuffling. Exact repeatability is not promised. Research training and data preparation were not rerun for publication cleanup. Generate new results with the documented pipeline before making quantitative decoding claims.

No Elicio paper or preprint is included in this tree.
