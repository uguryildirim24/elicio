# L2 — manufacturing services for a one-off skin-contact shell

Report path: docs/fab/L2-vendors.md
Repo: /Users/rolfie/projects/elicio

Rules:
- You are one research lane of a fabrication study. Read docs/fab/brief.md first, then the "Fabrication without a 3D printer" and "Requirements" sections of docs/EARPIECE_DESIGN.md.
- Write your report as Markdown to the report path above. Do not edit any other file. Do not create git commits.
- Cite a URL for every non-obvious claim (prices: the page you read them on, with the date). Mark anything you could not verify as UNVERIFIED.
- Prefer primary sources and 2024-2026 material. Be concrete: service names, material names, prices, minimums, lead times, dates.
- Do not sign up anywhere, request a quote, upload a file, or contact anyone. Read public pricing and material pages only. Where a price needs an upload to see, say so and give the nearest public number.
- Aim for 1500-3000 words, structured with headers and tables. End with a section "Open questions for the synthesis" and a section "Top 10 sources".
- When the file is written, run these three commands in the shell, in order:
  herdr pane report-metadata "$HERDR_PANE_ID" --source lane --token lane=L2 --token done=1
  herdr notification show "L2 done" --body "lane l2" --sound done
  herdr agent prompt elicio "DONE L2 docs/fab/L2-vendors.md -" || herdr agent prompt elicio "DONE L2 docs/fab/L2-vendors.md -"
- Then reply with a single final line containing exactly: DONE docs/fab/L2-vendors.md
- If you cannot finish, still write what you have to the report path, mark the gaps, and run the same three commands. A lane that stops silently is the one failure nothing catches.

The part: a behind-the-ear shell roughly 35 x 20 x 12 mm, hollow, with a lid, a pocket for a small PCB and a battery, and three bosses or holes for skin-contact electrodes. One unit, then a few more as the design iterates. It touches skin for hours. The customer is one person in Massachusetts, USA, uploading a file.

Questions to answer:
1. Chinese online services that take a one-off file: JLCPCB 3D printing, PCBWay (3D printing, vacuum casting, CNC, silicone), WeNext, Unionfab, Xometry China, and any others with real traction in 2025-2026. For each: processes and materials suitable for a skin-contact shell (SLA resins including flexible and any skin-safe or biocompatible grade, MJF and SLS nylon, TPU, cast silicone or urethane), any biocompatibility or skin-safe claim and the standard behind it (ISO 10993 or none), minimum order, a concrete price for one part of this size, lead time, shipping options and cost to Massachusetts.
2. The 2026 US import situation for a small China-origin parcel: is the de minimis exemption still gone for China, what tariff and broker fee a $20 to $100 part actually attracts, and how services such as JLCPCB or PCBWay handle it (DDP, prepaid duty, or surprise bill). Cite current government or carrier sources.
3. Small-batch silicone or TPU shops on Alibaba or 1688 for custom earbud or ear-hook parts: typical MOQ, sample cost, mould or tooling cost for a soft silicone overmould, and whether a one-off is realistic versus a 3D-printed flexible part.
4. Custom in-ear-monitor and hearing-aid shell makers in Shenzhen or Dongguan that make shells from an impression or an STL: would they make an empty shell with a lid and holes, at what price, and how would Rolf send geometry.
5. Comparison outside China, to keep the choice honest: US and EU bureaus (Shapeways, Protolabs, Xometry US, Craftcloud, Sculpteo, Fictiv), a hearing-aid lab, and Boston-area makerspaces or university shops that print skin-safe resin or TPU. Cost and time difference against the Chinese options.
6. Conductive and metal-insert options at these services: does anyone print conductive TPU (Palmiga PI-ETPU 95-250) or conductive silicone, insert stainless or gold-plated contacts, or overmould around a PCB; what to send (STL, STEP, drawing) and how to specify.
7. A concrete recommended first order: vendor, process, material, files, estimated all-in cost including shipping and duty, lead time, and what Rolf has to do himself (account, payment). Do it twice: once for a fit-check shell with no electronics, once for the Stage B shell with electrode bosses and a lid.
