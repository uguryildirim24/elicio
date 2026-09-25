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


def draw(out: Path, angle: tuple[int,int], board: bool, filename: str, detail: bool = False):
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
    if detail:
        ax.set_xlim(10,21);ax.set_ylim(0,8.2);ax.set_zlim(-46,-35)
        ax.set_box_aspect((11,8.2,11),zoom=1.1)
    ax.view_init(elev=angle[0],azim=angle[1]);ax.set_axis_off()
    closure=json.loads((out/'manifest.json').read_text())['closure']['type']
    fig.suptitle('Elicio v4 • W18 / T8.1 • '+closure+ ('\nSchematic folded board envelope (not component CAD)' if board else ''), y=0.99, fontsize=11)
    fig.savefig(out/filename,bbox_inches='tight');plt.close(fig)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=cad.REPO_ROOT/'docs/fab/cad/v4')
    parser.add_argument('--single', action='store_true', help='only render the medial closure view')
    args=parser.parse_args();out=args.out
    views=(((25,-75),False,'render_closure.png'),) if args.single else (((25,-75),False,'render_medial.png'),((27,100),False,'render_lateral.png'),((32,-55),True,'render_folded_board.png'))
    for angle,board,file in views:
        draw(out,angle,board,file,detail=args.single)
    manifest=out/'manifest.json';data=json.loads(manifest.read_text())
    data['views']={name:{'sha256':cad.sha256_file(out/name),'bytes':(out/name).stat().st_size}
                   for _,_,name in views}
    manifest.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':main()
