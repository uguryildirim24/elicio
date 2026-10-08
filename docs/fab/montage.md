# Proposed acquisition criteria and receiver mapping

These are unvalidated engineering targets, not measured results or an approved on-body protocol. The board is unfinished and unordered. No gel, dry-contact or live acquisition record is included. The shelved breadboard circuit, shopping path and gauge-first procedure have been removed.

All amplitude and detection targets below are proposals. Earlier agent reports do not provide a verified biological basis for them. Qualified electrical review and bench validation must precede any on-body study. No duration of powered wear is authorized by this document.

## Reference coordinates

The generator uses `u` across the body and `s` along its curved path from the hook root, in millimetres. Its reference contact centres are:

| Contact | u | s |
| --- | ---: | ---: |
| CONTACT_1 | 5.9 | 22.0 |
| CONTACT_2 | 10.4 | 33.1 |
| CONTACT_REF | 8.5 | 43.0 |

These are design defaults, not Rolf's anatomy measurements or a validated montage. Physical contact positions, material, pressure and cross-talk need separate review. A geometry check cannot establish independent auricular and jaw-muscle sources.

## Evidence needed

A future reviewed study needs raw signal, acquisition time, calibration, contact configuration, cue annotations and distinct session identifiers. Keep recordings and participant metadata in ignored `recordings/`. Keep completed anatomy parameters in ignored `measurements/`. Do not publish identifiable photos or personal self-reports as design evidence.

Preserve raw records without replacing them with filtered traces. Any change to a target needs a dated rationale before evaluation, not a threshold selected after seeing the test result. Transport fixtures test byte handling only.

## Proposed detection targets

| ID | Proposed target |
| --- | --- |
| 3.1 | Resting noise at most 5 microvolts RMS in the 20 to 490 Hz band over 60 seconds. |
| 3.2 | Median of 10 deliberate auricular contractions at least 45 microvolts peak-to-peak and at least 3 times resting peak-to-peak amplitude. |
| 3.3 | Median of 10 jaw clenches at least 150 microvolts peak-to-peak, at least 10 times rest and at least 3 times the contraction median. |
| 3.4 | No acquisition dropout. DC shift at most 50 mV input-referred relative to rest. Input and common-mode headroom remain open. |
| 3.5 | On each of 3 separate sessions after removal and replacement, at least 9 of 10 contractions detected without changing the threshold. |
| 3.6 | At most 1 false contraction event during 5 minutes of eating. |
| 3.7 | No false contraction event during 5 minutes of talking. |
| 3.8 | No false contraction event during 5 minutes of walking. |
| 3.9 | No confirmation pair or action above `RiskLevel.NONE` during 3 yawns. |
| 3.10 | At most 1 `RiskLevel.NONE` trigger per set of 5 wide smiles or 5 hard blinks, and no action above NONE. |

These small counts cannot estimate long-term false-positive rates or safety. Confidence floors and the three-second confirmation window are software policy settings in `src/elicio/harness/policy.py`, not calibrated biological probabilities. The event tuple cannot prove that a confirmation came from an independent muscle group.

## 8. Protocol v2 mapping

This section retains the criterion IDs consumed by the existing receiver checks. Frame-v2 acquisition is intended to run at 2000 samples per second. Raw ADS1292 codes are preserved. The nominal voltage scale in [frame-v2.md](frame-v2.md) is metadata, not measured calibration.

The proposed offline amplitude analysis uses a fourth-order Butterworth band-pass from 20 to 490 Hz with zero-phase `sosfiltfilt`. Rest RMS uses the full 60-second record after exclusions. Contraction and clench peak-to-peak windows start at the cue and last 2 seconds. The receiver does not implement this amplitude analysis or automatic gesture scoring.

Acquisition dropout is a constant-code stretch spanning more than 200 sample intervals (100 ms at 2000 SPS). `receive-check` checks each channel against `acq_index` continuity. Invalid samples and the first 200 conversions after each RESTART are excluded. Missing acquisition conversions and transport loss remain separate records. A missing `frame_seq` is not by itself an acquisition dropout.

HELLO messages and STREAM messages with no samples do not produce waveform samples. VBUS refusal, restart settling and overruns must remain visible in session records. Input headroom and common-mode headroom need bench data. DC shifts must be assessed on raw codes, not a high-passed trace.

| ID | Proposed target | Mapping |
| --- | --- | --- |
| 3.1 | Rest noise at most 5 microvolts RMS | revised: input-referred digital band-pass analysis, not scored by `receive-check`. |
| 3.2 | Contraction at least 45 microvolts peak-to-peak and 3 times rest | revised: same proposed values with a 2-second window, not scored by `receive-check`. |
| 3.3 | Clench at least 150 microvolts peak-to-peak, 10 times rest and 3 times contraction | revised: same proposed values with a 2-second window, not scored by `receive-check`. |
| 3.4 | No dropout and at most 50 mV DC shift | revised: receiver reports constant-code dropout only. DC shift and headroom need separate analysis. |
| 3.5 | Repeated-session detection with unchanged threshold | same criterion: externally scored session field. |
| 3.6 | Eating false-event count | same criterion: externally scored session field. |
| 3.7 | Talking false-event count | same criterion: externally scored session field. |
| 3.8 | Walking false-event count | same criterion: externally scored session field. |
| 3.9 | Yawning confirmation and action count | same criterion: externally scored session field. |
| 3.10 | Smile and blink event/action count | same criterion: externally scored session field. |

`receive` initializes criterion fields 3.5 to 3.10 as `not_scored` in `sidecar.json`. `receive-check` accepts `not_scored` and `pass`. Any other value for one of these IDs causes exit 1. A constant-code dropout alone causes exit 3. Missing or malformed session files cause exit 2. Otherwise it exits 0. An `"ok": true` report with unscored criteria does not mean that gesture or wear targets passed.

The historical `S2 continues (Q75)` message means that a bench dropout is reported rather than classified as a scored gesture failure. It is not approval for powered wear. See [open hardware gates](open-questions.md) and [receiver output](receiver-v2.md).
