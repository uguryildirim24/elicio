#!/usr/bin/env python3
"""Illustrative v4 STL views (board envelope is schematic, not a PCB assembly)."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import trimesh
import bte_fit_shell as cad


def draw(out: Path, angle: tuple[int,int], board: bool, filename: str):
    mesh = trimesh.load(out/'body_full_p15.stl', force='mesh')
    lid = trimesh.load(out/'lid.stl', force='mesh')
    fig = plt.figure(figsize=(9,9),dpi=130)
    ax = fig.add_axes((0,0,1,0.91), projection='3d', proj_type='ortho')
    for solid,color in ((mesh,'#9babb9'),(lid,'#d2dbe4')):
        faces=solid.triangles
        coll=Poly3DCollection(faces,facecolor=color,edgecolor='none',alpha=0.42 if board else 1)
        ax.add_collection3d(coll)
    if board:
        params,_=cad.build_reference_params(variant='full',preload=1.5,
            overrides=cad.load_params_file(cad.SCRIPT_DIR/'params/shell_v4.toml'),crease_bow_from_m=False)
        path=cad.make_path(params['BODY_ARC'],params['CREASE_BOW'])
        for u0,u1,s0,s1,y,label in ((2.25,15.75,16,37.6,5.12,'island'),
                                     (16.19,16.50,1.75,14.85,4.30,'folded charge plate')):
            points=np.array([cad.p_xyz(path,u,s,y) for u,s in ((u0,s0),(u1,s0),(u1,s1),(u0,s1),(u0,s0))])
            ax.plot(points[:,0],points[:,1],points[:,2],color='#e15739',linewidth=2.3,label=label)
        ax.legend(loc='lower left')
    bounds=np.vstack((mesh.vertices,lid.vertices))
    mid=(bounds.min(axis=0)+bounds.max(axis=0))/2
    radius=max(np.ptp(bounds,axis=0))/2
    ax.set_xlim(mid[0]-radius,mid[0]+radius);ax.set_ylim(mid[1]-radius,mid[1]+radius);ax.set_zlim(mid[2]-radius,mid[2]+radius)
    ax.set_box_aspect(np.ptp(bounds,axis=0),zoom=1.05)
    ax.view_init(elev=angle[0],azim=angle[1]);ax.set_axis_off()
    fig.suptitle('Elicio v4 • W18 / T8.1 • hinge only, closure unresolved'+ ('\nSchematic folded board envelope (not component CAD)' if board else ''), y=0.99, fontsize=11)
    fig.savefig(out/filename,bbox_inches='tight');plt.close(fig)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=cad.REPO_ROOT/'docs/fab/cad/v4')
    out=parser.parse_args().out
    for angle,board,file in (((25,-75),False,'render_medial.png'),((27,100),False,'render_lateral.png'),((32,-55),True,'render_folded_board.png')):
        draw(out,angle,board,file)
    manifest=out/'manifest.json';data=json.loads(manifest.read_text())
    data['views']={name:{'sha256':cad.sha256_file(out/name),'bytes':(out/name).stat().st_size}
                   for name in ('render_medial.png','render_lateral.png','render_folded_board.png')}
    manifest.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':main()
