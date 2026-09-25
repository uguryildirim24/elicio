#!/usr/bin/env python3
"""Build the v4 shell and compare folded courtyard volumes to the actual solids.

The source of the envelopes is board-v4-design.md §10.2, not pin centres.
No files outside --out are written. The hinge-only shell is NOT a closed product.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path

import bte_fit_shell as cad

ROOT = cad.REPO_ROOT
TABLE = ROOT / "docs/fab/board-v4-design.md"
PARAMS = cad.SCRIPT_DIR / "params/shell_v4.toml"


def folded_rows() -> list[tuple[str, str, tuple[float, ...]]]:
    text = TABLE.read_text().split("#### Courtyards on the island")[1].split("#### Rings, strip roots")[0]
    rows = []
    for line in text.splitlines():
        fields = [f.strip() for f in line.strip().strip("|").split("|")]
        if len(fields) != 12 or fields[1] not in ("top", "bottom"):
            continue
        if "cut off" in fields[5]:
            rows.append((fields[0], "exterior (tab cut)", ()))
            continue
        def interval(value: str) -> tuple[float, float]:
            found = re.fullmatch(r"(-?\d+(?:\.\d+)?)-(-?\d+(?:\.\d+)?)", value)
            if found is None:
                raise ValueError(f"{fields[0]}: invalid courtyard {value}")
            return float(found[1]), float(found[2])
        rows.append((fields[0], fields[1], (*interval(fields[2]), *interval(fields[3]), *interval(fields[5]))))
    if len(rows) < 55:
        raise ValueError(f"§10.2 courtyard table incomplete ({len(rows)})")
    return rows


def measure(body, lid, path, params):
    maker = cad.path_solid_for(path, params)
    checks = []
    for ref, side, bounds in folded_rows():
        if not bounds:
            checks.append({"item": ref, "kind": side, "margin_mm": None, "passed": True})
            continue
        u0, u1, s0, s1, y0, y1 = bounds
        # Pads-only J4 has zero height. A 0.01 mm slab is the probe, not an
        # assumed mounted part; its height remains UNVERIFIED in the report.
        prism = maker(u0, u1, s0, s1, y0, max(y1, y0 + 0.01))
        body_hit = cad._overlap_volume(body, prism)
        lid_hit = cad._overlap_volume(lid, prism)
        distance = min(body.distance_to(prism), lid.distance_to(prism))
        # U1 deliberately seats against the second post. Other parts must
        # have strictly disjoint interiors; proximity is the nearest solid
        # distance, not just clearance from a nominal rectangular cavity.
        intentional = ref == "U1" and lid_hit > 0
        passed = body_hit < 0.001 and (lid_hit < 0.001 or intentional)
        checks.append({"item": ref, "kind": f"{side} courtyard", "margin_mm": round(distance, 4) if passed else -round(max(body_hit, lid_hit), 4),
                       "body_overlap_mm3": round(body_hit, 4), "lid_overlap_mm3": round(lid_hit, 4),
                       "post_on_U1": intentional, "passed": passed})
    def probe(name, bounds, part=body):
        u0,u1,s0,s1,y0,y1 = bounds
        block = maker(u0,u1,s0,s1,y0,y1)
        hit = cad._overlap_volume(part, block)
        checks.append({"item": name, "kind": "reserved air", "margin_mm": round(part.distance_to(block),4) if hit < 0.001 else -round(hit,4),
                       "overlap_mm3": round(hit,4), "passed": hit < 0.001})
    probe("cell + 0.5 foam", (1.8,11.9,1.5,14.5,1.501,7.099))
    probe("SIG1 root", (4.65,7.15,14.4,16,1.51,4.49))
    probe("SIG2 root", (9.15,11.65,14.4,16,1.51,4.49))
    probe("REF root", (7.25,9.75,38.2,39.25,1.51,1.81))
    probe("P4/P5 flap slot", (16.02,16.48,14.91,15.69,1.51,4.49))
    probe("P4/P5 plate", (16.19,16.49,1.75,14.85,1.695,6.895))
    # The plate's lower continuation past the rib is separate from its
    # s1.75–14.85 straight run and its high joint root. Probe its entire
    # s14.85–19.30 wall volume, not only the first 0.8 mm of the slot.
    probe("P4/P5 folded flap", (16.19,16.50,14.85,19.30,1.695,3.905))
    probe("P4/P5 joint root", (15.09,16.30,16.30,19.30,3.80,5.12))
    probe("J3 stub", (15.75,16.20,19.9,22.4,5.01,5.12))
    probe("island", (2.25,15.75,16,37.6,5.01,5.12))
    probe("P1 post landing", (4.95,6.85,22.05,23.95,5.12,7.10), lid)
    probe("P2 post landing", (8.45,10.35,31.15,33.05,6.12,7.10), lid)
    # Posts should occupy the volumes above; these two are *positive* tests.
    for row in checks[-2:]:
        row["kind"] = "post solid (intentional)"
        row["passed"] = row["overlap_mm3"] > 2.5
        row["margin_mm"] = round(row["overlap_mm3"],4)
    for ring,u,s in (("P1",5.9,22.0),("P2",10.4,33.1),("P3",8.5,43.0)):
        for y in (0.05,0.75,1.65):
            free=not cad._inside_uys(body,path,u,s,y)
            checks.append({"item":f"{ring} ring axis y{y:g}","kind":"open floor hole / seat",
                           "margin_mm":0 if free else -1,"passed":free})
    # Built-solid occupancy at each key, screw axis and post (not a
    # coordinate-only assertion). The keys are 1.0 in s, 2.8 high.
    for site_name,site in (("P4",4.35),("P5",12.10)):
        for side,ss in (("low",site-3.3),("high",site+3.3)):
            inside = cad._inside_uys(body,path,14.5,ss,2.5)
            checks.append({"item":f"{site_name} {side} key", "kind":"solid occupancy",
                           "margin_mm":0.5 if inside else -0.5, "passed":inside})
        for u in (13.10,16.55,17.95,18.05):
            free = not cad._inside_uys(body,path,u,site,4.295)
            checks.append({"item":f"{site_name} screw axis u{u:g}", "kind":"hole face air",
                           "margin_mm":0 if free else -1, "passed":free})
    for label,u,s,bottom in (("P1",5.90,23.00,5.12),("P2",9.40,32.10,6.12)):
        near_bottom=cad._inside_uys(lid,path,u,s,bottom+0.05)
        below=not cad._inside_uys(lid,path,u,s,bottom-0.05)
        checks.append({"item":f"{label} post datum", "kind":"lid post y landing",
                       "margin_mm":0.05 if near_bottom and below else -0.05,
                       "passed":near_bottom and below})
    # J2 vs the near edge of the P5 standoff: no well protrudes into this
    # area. The gap is measured from the courtyard box, not J2's centre.
    j2 = next(row for row in checks if row["item"] == "J2")
    j2_gap = 13.19 - 8.38
    checks.append({"item":"J2 to P5 key", "kind":"courtyard-to-open-standoff-end",
                   "margin_mm":round(j2_gap,4), "passed":j2_gap>=0.3 and j2["passed"]})
    return checks


def ramp_lip(path, u0, u1, start):
    """Inclined insertion face; vertical underside provides the catch."""
    mid = start + 1.75
    center = cad._vec(path, u0, mid, 4.85)
    radial = (cad._vec(path, u0 + .01, mid, 4.85) - center).normalized()
    tangent = (cad._vec(path, u0, mid + .01, 4.85)
               - cad._vec(path, u0, mid - .01, 4.85)).normalized()
    points = [center + tangent*(s-mid) + cad.Vector(0,y-4.85,0)
              for s,y in ((start,4.85),(44.70,4.85),(44.70,5.85),(start+1.40,5.85))]
    face = cad.Face(cad.Wire.make_polygon(points + points[:1]))
    return cad.Solid.extrude(face, radial*(u1-u0))


def closure_variant(body, lid, path, params, name):
    """Independent closure prototypes on the unchanged v4 solid."""
    if name == "hinge":
        return body, lid, {"type": "hinge only"}
    if name == "snap":
        maker = cad.path_solid_for(path, params)
        # Pocket in the solid tail, leaving a 1 mm floor. Two side catches
        # bridge to the uncut tail and leave an open central key corridor.
        body = body.cut(maker(9.50, 14.50, 38.05, 44.60, 2.50, 7.10))
        for u0, u1 in ((9.50, 10.90), (13.10, 14.50)):
            body = body.fuse(maker(u0, u1, 43.50, 47.50 if u0 < 11 else 45.00, 4.85, 5.85))
            body = body.fuse(ramp_lip(path, u0, u1, 41.30))
        # Two independent 1 mm-thick arms flank the central key corridor.
        # They join at a foot whose two wings hook under the side ledges.
        for u0, u1 in ((9.80, 10.90), (13.10, 14.20)):
            lid = lid.fuse(maker(u0, u1, 39.70, 40.70, 3.15, 7.18))
        lid = lid.fuse(maker(9.80, 14.20, 40.60, 42.00, 3.15, 4.15))
        # Open the centre for the entire shaft sweep, not just its tip.
        lid = lid.cut(maker(11.05, 12.95, 39.80, 44.60, 7.09, 8.20))
        return body, lid, {"type": "PA12 twin-side snap", "beam_u_mm": [[9.80, 10.90], [13.10, 14.20]],
                           "beam_s_mm": [39.70, 40.70], "beam_y_mm": [3.15, 7.18],
                           "foot_s_mm": [40.60, 42.00], "lip_s_mm": [41.30, 44.70],
                           "lip_y_mm": [4.85, 5.85], "engagement_mm": 0.70,
                           "closing_travel_worst_mm": 1.32,
                           "max_strain_percent": round(100 * 3 * 1.0 * 1.32 / (2 * 3.95**2), 2)}
    diameter, head, height, boss_od = (1.6, 3.14, 1.64, 3.6)
    u, s = 14.10, 11.80
    xyz = cad._vec(path, u, s, 0)
    # The shank is 4 mm measured from the head seat. A 0.10 mm face
    # clearance separates the floor pillar from the hanging lid boss.
    # This is a deliberate diagnostic prototype: the head's radial wall
    # is thinner than the published MJF minimum, so it is not for printing.
    seat = height + 0.12
    tip = seat + 4.0
    body_boss_top = 3.95
    lid_boss_bottom = 4.05
    body_boss_od = boss_od  # narrow gap beside the folded charging plate
    body = body.fuse(cad._y_cylinder(xyz.X, 1.48, xyz.Z, body_boss_od / 2, body_boss_top - 1.48))
    lid = lid.fuse(cad._y_cylinder(xyz.X, lid_boss_bottom, xyz.Z, boss_od / 2,
                                    7.20 - lid_boss_bottom))
    body = body.cut(cad._y_cylinder(xyz.X, -0.05, xyz.Z, head / 2 + 0.10, seat + 0.05))
    body = body.cut(cad._y_cylinder(xyz.X, seat - 0.01, xyz.Z, diameter / 2 + 0.10,
                                     body_boss_top - seat + 0.02))
    lid = lid.cut(cad._y_cylinder(xyz.X, lid_boss_bottom - 0.01, xyz.Z,
                                   (diameter - 0.2) / 2, tip - lid_boss_bottom + 0.02))
    return body, lid, {"type": "ISO 4762 medial-access socket screw", "thread": name,
                       "u": u, "s": s, "head_max_mm": head, "head_height_max_mm": height,
                       "key_mm": 1.5, "head_seat_y_mm": seat, "nominal_screw_length_mm": 4,
                       "tip_y_mm": tip, "lid_engagement_mm": round(tip - lid_boss_bottom, 3),
                       "body_boss_od_mm": body_boss_od, "lid_boss_od_mm": boss_od,
                       "head_well_radial_wall_mm": round((body_boss_od - head - .20) / 2, 3),
                       "lid_boss_radial_wall_mm": round((boss_od - diameter) / 2, 3),
                       "head_well_floor_radial_mm": round(min(u - (head / 2 + .1),
                                                              18 - u - (head / 2 + .1)), 3)}


def hex_sweep(path, af, s0, s1, y0, y1):
    """Exact flat-to-flat hex shaft, swept along s and extruded along y.

    The path tangent is evaluated at the tool station; the tail curvature
    over this 3 mm stroke is negligible only for the tool, never the shell.
    """
    center = cad._vec(path, 12.0, (s0 + s1) / 2, y0)
    radial = (cad._vec(path, 13.0, (s0 + s1) / 2, y0) - center).normalized()
    tangent = (cad._vec(path, 12.0, (s0 + s1) / 2 + .01, y0)
               - cad._vec(path, 12.0, (s0 + s1) / 2 - .01, y0)).normalized()
    radius = af / math.sqrt(3)
    # Convex hull of the two endpoint hexagons, in cyclic perimeter order.
    vertices = [(-af/2, -radius/2), (0, -radius), (af/2, -radius/2),
                (af/2, radius/2), (0, radius), (-af/2, radius/2)]
    # Union of endpoint polygons swept in s: their hull has these 6 vertices.
    outline = [(-af/2, s0-radius/2), (0, s0-radius), (af/2, s0-radius/2),
               (af/2, s1+radius/2), (0, s1+radius), (-af/2, s1+radius/2)]
    mid = (s0+s1)/2
    points = [center + radial*u + tangent*(s-mid) for u,s in outline]
    wire = cad.Wire.make_polygon(points + points[:1])
    return cad.Solid.extrude(cad.Face(wire), cad.Vector(0, y1-y0, 0))


def snap_checks(body, lid, path, params):
    maker = cad.path_solid_for(path, params)
    checks = []
    # Entire shaft, not a point in the mouth: from outside at y8.2 to
    # y3.0, and then along s up to first contact with the foot at s42.
    # Clearance envelope adds 0.2 mm per flat to the actual 1.5 mm key.
    foot = maker(9.80, 14.20, 40.60, 42.00, 3.15, 4.15)
    for label, af, s0, s1, contact in (
        ("key approach", 1.9, 43.38, 43.38, False),
        ("key release sweep", 1.9, 43.10, 43.38, False),
        ("key contact and stroke", 1.5, 41.47, 43.10, True),
    ):
        tool = hex_sweep(path, af, s0, s1, 3.35, 8.20)
        b_hit = cad._overlap_volume(body, tool)
        # Remove ONLY the defined foot contact face/volume from this test;
        # the rest of the built lid must remain entirely outside the shaft.
        l_hit = cad._overlap_volume(lid.cut(foot) if contact else lid, tool)
        foot_hit = cad._overlap_volume(foot, tool) if contact else 0
        checks.append({"item": label, "kind": "swept hex key, 0.2 per-flat approach clearance",
                       "body_overlap_mm3": round(b_hit, 4), "lid_overlap_mm3": round(l_hit, 4),
                       "intended_foot_contact_mm3": round(foot_hit, 4),
                       "passed": b_hit < .001 and l_hit < .001 and (not contact or foot_hit > .001)})
    # Opposing ±0.3 shifts of foot and ledge are the worst horizontal stack.
    # Vertical stack: .70 gap to ledge, .65 above floor; each loses .60.
    for offset in (-.3, .3):
        lip_start = 41.30 + offset
        # Rebuild the catch at its offset, leaving the end anchor in place.
        tol_body = body
        for u0,u1 in ((9.5,10.9),(13.1,14.5)):
            tol_body = tol_body.cut(maker(u0,u1,41.28,44.71,4.84,5.86))
            tol_body = tol_body.fuse(maker(u0,u1,43.50,47.50 if u0 < 11 else 45.00,4.85,5.85))
            tol_body = tol_body.fuse(ramp_lip(path,u0,u1,lip_start))
        foot_offset = -offset
        engagement = 42.00 + foot_offset - lip_start
        # Move the entire foot, not a point, into the closing pose at the
        # underside of the ledge. Its tip must clear even at opposing errors.
        travel = engagement + .02
        posed_foot = maker(9.80,14.20,40.60+foot_offset-travel,
                           42.00+foot_offset-travel,4.85,5.85)
        collision = cad._overlap_volume(tol_body, posed_foot)
        checks.append({"item": f"catch offset {offset:+.1f}", "kind": "rebuilt opposing tolerance stack",
                       "ledge_offset_mm": offset, "foot_offset_mm": foot_offset,
                       "engagement_mm": round(engagement, 3),
                       "closing_travel_mm": round(travel, 3),
                       "closing_overlap_mm3": round(collision, 4),
                       "vertical_ledge_gap_worst_mm": .10,
                       "vertical_floor_gap_worst_mm": .05,
                       "passed": engagement > 0 and travel <= 1.321 and collision < .001})
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "docs/fab/cad/v4")
    parser.add_argument("--closure", choices=("hinge", "m16", "snap"), default="hinge")
    args = parser.parse_args()
    params, unused = cad.build_reference_params(variant="full", preload=1.5,
        overrides=cad.load_params_file(PARAMS), crease_bow_from_m=False)
    body, lid, path, notes = cad.build_body_and_lid(params)
    body, lid, closure = closure_variant(body, lid, path, params, args.closure)
    body, lid = cad._one_solid(body, 'closure body'), cad._one_solid(lid, 'closure lid')
    checks = measure(body,lid,path,params)
    checks.append({"item":"seated lid vs body", "kind":"solid overlap",
                   "margin_mm":round(cad._overlap_volume(body,lid),4),
                   "passed":cad._overlap_volume(body,lid)<0.001})
    if args.closure == 'snap':
        checks.extend(snap_checks(body, lid, path, params))
    elif args.closure == 'm16':
        for item, solid, y, occupied in (
            ('screw head air', body, 0.8, False),
            ('screw shank air', body, 3.0, False),
            ('screw lid pilot air', lid, 5.0, False),
            ('screw lid boss wall', lid, 5.0, True),
        ):
            u = 15.65 if item == 'screw lid boss wall' else 14.10
            present = cad._inside_uys(solid,path,u,11.80,y)
            checks.append({'item':item,'kind':'closure solid probe','margin_mm':0,
                           'passed':present == occupied})
    assembled, lid_s = cad.assemble_shell(body,lid,params,notes)
    args.out.mkdir(parents=True,exist_ok=True)
    files = {}
    for name,solid in (("body_full_p15",assembled),("lid",lid_s)):
        files.update(cad.export_part(solid,args.out/name,name,uuid_ns="elicio:cad:v4"))
        if not cad.stl_watertight(args.out/f"{name}.stl"):
            raise cad.CheckFail(f"{name}: STL not watertight")
    manifest = {"schema": 1,"stage":"shell-v4", "provisional":True,
                "closure":closure,
                "source_table":"docs/fab/board-v4-design.md §10.2",
                "parameters":{k:v for k,v in params.items() if not k.startswith('_') and cad._jsonable(v)},
                "params_sha256":cad.sha256_file(PARAMS), "checks":checks,
                "files":files,"notes":notes,"body_lid_overlap_mm3":round(cad._overlap_volume(body,lid),4),
                "hash_rule":"SHA256 raw bytes; STEP pinned timestamp; STL/3MF CAD meshing 0.02 mm, 5 degrees"}
    (args.out/"manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    failing = [c['item'] for c in checks if not c['passed']]
    print(json.dumps({"out":str(args.out),"checks":len(checks),"failed":failing},indent=2))
    return 1 if failing else 0

if __name__ == '__main__':
    raise SystemExit(main())
