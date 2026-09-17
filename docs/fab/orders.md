# Order log

One row per order. Fill nothing until Rolf places an order. Copy hashes
from `docs/fab/cad/v1/manifest.json` at the time of upload. Quote numbers
come from the JLC checkout page. Charged numbers come from the receipt.

| Date | Vendor | Files and hashes (manifest) | Quantities | Quoted, by line | Charged, by line | Duty paid | Shipping paid | Lead time | Tracking | Receipt inspection |
|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |  |

Line items to split under Quoted and Charged when an order exists:

- parts (process, material, colour, finish)
- import collection / tariff
- shipping (service name, DDP or not)

Receipt inspection, when a parcel arrives, includes: part count, finish,
damage, closure test, hook-test drop and force, tape fallback if used.
