#!/usr/bin/env python3
"""Offline v4-snap assembly from committed shell STLs and §10.2 folded sites.

Exports GLB in metres and renders in millimetres via SceneKit on macOS or
Blender on Linux. Requires NumPy and Pillow. No board STEP is bent: the flat
STEP is not the geometry of the folded assembly.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import struct
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from assemble_photo import ROOT, SHELL, OLD_SHELL, BOARD, DESIGN, source_commit, parse_footprints

MATERIALS = {
    "nylon": ([.49, .51, .50, 1], 0, .78),
    "titanium": ([.49, .53, .56, 1], .78, .26),
    "gold": ([.62, .40, .12, 1], .82, .21),
    "flex": ([.39, .20, .07, 1], .12, .48),
    "pcb": ([.25, .24, .17, 1], .05, .65),
    "silicon": ([.045, .055, .06, 1], .1, .45),
    "cell": ([.65, .69, .68, 1], .7, .3),
}
VIEWS = ("lateral", "medial", "top", "three_quarter", "exploded",
         "inside_lid_off", "quarter_scale", "old_new")


def stl(path: Path):
    data = path.read_bytes()
    n = struct.unpack_from("<I", data, 80)[0]
    if len(data) != 84 + 50*n:
        raise ValueError(f"not a binary triangle STL: {path}")
    raw = np.ndarray((n,), dtype=np.dtype([("normal", "<f4", (3,)),
                                             ("points", "<f4", (3, 3)),
                                             ("attribute", "<u2")]), buffer=data, offset=84)
    return raw["points"].copy().reshape(-1, 3)


def save_stl(path: Path, vertices: np.ndarray):
    tris = vertices.reshape(-1, 3, 3).astype("<f4")
    normal = np.cross(tris[:, 1]-tris[:, 0], tris[:, 2]-tris[:, 0])
    normal /= np.maximum(np.linalg.norm(normal, axis=1, keepdims=True), 1e-10)
    raw = np.empty(len(tris), dtype=np.dtype([("normal", "<f4", (3,)),
                                             ("points", "<f4", (3, 3)),
                                             ("attribute", "<u2")]))
    raw["normal"], raw["points"], raw["attribute"] = normal, tris, 0
    path.write_bytes(b"Elicio native assembly".ljust(80, b"\0") + struct.pack("<I", len(raw)) + raw.tobytes())


def box(x0, x1, y0, y1, z0, z1):
    v = [(x0,y0,z0), (x1,y0,z0), (x1,y1,z0), (x0,y1,z0),
         (x0,y0,z1), (x1,y0,z1), (x1,y1,z1), (x0,y1,z1)]
    fs = [(0,2,1),(0,3,2), (4,5,6),(4,6,7), (0,1,5),(0,5,4),
          (1,2,6),(1,6,5), (2,3,7),(2,7,6), (3,0,4),(3,4,7)]
    return np.array([v[k] for face in fs for k in face], dtype="<f4")


def make_scene(tmp: Path):
    params = json.loads((SHELL/"manifest.json").read_text())["parameters"]
    design = DESIGN.read_text()
    folded = design.split("### 10.2 Folded shell sites", 1)[1]
    footprints = parse_footprints(BOARD.read_text())
    radius, chord, bow = (params[k] for k in ("PATH_RADIUS", "TOTAL_CHORD", "CREASE_BOW"))

    def point(u, s, y):
        angle = math.asin(chord / (2*radius)) - s/radius
        return np.array((bow-radius+(radius+u)*math.cos(angle), y,
                         -chord/2+(radius+u)*math.sin(angle)), dtype="<f4")

    parts = []
    def add(name, vertices, mat, *, group="main", source=None):
        path = source or tmp/(f"part_{len(parts):03d}.stl")
        if source is None:
            save_stl(path, vertices)
        parts.append(dict(name=name, path=str(path), material=mat, group=group))
        return vertices

    add("v4-snap body", None, "nylon", source=SHELL/"body_full_p15.stl")
    add("v4-snap lid", None, "nylon", group="lid", source=SHELL/"lid.stl")

    def curved(u0, u1, s0, s1, y0, y1):
        n = max(2, math.ceil(abs(s1-s0)/1.5))
        # build a closed swept hexagonal slab, subdivision follows shell arc
        rings = []
        for s in np.linspace(s0, s1, n+1):
            rings.append(np.array([point(u, float(s), y) for u,y in
                                   ((u0,y0),(u1,y0),(u1,y1),(u0,y1))]))
        result = []
        faces = ((0,1,2),(0,2,3))
        for i in range(n):
            a,b = rings[i],rings[i+1]
            for j in range(4):
                k=(j+1)%4
                result.extend((a[j],b[j],b[k], a[j],b[k],a[k]))
        for a, reverse in ((rings[0], True),(rings[-1], False)):
            for f in faces:
                result.extend(a[list(reversed(f)) if reverse else list(f)])
        return np.array(result, dtype="<f4")

    def cylinder(u,s,y,r,h,axis="y", segments=24):
        def xyz(theta, delta):
            a = math.asin(chord/(2*radius))-s/radius
            tangent_u = np.array([math.cos(a),0,math.sin(a)])
            tangent_s = np.array([math.sin(a),0,-math.cos(a)])
            if axis == "y":
                return point(u,s,y) + r*(math.cos(theta)*tangent_u+math.sin(theta)*tangent_s) + np.array([0,delta,0])
            return point(u,s,y) + delta*tangent_u + r*(math.cos(theta)*tangent_s+math.sin(theta)*np.array([0,1,0]))
        if axis == "y":
            direction = np.array([0, 1, 0])
        else:
            a = math.asin(chord/(2*radius))-s/radius
            direction = np.array([math.cos(a), 0, math.sin(a)])
        bottom = point(u,s,y)-direction*h/2
        top = point(u,s,y)+direction*h/2
        tris=[]
        for i in range(segments):
            a,b=2*math.pi*i/segments,2*math.pi*(i+1)/segments
            p,q=xyz(a,-h/2),xyz(b,-h/2)
            P,Q=xyz(a,h/2),xyz(b,h/2)
            tris.extend((p,q,Q,p,Q,P,bottom,q,p,top,P,Q))
        return np.array(tris, dtype="<f4")

    iu0,iu1=params["BOARD_ZONE_U"]; is0,is1=params["BOARD_ZONE_S"]
    add("folded polyimide island",curved(iu0,iu1,is0,is1,4.81,5.12),"flex")
    add("FR4 stiffener",curved(iu0,iu1,is0,is1,4.81,5.01),"pcb")
    section=folded.split("#### Courtyards on the island",1)[1].split("#### ",1)[0]
    count=0
    for line in section.splitlines():
        cols=[c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols)<6 or cols[0] not in footprints or cols[0]=="J3":
            continue
        try:
            u0,u1=map(float,cols[2].split("-"));s0,s1=map(float,cols[3].split("-"))
            y0,y1=map(float,cols[5].split("-"))
        except ValueError:
            continue
        if y1>y0:
            add(cols[0]+" courtyard block",curved(u0,u1,s0,s1,y0,y1),"cell" if cols[0]=="J2" else "silicon")
            count+=1
    if count<40:
        raise ValueError(f"only {count} folded component blocks")
    import re
    number=r"[-+]?\d+(?:\.\d+)?"
    sites={}
    for line in folded.splitlines():
        m=re.match(r"\| (P[1-5]) ring .*?\| .*?\| \(("+number+r"), ("+number+r")(?:, ("+number+r"))?\)",line)
        if m:
            y=float(m[4]) if m[4] else float(re.search(r"floor ("+number+r")",line)[1])
            sites[m[1]]=(float(m[2]),float(m[3]),y)
    if len(sites)!=5:
        raise ValueError("missing §10.2 folded sites")
    for pad in ("P1","P2","P3"):
        u,s,y=sites[pad]
        add(pad+" folded landing",curved(u-1.25,u+1.25,min(s,is0 if pad!="P3" else is1),max(s,is0 if pad!="P3" else is1),y,y+.11),"flex")
        add(pad+" ENIG ring",cylinder(u,s,y+.06,2.5,.12),"gold")
        add(pad+" titanium M2.5 shaft",cylinder(u,s,1.85,1.25,3.7),"titanium")
        add(pad+" titanium button",cylinder(u,s,-.45,2.35,.9),"titanium")
    add("posterior folded charge flap",curved(16.19,16.50,1.75,14.85,1.695,6.895),"flex")
    for pad in ("P4","P5"):
        u,s,y=sites[pad]
        add(pad+" posterior titanium head",cylinder(17.05,s,y,1.35,1.2,"u"),"titanium")
        add(pad+" posterior ENIG ring",cylinder(16.56,s,y,1.6,.1,"u"),"gold")
    add("501012 cell envelope",curved(1.8,11.9,1.5,14.5,2.0,7.1),"cell")
    add("US quarter / 24.26 mm plain scale disc",cylinder(params["BODY_WIDTH"]+17,params["BODY_ARC"]/2,-1,12.13,1.75),"cell",group="coin")
    add("old 22 mm body",None,"nylon",group="old",source=OLD_SHELL/"body_full_p15.stl")
    return parts,params


def export_glb(path: Path, parts):
    meshes=[]; nodes=[]; views=[]; accessors=[]; payload=bytearray()
    mats=list(MATERIALS)
    materials=[{"name":name,"pbrMetallicRoughness":{"baseColorFactor":rgba,"metallicFactor":metallic,"roughnessFactor":roughness},"doubleSided":True} for name,(rgba,metallic,roughness) in MATERIALS.items()]
    for part in parts:
        if part["group"] not in ("main","lid"):
            continue
        coords=stl(Path(part["path"])).astype("<f4")*.001
        # Preserve source STL triangle winding; glTF coordinates are metres.
        normals=np.cross(coords[1::3]-coords[::3],coords[2::3]-coords[::3])
        normals/=np.maximum(np.linalg.norm(normals,axis=1,keepdims=True),1e-12)
        normals=np.repeat(normals,3,axis=0).astype("<f4")
        attrs={}
        for label,values in (("POSITION",coords),("NORMAL",normals)):
            while len(payload)%4:payload.append(0)
            offset=len(payload);payload.extend(values.tobytes())
            views.append({"buffer":0,"byteOffset":offset,"byteLength":values.nbytes,"target":34962})
            accessor={"bufferView":len(views)-1,"componentType":5126,"count":len(values),"type":"VEC3"}
            if label=="POSITION":
                accessor.update(min=values.min(axis=0).tolist(),max=values.max(axis=0).tolist())
            accessors.append(accessor);attrs[label]=len(accessors)-1
        meshes.append({"name":part["name"],"primitives":[{"attributes":attrs,"material":mats.index(part["material"]),"mode":4}]})
        nodes.append({"mesh":len(meshes)-1,"name":part["name"]})
    doc={"asset":{"version":"2.0","generator":"Elicio native folded-site assembly"},"scene":0,
         "scenes":[{"nodes":list(range(len(nodes)))}],"nodes":nodes,"meshes":meshes,
         "materials":materials,"buffers":[{"byteLength":len(payload)}],"bufferViews":views,"accessors":accessors}
    j=json.dumps(doc,separators=(",",":")).encode();j+=b" "*((-len(j))%4)
    payload.extend(b"\0"*((-len(payload))%4))
    path.write_bytes(struct.pack("<4sII",b"glTF",2,12+8+len(j)+8+len(payload))+
                     struct.pack("<I4s",len(j),b"JSON")+j+
                     struct.pack("<I4s",len(payload),b"BIN\0")+payload)


def caption_png(path:Path, caption:str):
    image=Image.open(path).convert("RGB")
    draw=ImageDraw.Draw(image)
    font_path=ROOT/"scripts/cad/fonts/LiberationSans-Regular.ttf"
    font=ImageFont.truetype(str(font_path),18)
    draw.rounded_rectangle((22,image.height-74,image.width-22,image.height-22),radius=10,fill=(234,231,225))
    draw.text((40,image.height-60),caption,fill=(41,44,47),font=font)
    image.save(path,optimize=True)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="elicio-assembly-") as d:
        tmp=Path(d);parts,params=make_scene(tmp)
        export_glb(out/"earpiece.glb",parts)
        (tmp/"scene.json").write_text(json.dumps({"parts":parts,"materials":MATERIALS,"params":params,"out":str(out)}))
        if sys.platform == "darwin":
            renderer = ["swift", str(Path(__file__).with_suffix(".swift")), str(tmp/"scene.json")]
        else:
            renderer = ["blender", "-b", "-noaudio", "-t", "4", "--python",
                        str(Path(__file__).with_name("assemble_blender.py")), "--", str(tmp/"scene.json")]
        subprocess.run(renderer, check=True)
    shell_sha=source_commit(SHELL/"body_full_p15.step")
    board_sha=source_commit(BOARD)
    old_sha=source_commit(OLD_SHELL/"body_full_p15.step")
    for view in VIEWS:
        caption=(f"22 mm shell {old_sha[:9]}  |  18 mm shell {shell_sha[:9]}  ·  board {board_sha[:9]}" if view=="old_new"
                 else f"18 mm V4 SNAP  |  shell {shell_sha[:9]}  ·  board {board_sha[:9]}")
        caption_png(out/(view+".png"),caption)
    metadata={"label":"18 mm v4-snap, natural grey PA12 with titanium heads",
        "shell_commit":shell_sha,"board_commit":board_sha,"old_shell_commit":old_sha,
        "shell_source":"docs/fab/cad/v4-snap/{body_full_p15,lid}.stl",
        "board_source":"hardware/board/elicio-v4.kicad_pcb and docs/fab/board-v4-design.md §10.2",
        "renderer":("macOS SceneKit" if sys.platform == "darwin" else "Blender Cycles CPU") + ", orthographic; Pillow caption overlays",
        "pictures":{view:{"shell_commit":shell_sha,"board_commit":board_sha,
                          **({"old_shell_commit":old_sha} if view=="old_new" else {})} for view in VIEWS},
        "simplifications":["Board and populated components are folded §10.2 courtyard envelopes, not a bent STEP or exact component CAD; cell is a dimensioned envelope without leads.",
                           "M2.5 titanium heads and wall charging heads are smooth visual proxies without threads; quarter is a plain 24.26 mm disc.",
                           "This v4-snap STL includes the local C6, U3 and U5 chip reliefs; its interior still differs from the v4 base interior correction. The snap latch is concealed; there is no lid screw. Nominal reliefs are not print-tolerance proof."]}
    (out/"captions.json").write_text(json.dumps(metadata,indent=2)+"\n")
    for f in out.iterdir():
        if f.suffix in (".png",".glb"):
            print(f.name,f.stat().st_size)


if __name__=="__main__":main()
