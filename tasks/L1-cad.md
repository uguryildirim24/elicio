# L1 — CAD tool, ear geometry, starting models, design rules

Report path: docs/fab/L1-cad.md
Repo: /home/user/projects/elicio

Rules:
- You are one research lane of a fabrication study. Read docs/fab/brief.md first, then the "Fabrication without a 3D printer" and "Requirements" sections of docs/EARPIECE_DESIGN.md.
- Write your report as Markdown to the report path above. Do not edit any other file. Do not create git commits.
- Cite a URL for every non-obvious claim (papers: DOI or journal link; software: repo or product page; prices: the page you read). Mark anything you could not verify as UNVERIFIED.
- Prefer primary sources and 2024-2026 material. Be concrete: names, versions, prices, dimensions, licenses, dates.
- Do not sign up anywhere, request a quote, upload a file, or contact anyone. Read public pages only.
- Aim for 1500-3000 words, structured with headers and tables. End with a section "Open questions for the synthesis" and a section "Top 10 sources".
- When the file is written, run these three commands in the shell, in order:
  herdr pane report-metadata "$HERDR_PANE_ID" --source lane --token lane=L1 --token done=1
  herdr notification show "L1 done" --body "lane l1" --sound done
  herdr agent prompt elicio "DONE L1 docs/fab/L1-cad.md -" || herdr agent prompt elicio "DONE L1 docs/fab/L1-cad.md -"
- Then reply with a single final line containing exactly: DONE docs/fab/L1-cad.md
- If you cannot finish, still write what you have to the report path, mark the gaps, and run the same three commands. A lane that stops silently is the one failure nothing catches.

Questions to answer:
1. Which CAD tool should an AI coding agent use to design a behind-the-ear shell from a text spec plus measurements, iterating over several rounds? Compare Blender (Python API, sculpting, no parametric history), Fusion 360 personal license, Onshape free, FreeCAD 1.x, OpenSCAD, CadQuery and build123d (Python, headless), Plasticity, Shapr3D. For each: parametric or direct, scriptable headless from Python on macOS, exports STEP/STL/3MF, cost, and fit for a part that is organic on the skin side and precise on the inside (PCB pocket, battery pocket, snap lid, electrode bosses). Recommend a primary tool and a fallback, and say why, given that the designer is an agent working from text and the reviewer is Rolf looking at renders.
2. How does Rolf get his own ear and mastoid geometry? Cover iPhone scanning apps (TrueDepth and LiDAR: Polycam, Scaniverse, Heges, 3D Scanner App, Kiri Engine, others), their accuracy for millimetre features behind the ear, the hair problem, and export formats. Cover photogrammetry (Meshroom, RealityScan). Cover DIY silicone ear-impression kits (which, price) and scanning the impression. Explain how custom in-ear-monitor and hearing-aid makers do it (impression, scan, shell-modelling software such as 3Shape or Cyfex Secret Ear Designer, then SLA), and whether any free or cheap shell-from-scan tool exists.
3. Starting models: open-source or free behind-the-ear hearing-aid shells, ear hooks, bone-conduction headset shells, open earable platforms (OpenEarable 2.0, OpenBCI ear-EEG, cEEGrid holders, others) on GitHub, Printables, Thingiverse, GrabCAD. Give links, licenses, formats. Give the standard dimensions of a BTE hearing-aid body and hook. Say whether a generic BTE shell can be designed and fit-checked without a personal scan.
4. Design rules for the likely processes: minimum wall thickness, clearances, hole and boss tolerances, and lid or snap-fit guidance for SLA resin, MJF and SLS nylon, TPU (FDM and SLS), and cast silicone. Which file formats manufacturers want (STL, STEP, 3MF, plus a drawing PDF), and what units and resolution.
5. Propose the first concrete deliverable: which files, in which tool, could be produced in one session from a text spec and a few measurements, and exactly which measurements Rolf should take with a ruler or caliper if no scan exists yet. Include a fit-check shell (no electronics) as the first printed part.
