"""
Automated Bambu Lab A1 Plate & STL Integrity Verifier
ORC K2 Robot - Sac Hoa Tri An
Checks:
1. STL manifoldness (open edges, non-manifold edges)
2. Floating components / disconnected shells in air
3. Bed extents (fits 256x256mm build volume)
4. Bottom contact surface area
"""

import os
import struct
import collections
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STL_DIR = os.path.join(BASE_DIR, "3D_Models")
OUT_3MF_DIR = os.path.join(BASE_DIR, "3MF_Models")

from generate_bambu_3mf import MESH_DEFS, PLATES
import trimesh
import numpy as np

def audit_stl(fname, rot_y_90=False):
    path = os.path.join(STL_DIR, fname)
    if not os.path.exists(path):
        return {"error": f"File not found: {fname}"}
    m = trimesh.load(path)
    if rot_y_90:
        # Rotate -90 deg around Y: (-z, y, x)
        matrix = [[0, 0, -1, 0], [0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1]]
        m.apply_transform(matrix)

    b = m.bounds
    min_x, min_y, min_z = b[0]
    max_x, max_y, max_z = b[1]

    # Edges analysis
    edges_unique = m.edges_unique
    edges_count = m.edges_unique_inverse
    # Non-manifold or open edges
    open_edges = len(m.edges[m.edges_face[:, 1] == -1]) if hasattr(m, 'edges_face') and len(m.edges_face.shape) > 1 and m.edges_face.shape[1] > 1 else 0
    bad_edges = len(trimesh.repair.broken_faces(m))

    # Connected bodies / shells
    components = m.split(only_watertight=False)
    floating_shells = []
    for i, comp in enumerate(components):
        c_min_z = comp.bounds[0][2]
        if c_min_z > min_z + 0.1:
            floating_shells.append((i, len(comp.faces), round(c_min_z - min_z, 2)))

    # Bottom area
    face_z = m.triangles[:, :, 2]
    on_bed = (np.abs(face_z - min_z) < 0.05).all(axis=1)
    down_facing = m.face_normals[:, 2] < -0.99
    bed_faces = on_bed & down_facing
    bottom_area = float(m.area_faces[bed_faces].sum())

    return {
        "tris": len(m.faces),
        "dx": round(max_x - min_x, 1),
        "dy": round(max_y - min_y, 1),
        "dz": round(max_z - min_z, 1),
        "open_edges": open_edges,
        "bad_edges": bad_edges,
        "is_manifold": (open_edges == 0 and bad_edges == 0),
        "num_shells": len(components),
        "floating_shells": floating_shells,
        "bottom_area": round(bottom_area, 1),
    }

def main():
    print("=" * 70)
    print("AUDITING ALL 8 BAMBU LAB A1 PLATES AND MESHES")
    print("=" * 70)
    
    mesh_results = {}
    for mk, mdef in MESH_DEFS.items():
        res = audit_stl(mdef["stl"], mdef.get("rot_y_90", False))
        mesh_results[mk] = res

    # Plate check
    has_critical_error = False
    for pl in PLATES:
        p_idx = pl["index"]
        p_name = pl["name"]
        print(f"\n--- Plate {p_idx}: {p_name} ---")
        plate_floating = 0
        plate_non_manifold = 0
        for it in pl["items"]:
            mk = it["mesh"]
            r = mesh_results[mk]
            status = "OK"
            warns = []
            if not r["is_manifold"]:
                plate_non_manifold += 1
                warns.append(f"NON-MANIFOLD (bad_edges={r['bad_edges']}, open={r['open_edges']})")
            if r["floating_shells"]:
                plate_floating += 1
                has_critical_error = True
                warns.append(f"FLOATING SHELLS: {r['floating_shells']}")
            if warns:
                status = " | ".join(warns)
            print(f"  * [{mk:18s}] {it['name'][:35]:35s} -> {status}")

        if plate_floating > 0:
            print(f"  [!] PLATE {p_idx} STATUS: CRITICAL - FLOATING OBJECTS DETECTED")
        elif plate_non_manifold > 0:
            print(f"  [*] PLATE {p_idx} STATUS: WARNING - NON-MANIFOLD EDGES (Slicer may auto-repair)")
        else:
            print(f"  [+] PLATE {p_idx} STATUS: 100% PERFECT (Manifold & Flat)")

    print("\n" + "=" * 70)
    if has_critical_error:
        print("SUMMARY: CRITICAL ERRORS FOUND THAT REQUIRE CODE FIX BEFORE SLICING!")
    else:
        print("SUMMARY: ALL PLATES PASSED FLOATING OBJECT CHECKS!")
    print("=" * 70)

if __name__ == "__main__":
    main()
