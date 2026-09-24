#!/usr/bin/env python3
"""One-line summary of a kicad-cli DRC json, then every non-thermal error, the starved pads and
each open connection with the gap between the two reported positions (design note §9.5).

  .venv/bin/python hardware/board/v4_drcsum.py DRC.json
"""
import collections, json, math, sys

d = json.load(open(sys.argv[1]))
errs = collections.Counter(v["type"] for v in d["violations"] if v["severity"] == "error")
warns = collections.Counter(v["type"] for v in d["violations"] if v["severity"] == "warning")
un = collections.Counter(u["items"][0]["description"].split("[")[1].split("]")[0] for u in d["unconnected_items"])
print(f"errors {sum(errs.values())} {dict(errs)} | warnings {dict(warns)} | unconnected {len(d['unconnected_items'])} "
      f"{dict(un)} | parity {len(d.get('schematic_parity', []))}")
for v in d["violations"]:
    if v["severity"] == "error" and v["type"] != "starved_thermal":
        print("  ERR", v["type"], v["description"][:80], [(i["description"][:45], i["pos"]["x"], i["pos"]["y"]) for i in v["items"]])
st = [v["items"][1]["description"].replace(" [GND] of ", ".").replace("Pad ", "") for v in d["violations"] if v["type"] == "starved_thermal"]
if st:
    print("  starved", st)
for u in d["unconnected_items"]:
    a, b = u["items"][0], u["items"][1]
    net = a["description"].split("[")[1].split("]")[0]
    gap = math.hypot(a["pos"]["x"] - b["pos"]["x"], a["pos"]["y"] - b["pos"]["y"])
    print(f"  OPEN {net}: {a['description']} @({a['pos']['x']:.2f},{a['pos']['y']:.2f}) <-> "
          f"{b['description']} @({b['pos']['x']:.2f},{b['pos']['y']:.2f}): {gap:.2f} mm")
