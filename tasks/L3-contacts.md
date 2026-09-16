# L3 — auricular anatomy and skin contacts for a manufactured shell

Report path: docs/fab/L3-contacts.md
Repo: /Users/rolfie/projects/elicio

Rules:
- You are one research lane of a fabrication study. Read docs/fab/brief.md first, then the "Decision record", "Evidence", "Requirements" and "Fabrication without a 3D printer" sections of docs/EARPIECE_DESIGN.md.
- Write your report as Markdown to the report path above. Do not edit any other file. Do not create git commits.
- Cite a URL for every non-obvious claim (papers: DOI or journal link; parts: the product page with price and date). Mark anything you could not verify as UNVERIFIED.
- Prefer primary sources and 2024-2026 material. Be concrete: dimensions in mm, amplitudes in microvolts, prices, materials, part numbers.
- Do not sign up anywhere, request a quote, or contact anyone. Read public pages only.
- Aim for 1500-3000 words, structured with headers and tables. End with a section "Open questions for the synthesis" and a section "Top 10 sources".
- When the file is written, run these three commands in the shell, in order:
  herdr pane report-metadata "$HERDR_PANE_ID" --source lane --token lane=L3 --token done=1
  herdr notification show "L3 done" --body "lane l3" --sound done
  herdr agent prompt elicio "DONE L3 docs/fab/L3-contacts.md -" || herdr agent prompt elicio "DONE L3 docs/fab/L3-contacts.md -"
- Then reply with a single final line containing exactly: DONE docs/fab/L3-contacts.md
- If you cannot finish, still write what you have to the report path, mark the gaps, and run the same three commands. A lane that stops silently is the one failure nothing catches.

Questions to answer:
1. Anatomy for placement: the posterior auricular and superior auricular muscles (and the anterior, if relevant) relative to the pinna, the mastoid and the hairline; their size; where a surface EMG contact over each of them sits on the skin; what the muscle-fibre direction is, so two signal contacts can be placed along the fibres. Give the reference-electrode site. Note cross-talk from temporalis, masseter, occipitalis and neck muscles.
2. Prior recordings of auricular EMG: papers and products that recorded the auricular muscles at the skin (postauricular muscle response studies, earable EMG work such as ear-worn gesture systems, EarFieldSensing, EarBuddy and similar, hearing-aid steering by ear movement, any 2024-2026 work). For each: electrode type, positions, inter-electrode distance, signal amplitude range in microvolts, sample rate, filters, and what classification they achieved.
3. cEEGrid and its relatives: the around-the-ear flexprint electrode array (TMSi and the Oldenburg group). Geometry, material (Ag/AgCl on flex), adhesive, price, source, and whether it is still sold in 2026. Then: could a custom flex PCB from JLCPCB or PCBWay with ENIG gold pads reproduce the idea for a few dollars, and what are the trade-offs against a rigid shell with metal contacts.
4. Dry-contact options that fix into a manufactured shell and are nickel-free: 316L stainless discs, domes and studs; gold-plated snap studs; titanium; sintered Ag/AgCl pellets; conductive silicone (carbon-loaded); conductive TPU (Palmiga PI-ETPU 95-250, and who prints it); conductive fabric; PCB ENIG pads; spring-loaded pogo pins. For each: skin safety and the nickel question, typical contact impedance, comfort, attachment method (press-fit, adhesive, overmould, screw), wire termination, a concrete part or source with price.
5. How commercial ear-worn biopotential devices do their contacts: NextSense Smartbuds, IDUN Guardian, Naox, Neurable, OpenEarable ExG, Cognionics or Zeto dry electrodes, Emotiv Insight's polymer sensors. Contact material, size, how they hold pressure, and anything published about impedance or re-donning stability.
6. Recommendation: number, size and spacing of contacts for this shell (the design record cites roughly 16 mm contacts working where 5 mm failed for printed TPU; say what applies to metal), how the shell should hold them against the skin with repeatable pressure (spring, foam, clip force), and how to verify a stud is nickel-free (EN 1811 nickel release test, supplier certification).
