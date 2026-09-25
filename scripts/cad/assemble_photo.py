#!/usr/bin/env python3
"""Assemble the committed v4-snap earpiece in Blender; see scripts/cad/README.md.

Run with Python 3.11+; this file re-executes itself under Blender's Python.
No downloads or hand-positioned device parts. Units throughout are millimetres.
"""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import re
import subprocess
import struct
import sys
import zlib

ROOT = Path(__file__).resolve().parents[2]
SHELL = ROOT / "docs/fab/cad/v4-snap"
OLD_SHELL = ROOT / "docs/fab/cad/v2"
BOARD = ROOT / "hardware/board/elicio-v4.kicad_pcb"
DESIGN = ROOT / "docs/fab/board-v4-design.md"
NUMBER = r"[-+]?\d+(?:\.\d+)?"


def source_commit(path: Path) -> str:
    return subprocess.check_output(
        ["git", "log", "-1", "--format=%H", "--", str(path.relative_to(ROOT))],
        cwd=ROOT, text=True,
    ).strip()


def balanced(text: str, needle: str):
    """Yield top-level S-expressions beginning with needle, respecting quoted strings."""
    for match in re.finditer(r"(?m)^\s*\(" + re.escape(needle) + r"\s", text):
        start = text.index("(", match.start())
        depth, quoted, escape = 0, False, False
        for end in range(start, len(text)):
            ch = text[end]
            if quoted:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    quoted = False
            elif ch == '"':
                quoted = True
            elif ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    yield text[start:end + 1]
                    break


def parse_packing(text: str):
    section = text.split("## 5d. Flat pattern and pin table", 1)[1]
    folded = section.split("### Folded sites for the shell", 1)[1].split("### Shell extras", 1)[0]
    sites = {}
    for line in folded.splitlines():
        m = re.match(r"\| (P[1-5]) \|[^|]*\|\s*(" + NUMBER + r")\s*\|\s*(" + NUMBER + r")\s*\|\s*(" + NUMBER + r")\s*\|", line)
        if m:
            sites[m[1]] = tuple(map(float, m.groups()[1:]))
    if len(sites) != 5:
        raise ValueError("packing §5d folded site table not found")
    return sites


def parse_footprints(text: str):
    result = {}
    for block in balanced(text, "footprint"):
        ref = re.search(r'\(property "Reference" "([A-Z]+\d+)"', block)
        at = re.search(r"\(at\s+(" + NUMBER + r")\s+(" + NUMBER + r")(?:\s+(" + NUMBER + r"))?\)", block)
        if not ref or not at:
            continue
        if re.search(r"\(attr [^)]*\bdnp\b", block):
            continue
        # Courtyard is the mechanical envelope, not the package body. Use
        # fp_rect where available; the packing §5d table supplies the others.
        rect = next((r for r in balanced(block, "fp_rect") if '.CrtYd"' in r), None)
        size = None
        if rect:
            a = re.search(r"\(start\s+(" + NUMBER + r")\s+(" + NUMBER + r")\)", rect)
            b = re.search(r"\(end\s+(" + NUMBER + r")\s+(" + NUMBER + r")\)", rect)
            if a and b:
                size = (abs(float(a[1]) - float(b[1])), abs(float(a[2]) - float(b[2])))
        result[ref[1]] = dict(u=float(at[1]), s=float(at[2]), rot=float(at[3] or 0),
                              side="bottom" if '(layer "B.Cu")' in block[:180] else "top",
                              size=size)
    return result


def pin_table(text: str):
    section = text.split("### Pin table v2.1", 1)[1].split("### Folded sites for the shell", 1)[0]
    rows = {}
    for line in section.splitlines():
        m = re.match(r"\| ([A-Z]+\d+) \| (top|bottom|floor|both) \|\s*(" + NUMBER + r")\s*\|\s*(" + NUMBER + r")\s*\|\s*(" + NUMBER + r")\s*\|\s*(" + NUMBER + r") × (" + NUMBER + r") \|", line)
        if m:
            rows[m[1]] = (m[2], *map(float, m.groups()[2:]))
    return rows


def body_point(u: float, s: float, y: float, params: dict) -> tuple[float, float, float]:
    # Exact p_xyz / make_path map in scripts/cad/bte_fit_shell.py. The manifest
    # pins PATH_RADIUS, TOTAL_CHORD and CREASE_BOW for the exported solids.
    radius = params["PATH_RADIUS"]
    a = math.asin(params["TOTAL_CHORD"] / (2 * radius)) - s / radius
    return (params["CREASE_BOW"] - radius + (radius + u) * math.cos(a),
            y, -params["TOTAL_CHORD"] / 2 + (radius + u) * math.sin(a))


def compact_png(path: Path):
    """Bound PNG size without another dependency: reduce 8-bit RGB to 6-bit RGB.

    Retains full 2000-pixel geometry and exact sRGB/PNG decoding; only colour
    precision is reduced (64 levels/channel). Blender Cycles PNG has no alpha.
    """
    data = path.read_bytes()
    if len(data) < 1_800_000:
        return
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not PNG")
    chunks, compressed = [], bytearray()
    pos = 8
    while pos < len(data):
        n = struct.unpack_from(">I", data, pos)[0]
        kind = data[pos+4:pos+8]
        payload = data[pos+8:pos+8+n]
        if kind == b"IDAT":
            compressed.extend(payload)
        elif kind != b"IEND":
            chunks.append((kind, payload))
        pos += n+12
    head = chunks[0][1]
    width, height, depth, colour, *_ = struct.unpack(">IIBBBBB", head)
    if (depth, colour) != (8, 2):
        raise ValueError("expected Blender RGB8 PNG")
    raw = zlib.decompress(compressed)
    stride, cur, previous = width*3, 0, bytearray(width*3)
    packed = bytearray()
    for _ in range(height):
        f = raw[cur]; cur += 1
        scan = bytearray(raw[cur:cur+stride]); cur += stride
        for i in range(stride):
            a = scan[i-3] if i >= 3 else 0
            b = previous[i]
            c = previous[i-3] if i >= 3 else 0
            if f == 1: predictor = a
            elif f == 2: predictor = b
            elif f == 3: predictor = (a+b)//2
            elif f == 4:
                p = a+b-c
                predictor = min((a,b,c), key=lambda v: abs(p-v))
            elif f == 0: predictor = 0
            else: raise ValueError(f"PNG filter {f}")
            scan[i] = (scan[i]+predictor) & 255
        # No rescaling of pixels or scene; keep six highest bits of each channel.
        quant = bytearray(v & 252 for v in scan)
        packed.append(1)  # Sub predictor on the *quantized* scanline
        packed.extend((v - (quant[i-3] if i >= 3 else 0)) & 255 for i, v in enumerate(quant))
        previous = scan
    def chunk(kind, payload):
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind+payload))
    encoded = bytearray(data[:8])
    for kind, payload in chunks:
        encoded.extend(chunk(kind, payload))
    encoded.extend(chunk(b"IDAT", zlib.compress(packed, 9)))
    encoded.extend(chunk(b"IEND", b""))
    if len(encoded) < len(data):
        path.write_bytes(encoded)


def render(out: Path, samples: int, only: str | None):
    import bpy
    from mathutils import Vector

    out.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((SHELL / "manifest.json").read_text())
    params = manifest["parameters"]
    design = DESIGN.read_text()
    # §10.2 is the folded assembly authority. The footprint table supplies
    # physical courtyards and height intervals for the populated island.
    folded = design.split("### 10.2 Folded shell sites", 1)[1]
    sites = {}
    for line in folded.splitlines():
        m = re.match(r"\| (P[1-5]) ring .*?\| .*?\| \((" + NUMBER + r"), (" + NUMBER +
                     r")(?:, (" + NUMBER + r"))?\)", line)
        if m:
            # Floor-ring entries have a y range after the coordinate pair;
            # wall charge entries specify their axis as the third coordinate.
            y = float(m[4]) if m[4] else float(re.search(r"floor (" + NUMBER + r")", line)[1])
            sites[m[1]] = (float(m[2]), float(m[3]), y)
    if len(sites) != 5:
        raise ValueError(f"expected five §10.2 folded sites, got {sites}")
    footprints = parse_footprints(BOARD.read_text())
    shell_sha = source_commit(SHELL / "body_full_p15.step")
    board_sha = source_commit(BOARD)
    old_sha = source_commit(OLD_SHELL / "body_full_p15.step")
    interior_fix_sha = source_commit(ROOT / "docs/fab/cad/v4/body_full_p15.step")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    def material(name, rgba, metallic=0, roughness=.5):
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = (*rgba, 1)
        mat.use_nodes = True
        p = mat.node_tree.nodes.get("Principled BSDF")
        p.inputs["Base Color"].default_value = (*rgba, 1)
        p.inputs["Metallic"].default_value = metallic
        p.inputs["Roughness"].default_value = roughness
        return mat

    nylon = material("MJF PA12 natural warm grey", (.49, .51, .50), roughness=.78)
    titanium = material("unplated Grade 5 titanium", (.49, .53, .56), .78, .26)
    gold = material("ENIG gold over copper", (.62, .40, .12), .82, .21)
    brass = material("brass standoffs", (.48, .30, .13), .72, .31)
    flex = material("amber polyimide flexible PCB", (.39, .20, .07), .12, .48)
    pcb = material("FR4 stiffener under amber flex", (.25, .24, .17), .05, .65)
    silicon = material("electronics black moulded packages", (.045, .055, .06), .1, .45)
    metal = material("cell silver laminated foil", (.65, .69, .68), .7, .3)
    ink = material("engraved drive shadow", (.07, .09, .1), 0, .8)
    bgmat = material("warm neutral studio", (.76, .74, .70), 0, .85)
    objects = []

    def assign(obj, mat):
        obj.data.materials.append(mat)
        objects.append(obj)
        return obj

    def cube(name, center, dims, mat, bevel=0):
        bpy.ops.mesh.primitive_cube_add(size=1, location=center)
        obj = bpy.context.object
        obj.name = name
        obj.dimensions = dims
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        assign(obj, mat)
        if bevel:
            mod = obj.modifiers.new("soft physical edge", "BEVEL")
            mod.width = bevel
            mod.segments = 3
            obj.modifiers.new("weighted normals", "WEIGHTED_NORMAL")
        return obj

    def cyl(name, u, s, y, radius, height, mat, vertices=32, axis="y"):
        bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=height,
                                            location=body_point(u, s, y, params))
        obj = bpy.context.object
        obj.name = name
        if axis == "y":
            obj.rotation_euler[0] = math.pi / 2
        elif axis == "u":
            # A radial wall head points outward along the shell u coordinate.
            a = math.asin(params["TOTAL_CHORD"] / (2*params["PATH_RADIUS"])) - s/params["PATH_RADIUS"]
            obj.rotation_euler = Vector((math.cos(a), 0, math.sin(a))).to_track_quat("Z", "Y").to_euler()
        return assign(obj, mat)

    def curved_rect(name, u0, u1, s0, s1, y0, y1, mat):
        """Board island / folded tab swept along the committed shell arc."""
        n = max(2, math.ceil(abs(s1 - s0) / 1.5))
        vertices = []
        for y in (y0, y1):
            for i in range(n + 1):
                s = s0 + (s1 - s0) * i / n
                for u in (u0, u1):
                    vertices.append(body_point(u, s, y, params))
        faces = []
        layer = 2 * (n + 1)
        for i in range(n):
            for k in (0, 1):
                a = 2 * i + k
                b = a + 2
                faces.append((a, b, b + layer, a + layer))
        for i in range(n):
            a = 2 * i
            faces.extend(((a, a + 1, a + 3, a + 2),
                          (a + layer, a + layer + 2, a + layer + 3, a + layer + 1)))
        faces.extend(((0, layer, layer + 1, 1),
                      (2*n, 2*n+1, layer+2*n+1, layer+2*n)))
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertices, [], faces)
        mesh.update()
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.collection.objects.link(obj)
        return assign(obj, mat)

    def site_rect(name, uc, sc, wu, ws, yc, h, mat, bevel=0):
        # Courtyard axes are in (u,s), not Blender XYZ. A short curved sweep
        # gives an honest placement even at the bowed tail.
        obj = curved_rect(name, uc-wu/2, uc+wu/2, sc-ws/2, sc+ws/2,
                          yc-h/2, yc+h/2, mat)
        return obj

    for name in ("body_full_p15", "lid"):
        bpy.ops.wm.stl_import(filepath=str(SHELL / (name + ".stl")))
        obj = bpy.context.object
        obj.name = "PA12 " + ("body" if name.startswith("body") else "lid")
        assign(obj, nylon)
    lid = objects[-1]

    floor = params["WALL_MEDIAL"]
    top, underside = 5.12, 4.81  # §10.2 island, including 0.20 FR4 stiffener
    island_u = params["BOARD_ZONE_U"]
    island_s = params["BOARD_ZONE_S"]
    curved_rect("folded PI flex / populated island", *island_u, *island_s,
                underside, top, flex)
    # The released flat STEP cannot be used as an assembled board: its tabs
    # occupy the flat manufacturing coordinates. Use §10.2 folded envelopes.
    curved_rect("FR4 stiffener on flex island", *island_u, *island_s,
                underside, underside + .20, pcb)

    section = folded.split("#### Courtyards on the island", 1)[1].split("#### ", 1)[0]
    count = 0
    for line in section.splitlines():
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 6 or not re.fullmatch(r"[A-Z]+\d+", cols[0]):
            continue
        ref, side = cols[:2]
        if ref == "J3" or ref not in footprints:  # J3 is cut off per §10.2
            continue
        try:
            u0, u1 = map(float, cols[2].split("-"))
            s0, s1 = map(float, cols[3].split("-"))
            y0, y1 = map(float, cols[5].split("-"))
        except ValueError:
            continue
        if y1 <= y0:  # J4 is pads only, no component body
            continue
        site_rect(ref + " | §10.2 courtyard envelope", (u0+u1)/2, (s0+s1)/2,
                  u1-u0, s1-s0, (y0+y1)/2, y1-y0,
                  silicon if ref != "J2" else metal)
        count += 1
    if count < 40:
        raise ValueError(f"only {count} component courtyards found in §10.2")

    # Curved PI landing strips and REF pocket. Their bend curvature is a
    # schematic proxy, but their end sites are exactly the §10.2 fold sites.
    for pad in ("P1", "P2", "P3"):
        u, s, y = sites[pad]
        curved_rect(pad + " | folded PI landing", u-1.25, u+1.25,
                    min(s, island_s[0] if pad != "P3" else island_s[1]),
                    max(s, island_s[0] if pad != "P3" else island_s[1]),
                    y, y+.11, flex)
        cyl(pad + " | ENIG ring", u, s, y+.06, 2.5, .12, gold)
        cyl(pad + " | titanium M2.5 shaft", u, s, 1.85, 1.25, 3.7, titanium)
        cyl(pad + " | titanium button rim", u, s, -.23, 2.35, .46, titanium)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=12,
            location=body_point(u, s, -.65, params))
        cap = bpy.context.object
        cap.name = pad + " | titanium button crown"
        cap.scale = (2.17, .70, 2.17)
        assign(cap, titanium)
        cyl(pad + " | hex recess proxy", u, s, -1.34, .68, .035, ink, 6)
    # §10.2 charge flap lies on the posterior wall; contact axes are radial.
    curved_rect("P4/P5 folded charge flap proxy", 16.19, 16.50,
                1.75, 14.85, 1.695, 6.895, flex)
    for pad in ("P4", "P5"):
        u, s, y = sites[pad]
        cyl(pad + " | titanium posterior charging head", 17.05, s, y,
            1.35, 1.2, titanium, axis="u")
        cyl(pad + " | wall ENIG ring", 16.56, s, y, 1.6, .1, gold, axis="u")

    # §1.4 width chain and §4.1 cell bay: 501012 pouch 10.1 × 13 × 5.1.
    site_rect("501012 lithium pouch / foil envelope", (1.8+11.9)/2,
              (1.5+14.9)/2, 10.1, 13.0, floor+.5+5.1/2, 5.1, metal)
    # The v4-snap lid uses a hidden soft latch; there is no lid screw.

    # glTF distances are metres, Blender's numeric scene was millimetres.
    # Export a temporary 0.001-scaled instance, then restore the original mm
    # positions for the product render. Camera/caption/coin are excluded.
    transforms = [(obj, obj.location.copy(), obj.scale.copy()) for obj in objects]
    for obj in bpy.context.selected_objects:
        obj.select_set(False)
    for obj, loc, scale in transforms:
        obj.location = loc * .001
        obj.scale = scale * .001
        obj.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(out / "earpiece.glb"), export_format="GLB",
                              use_selection=True, export_yup=True,
                              export_apply=True, export_extras=True)
    for obj, loc, scale in transforms:
        obj.location, obj.scale = loc, scale

    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.render.threads_mode = "FIXED"
    scene.render.threads = 4
    scene.render.resolution_x, scene.render.resolution_y = 1050, 1300
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.image_settings.color_depth = "8"
    scene.render.image_settings.compression = 95
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (.72, .70, .67, 1)
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = .8
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    camera_data = bpy.data.cameras.new("studio orthographic")
    camera = bpy.data.objects.new("studio orthographic", camera_data)
    bpy.context.collection.objects.link(camera)
    scene.camera = camera
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = 80

    target = Vector(body_point(params["BODY_WIDTH"]/2, params["BODY_ARC"]/2, 4, params))
    def aim(location, at=target):
        camera.location = location
        camera.rotation_euler = (at - camera.location).to_track_quat("-Z", "Y").to_euler()

    def area(name, pos, power, size):
        light = bpy.data.lights.new(name, "AREA")
        light.energy = power
        light.shape = "DISK"
        light.size = size
        obj = bpy.data.objects.new(name, light)
        bpy.context.collection.objects.link(obj)
        obj.location = pos
        obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()
    area("key softbox", target + Vector((-35, -30, 35)), 18000, 65)
    area("fill softbox", target + Vector((40, 23, 7)), 22000, 58)
    area("rim softbox", target + Vector((10, 28, -35)), 15000, 42)
    bg = cube("studio backdrop (render only)", target + Vector((0, 0, -75)),
              (300, 300, 1), bgmat)
    objects.remove(bg)
    # Backdrop is replaced per view to stay behind the object.
    labelmat = material("print caption", (.16, .18, .19), roughness=1)
    caption = bpy.data.curves.new("caption lettering", "FONT")
    caption.body = f"V4 SNAP · 18 MM | shell {shell_sha[:9]} · board {board_sha[:9]}"
    caption.size = .74
    caption.space_character = 1.15
    capobj = bpy.data.objects.new("render caption (not in GLB)", caption)
    bpy.context.collection.objects.link(capobj)
    capobj.data.materials.append(labelmat)

    views = {
        "lateral": (Vector((35, 82, 55)), 80),
        "medial": (Vector((-27, -89, 55)), 80),
        "top": (Vector((28, 28, 95)), 80),
        "three_quarter": (Vector((78, 80, 71)), 85),
        "exploded": (Vector((65, 90, 64)), 95),
        "inside_lid_off": (Vector((-35, 85, 75)), 85),
        "quarter_scale": (Vector((78, 80, 71)), 100),
        "old_new": (Vector((35, 82, 55)), 110),
    }
    # Compare to a 24.26 mm US quarter: geometry is a scale prop only,
    # not an inference about coin metallurgy or numismatic detail.
    for name, (offset, scale) in views.items():
        if only and name != only:
            continue
        # Separation is presentation only; the exported GLB keeps the seated
        # lid. Derive the exploded offset from the committed body width.
        lid.location.x = 0 if name not in ("exploded", "inside_lid_off") else (
            params["BODY_WIDTH"] * (1.25 if name == "exploded" else 2))
        lid.location.y = 9 if name == "exploded" else 0
        aim(target+offset)
        camera_data.ortho_scale = scale
        bg.location = target + offset.normalized()*(-100)
        bg.rotation_euler = camera.rotation_euler
        # Caption rides the camera image plane and is excluded from GLB.
        bpy.context.view_layer.update()
        capobj.location = camera.matrix_world @ Vector((-scale*.36, -scale*.46, -24))
        capobj.rotation_euler = camera.rotation_euler
        if name == "old_new":
            bpy.ops.wm.stl_import(filepath=str(OLD_SHELL / "body_full_p15.stl"))
            old = bpy.context.object
            old.name = "old 22 mm PA12 body / same scale"
            old.location.x = -27
            old.data.materials.append(nylon)
            caption.body = f"22 MM shell {old_sha[:9]}  |  18 MM shell {shell_sha[:9]} · board {board_sha[:9]}"
        else:
            caption.body = f"V4 SNAP · 18 MM | shell {shell_sha[:9]} · board {board_sha[:9]}"
        if name == "quarter_scale":
            coin = cyl("US quarter / 24.26 mm scale prop", params["BODY_WIDTH"]+17,
                       params["BODY_ARC"]/2, -1, 12.13, 1.75, metal, 64)
            coin.name = "US quarter scale prop (render only)"
            objects.remove(coin)
        scene.render.filepath = str(out / (name + ".png"))
        bpy.ops.render.render(write_still=True)
        compact_png(out / (name + ".png"))
        if name == "quarter_scale":
            bpy.data.objects.remove(coin, do_unlink=True)
        if name == "old_new":
            bpy.data.objects.remove(old, do_unlink=True)

    metadata = {
        "label": "18 mm v4-snap; natural grey PA12 with titanium heads",
        "shell_commit": shell_sha, "board_commit": board_sha,
        "old_shell_commit": old_sha,
        "v4_interior_fix_commit": interior_fix_sha,
        "interior_caveat": "The v4 base interior fix is not present in the committed v4-snap solids. Outside uses v4-snap; lid-off interior is its earlier state, not the corrected v4 base.",
        "board_source": str(BOARD.relative_to(ROOT)),
        "flat_board_STEP_regenerated": "hardware/board/release/elicio-v4/elicio-v4.step",
        "shell_source": "docs/fab/cad/v4-snap/{body_full_p15,lid}.stl",
        "site_source": "docs/fab/board-v4-design.md §10.2 folded sites and courtyard envelopes; v4-snap manifest shell frame",
        "renderer": "Blender " + bpy.app.version_string + " Cycles CPU, 4 threads",
        "samples": samples,
        "pictures": {name: {"shell_commit": shell_sha, "board_commit": board_sha,
                            **({"old_shell_commit": old_sha} if name == "old_new" else {})}
                     for name in views if not only or name == only},
        "simplifications": [
            "The released flat board STEP cannot be bent directly; the populated island and folded sites are envelope geometry from §10.2, not copper traces or true bend transforms.",
            "Component blocks occupy §10.2 courtyards and documented height intervals; unverified component heights remain unverified.",
            "P4/P5 wall heads and the three button-head screws are titanium visual proxies without threads or detailed drives. Charging flap has no modelled bend radius or circuit traces.",
            "Nylon geometry is the committed STEP's STL export; cell is the §1.4 envelope without leads, plug or foam; quarter is a plain 24.26 mm scale disc.",
            "No lid screw: the v4-snap closure is concealed in the shell solids.",
        ],
    }
    (out / "captions.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print("preview outputs:", out)


def main():
    argv = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--samples", type=int, default=20)
    p.add_argument("--blender", default=os.environ.get("BLENDER", "blender"))
    p.add_argument("--only", choices=["lateral", "medial", "top", "three_quarter", "exploded", "inside_lid_off", "quarter_scale", "old_new"], help="render one view while adjusting lighting")
    args = p.parse_args(argv)
    if args.samples < 1:
        p.error("--samples must be positive")
    try:
        import bpy  # type: ignore[import-not-found]
    except ImportError:
        subprocess.run([args.blender, "-b", "-noaudio", "-t", "4", "--python", str(Path(__file__).resolve()),
                        "--", "--out", str(args.out.resolve()), "--samples", str(args.samples),
                        *(["--only", args.only] if args.only else [])], check=True)
    else:
        render(args.out.resolve(), args.samples, args.only)


if __name__ == "__main__":
    main()
