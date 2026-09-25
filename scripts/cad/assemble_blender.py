#!/usr/bin/env python3
"""Render the STL manifest made by assemble_native.py with Blender on Linux.

Invoked by Blender in background mode, after the GLB has been written from the
same mesh list. Coordinates in the manifest are millimetres; only the GLB uses
metres.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector

manifest = json.loads(Path(sys.argv[sys.argv.index("--") + 1]).read_text())
parts = manifest["parts"]
materials = manifest["materials"]
params = manifest["params"]
out = Path(manifest["out"])

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 32
scene.cycles.use_denoising = False
scene.render.threads_mode = "FIXED"
scene.render.threads = 4
scene.render.resolution_x = 1050
scene.render.resolution_y = 1300
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"
scene.render.film_transparent = False
scene.world.color = (.65, .64, .62)
scene.view_settings.view_transform = "Standard"
scene.view_settings.look = "Medium High Contrast"

finishes = {}
for name, (rgba, metallic, roughness) in materials.items():
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = rgba
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = rgba
    shader.inputs["Metallic"].default_value = metallic
    shader.inputs["Roughness"].default_value = roughness
    finishes[name] = mat

groups = {}
for part in parts:
    bpy.ops.wm.stl_import(filepath=part["path"])
    obj = bpy.context.object
    obj.name = part["name"]
    obj.data.materials.append(finishes[part["material"]])
    groups.setdefault(part["group"], []).append(obj)

def point(u, s, y):
    import math
    r = params["PATH_RADIUS"]
    a = math.asin(params["TOTAL_CHORD"] / (2*r)) - s/r
    return Vector((params["CREASE_BOW"]-r+(r+u)*math.cos(a), y,
                   -params["TOTAL_CHORD"]/2+(r+u)*math.sin(a)))

target = point(params["BODY_WIDTH"]/2, params["BODY_ARC"]/2, 4)

camera_data = bpy.data.cameras.new("studio orthographic")
camera = bpy.data.objects.new("studio orthographic", camera_data)
bpy.context.collection.objects.link(camera)
scene.camera = camera
camera_data.type = "ORTHO"
camera_data.clip_end = 400

def area(name, offset, power, size):
    light = bpy.data.lights.new(name, "AREA")
    light.energy = power
    light.shape = "DISK"
    light.size = size
    obj = bpy.data.objects.new(name, light)
    bpy.context.collection.objects.link(obj)
    obj.location = target + Vector(offset)
    obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()

area("soft key", (-35, -30, 35), 18000, 65)
area("soft fill", (40, 23, 7), 22000, 58)
area("soft rim", (10, 28, -35), 15000, 42)

views = (
    ("lateral", (35, 82, 55), 84),
    ("medial", (-27, -89, 55), 84),
    ("top", (28, 28, 95), 82),
    ("three_quarter", (78, 80, 71), 96),
    ("exploded", (65, 90, 64), 100),
    ("inside_lid_off", (-35, 85, 75), 110),
    ("quarter_scale", (78, 80, 71), 88),
    ("old_new", (35, 82, 55), 135),
)
for name, offset, scale in views:
    for lid in groups["lid"]:
        lid.location = ((params["BODY_WIDTH"] * 1.25 if name == "exploded" else
                         params["BODY_WIDTH"] * 2 if name == "inside_lid_off" else 0),
                        9 if name == "exploded" else 0, 0)
    for old in groups["old"]:
        old.hide_render = name != "old_new"
        old.location = (-27, 0, 0)
    for coin in groups["coin"]:
        coin.hide_render = name != "quarter_scale"
    camera_data.ortho_scale = scale
    aim = target + (Vector((-12, 0, 0)) if name == "old_new" else Vector((0, 0, 0)))
    camera.location = aim + Vector(offset)
    camera.rotation_euler = (aim - camera.location).to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = str(out / (name + ".png"))
    bpy.ops.render.render(write_still=True)
    print("rendered", name, flush=True)
