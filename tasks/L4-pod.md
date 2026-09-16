# L4 — Stage B pod electronics, envelope, and one-off PCB fabrication

Report path: docs/fab/L4-pod.md
Repo: /home/user/projects/elicio

Rules:
- You are one research lane of a fabrication study. Read docs/fab/brief.md first, then the "Requirements", "Staged build plan", "Stage A circuit design" and "Stream protocol and software bridge" sections of docs/EARPIECE_DESIGN.md.
- Write your report as Markdown to the report path above. Do not edit any other file. Do not create git commits.
- Cite a URL for every non-obvious claim (datasheets, product pages with price and date, repos). Mark anything you could not verify as UNVERIFIED.
- Prefer primary sources and 2024-2026 material. Be concrete: part numbers, package sizes in mm, currents in mA, prices, stock status.
- Do not sign up anywhere, request a quote, upload a file, or contact anyone. Read public pages only.
- Aim for 1500-3000 words, structured with headers and tables. End with a section "Open questions for the synthesis" and a section "Top 10 sources".
- When the file is written, run these three commands in the shell, in order:
  herdr pane report-metadata "$HERDR_PANE_ID" --source lane --token lane=L4 --token done=1
  herdr notification show "L4 done" --body "lane l4" --sound done
  herdr agent prompt elicio "DONE L4 docs/fab/L4-pod.md -" || herdr agent prompt elicio "DONE L4 docs/fab/L4-pod.md -"
- Then reply with a single final line containing exactly: DONE docs/fab/L4-pod.md
- If you cannot finish, still write what you have to the report path, mark the gaps, and run the same three commands. A lane that stops silently is the one failure nothing catches.

Questions to answer:
1. The smallest sensible Stage B electronics for one or two EMG channels: BLE microcontroller modules (Seeed XIAO nRF52840 Sense, Raytac MDBT50Q, other nRF52840 or nRF5340 modules, ESP32-C3 and C6 minis), biopotential front ends (TI ADS1291, ADS1292, ADS1299-4, AD8232, MAX30003, a discrete INA333 or AD8226 chain), what sample rate and resolution EMG needs (the design record runs 860 SPS on a 16-bit ADS1115 at Stage A), power (LiPo 40 to 100 mAh with dimensions, LIR2032 and CR2032, a charging IC, protection), and the run time per charge. Give footprints in mm and prices, and stock in 2026.
2. Reference designs to steal from: OpenEarable 2.0, OpenBCI Ganglion and Cyton (too big, say why), cEEGrid amplifiers, the EarSwitch and EarRumble hardware if published, PhysioLab or similar open EMG boards, any 2024-2026 open ear-EEG or ear-EMG hardware on GitHub. Links, licenses, board sizes.
3. The envelope: give a concrete estimate of the pod's outer dimensions (L x W x H in mm) with board, battery and contacts, as a single rigid board and as a two-board or flex design, and compare it with a BTE hearing aid body, a bone-conduction headset pod, and an over-ear hook. Say how the pod attaches (ear hook, clip, adhesive) and where the weight sits.
4. One-off PCB fabrication and assembly in China: JLCPCB PCBA (does its parts library stock the ADS1292, nRF52840 modules, the charger, the passives; minimum board count; cost for 2 or 5 assembled boards; lead time), PCBWay assembly, and flex PCB options for an electrode carrier. What files (Gerber, BOM, CPL) and what design tool; note that KiCad 9 is scriptable from Python.
5. Safety in a wireless pod: single-fault current limits and the on-board electrode protection network, why BLE plus a sealed battery satisfies the "never charge while worn" rule, and the IEC 60601-1 patient-leakage numbers as a design guideline, not a compliance claim.
6. Firmware and stream: how the pod would emit the one-ASCII-sample-per-line stream the design record specifies, over BLE (Nordic UART Service) into `elicio scope` on the Mac; latency, throughput at 500 to 1000 samples per second, and the simplest firmware path (Arduino core, Zephyr, CircuitPython, or the vendor SDK).
