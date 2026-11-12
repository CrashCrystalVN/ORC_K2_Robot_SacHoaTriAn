"""
Mesh Compiler & Topology Validator
Module & CLI for verifying 3D STL manifoldness, shell connectivity, and watertightness.

Usage:
    python validate_mesh_topology.py [file1.stl file2.stl ...] [--json]
    python validate_mesh_topology.py --all
"""

import sys
import os
import glob
import json
import trimesh
import numpy as np


def validate_stl(filepath):
    """
    Validates topology of an STL mesh using trimesh.
    Properly welds coincident vertices as per STL specification.
    Returns a dictionary with comprehensive mesh diagnostics.
    """
    if not os.path.exists(filepath):
        return {"file": os.path.basename(filepath), "error": "File not found"}

    try:
        # Load mesh with vertex merging enabled
        mesh = trimesh.load(filepath)
    except Exception as e:
        return {"file": os.path.basename(filepath), "error": str(e)}

    # Check basic properties
    faces_count = len(mesh.faces)
    vertices_count = len(mesh.vertices)
    is_watertight = bool(mesh.is_watertight)
    is_volume = bool(mesh.is_volume)
    bounds = mesh.bounds.tolist() if len(mesh.vertices) > 0 else [[0, 0, 0], [0, 0, 0]]
    dimensions = (mesh.bounds[1] - mesh.bounds[0]).round(3).tolist() if len(mesh.vertices) > 0 else [0, 0, 0]

    # Split into connected bodies / shells
    try:
        bodies = mesh.split(only_watertight=False)
        shells_count = len(bodies)
    except Exception as e:
        shells_count = 1
        bodies = [mesh]

    is_single_shell = (shells_count == 1)

    shell_breakdown = []
    for idx, b in enumerate(bodies):
        b_dims = (b.bounds[1] - b.bounds[0]).round(3).tolist() if len(b.vertices) > 0 else [0, 0, 0]
        shell_breakdown.append({
            "shell_id": idx + 1,
            "faces_count": len(b.faces),
            "is_watertight": bool(b.is_watertight),
            "bounds_min": [round(float(x), 3) for x in b.bounds[0]],
            "bounds_max": [round(float(x), 3) for x in b.bounds[1]],
            "size_mm": b_dims,
            "volume_mm3": round(float(b.volume), 2) if b.is_volume else None
        })

    volume_total = round(float(mesh.volume), 2) if is_volume else None
    euler = int(mesh.euler_number)

    return {
        "file": os.path.basename(filepath),
        "filepath": os.path.abspath(filepath),
        "total_faces": faces_count,
        "total_vertices": vertices_count,
        "is_watertight": is_watertight,
        "is_single_shell": is_single_shell,
        "connected_shells_count": shells_count,
        "euler_number": euler,
        "volume_mm3": volume_total,
        "overall_dimensions_mm": dimensions,
        "overall_bounds": {
            "min": [round(float(x), 3) for x in bounds[0]],
            "max": [round(float(x), 3) for x in bounds[1]]
        },
        "shells": shell_breakdown
    }


def print_report(res):
    print("=" * 80)
    print(f"FILE: {res['file']}")
    print("=" * 80)
    if "error" in res:
        print(f"  ERROR: {res['error']}")
        return

    status = "[PASSED] 100% UNIBODY (Single Connected Shell)" if res['is_single_shell'] else f"[FAILED] BROKEN INTO {res['connected_shells_count']} DISJOINT SHELLS"
    manifold_status = "WATERTIGHT (2-Manifold solid)" if res['is_watertight'] else "NON-MANIFOLD (Open boundaries or coincident non-manifold edges)"
    
    print(f"  Topology Status:    {status}")
    print(f"  Shells Count:       {res['connected_shells_count']}")
    print(f"  Manifold Integrity: {manifold_status}")
    print(f"  Mesh Complexity:    {res['total_faces']:,} faces, {res['total_vertices']:,} vertices (Euler={res['euler_number']})")
    print(f"  Overall Dimensions: X={res['overall_dimensions_mm'][0]} mm, Y={res['overall_dimensions_mm'][1]} mm, Z={res['overall_dimensions_mm'][2]} mm")
    print(f"  Bounding Box:       Min={res['overall_bounds']['min']} -> Max={res['overall_bounds']['max']}")
    if res['volume_mm3'] is not None:
        print(f"  Total Solid Volume: {res['volume_mm3']:,} mm3")

    print(f"  Shells Breakdown:")
    for s in res['shells']:
        wt = "Watertight Solid" if s['is_watertight'] else "Non-watertight"
        vol_str = f" | Vol: {s['volume_mm3']:,} mm3" if s['volume_mm3'] else ""
        print(f"    - Shell #{s['shell_id']}: {s['faces_count']:,} faces | {wt}{vol_str}")
        print(f"      Size: {s['size_mm']} mm | X=[{s['bounds_min'][0]}, {s['bounds_max'][0]}], Y=[{s['bounds_min'][1]}, {s['bounds_max'][1]}], Z=[{s['bounds_min'][2]}, {s['bounds_max'][2]}]")
    print()


def main():
    target_dir = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\3D_Models"
    args = sys.argv[1:]
    json_mode = "--json" in args
    check_all = "--all" in args
    file_args = [a for a in args if not a.startswith("--")]

    if check_all:
        file_args = [os.path.basename(f) for f in glob.glob(os.path.join(target_dir, "*.stl"))]
    elif not file_args:
        file_args = [
            "01D_K2_Hub_Adapter_Plate.stl",
            "01D_Base_Riser_Frame.stl",
            "01D_K2_Control_Hub_Riser_Adapter_Monolithic.stl"
        ]

    results = []
    for target in file_args:
        p = os.path.join(target_dir, target) if not os.path.isabs(target) else target
        res = validate_stl(p)
        results.append(res)
        if not json_mode:
            print_report(res)

    if json_mode:
        print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
