#!/usr/bin/env python3
"""Rename the GND net on named pads (text only) so v4_route_pf.py routes them as small nets of
their own; --back renames every GND_* net to GND again (design note §9.1, §9.5).

  .venv/bin/python hardware/board/v4_gnd_split.py IN OUT GND_A:U2.10,U2.13 GND_B:R12.2,R13.2 ...
  .venv/bin/python hardware/board/v4_gnd_split.py --back IN OUT
"""
import re
import sys

if sys.argv[1] == "--back":
    t = open(sys.argv[2]).read()
    n = len(re.findall(r'\(net "GND_[A-Z0-9]+"\)', t))
    open(sys.argv[3], "w").write(re.sub(r'\(net "GND_[A-Z0-9]+"\)', '(net "GND")', t))
    print("renamed back", n)
    sys.exit()
src, out = sys.argv[1], sys.argv[2]
groups = {}
for arg in sys.argv[3:]:
    name, pads = arg.split(":", 1)
    for p in pads.split(","):
        groups[p] = name
t = open(src).read()
done = {}
parts = t.split("\n\t(footprint ")
for i, chunk in enumerate(parts[1:], 1):
    ref = re.search(r'\(property "Reference" "([^"]+)"', chunk).group(1)

    def sub(m):
        pad = m.group(0)
        key = f"{ref}.{m.group(1)}"
        if key in groups and '(net "GND")' in pad:
            done[key] = groups[key]
            return pad.replace('(net "GND")', f'(net "{groups[key]}")')
        return pad

    parts[i] = re.sub(r'\n\t\t\(pad "([^"]*)"[\s\S]*?\n\t\t\)', sub, chunk)
open(out, "w").write("\n\t(footprint ".join(parts))
print("renamed", len(done), "missing", sorted(set(groups) - set(done)))
for name in sorted(set(groups.values())):
    print(" ", name, sorted(k for k, v in done.items() if v == name))
