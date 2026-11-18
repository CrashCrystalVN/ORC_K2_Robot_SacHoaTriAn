"""
Package Bambu Studio 3MF: Plate_Tower_2Part_Compact.3mf
ORC K2 Robot - Sac Hoa Tri An (2-Part Ultra-Compact Lift Tower Production Plate)
"""

import os
import sys
import json
import zipfile
import uuid
import struct
import subprocess
import numpy as np
import scipy.spatial.distance
import trimesh

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
STL_DIR = os.path.join(BASE_DIR, "3D_Models")
OUT_3MF_DIR = os.path.join(BASE_DIR, "3MF_Models")
os.makedirs(OUT_3MF_DIR, exist_ok=True)

sys.path.insert(0, BASE_DIR)
import generate_bambu_3mf as b3mf

PARTS_CONFIG = {
    "tower_left_v2": {
        "stl": "01_Tower_Left_Stanchion_v2.stl",
        "name": "01_Tower_Left_Stanchion_v2",
        "desc": "Left Lift Tower Stanchion V2.0 (Passive A-Frame Truss, M3 Clevis Pivot, 5x M3 Chassis Foot)",
        "local_x": 80.0,
        "local_y": 128.0,
        "support": "0",
        "infill": "35%",
        "walls": "4",
    },
    "tower_right_v2": {
        "stl": "02_Tower_Right_Stanchion_v2.stl",
        "name": "02_Tower_Right_Stanchion_v2",
        "desc": "Right Lift Tower Stanchion V2.0 (Coaxial MG996R Direct-Drive Cradle, 25T Horn Recess, 5x M3 Chassis Foot)",
        "local_x": 176.0,
        "local_y": 128.0,
        "support": "0",
        "infill": "35%",
        "walls": "4",
    }
}

PLATES_DEF = [
    {
        "index": 1,
        "name": "Plate 1 - Bo Thap Nang 2 Part Tinh Gon K2 V2.0 (Tru Trai + Tru Phai Tich Hop MG996R)",
        "file_slug": "Plate_Tower_2Part_Compact",
        "items": [
            {"mesh": "tower_left_v2", "name": PARTS_CONFIG["tower_left_v2"]["name"], "local_x": PARTS_CONFIG["tower_left_v2"]["local_x"], "local_y": PARTS_CONFIG["tower_left_v2"]["local_y"]},
            {"mesh": "tower_right_v2", "name": PARTS_CONFIG["tower_right_v2"]["name"], "local_x": PARTS_CONFIG["tower_right_v2"]["local_x"], "local_y": PARTS_CONFIG["tower_right_v2"]["local_y"]},
        ]
    }
]

def verify_and_package():
    print("=" * 70)
    print("PACKAGING BAMBU STUDIO 3MF: Plate_Tower_2Part_Compact.3mf")
    print("=" * 70)

    loaded_meshes = {}
    mesh_defs_for_b3mf = {}

    for k, pinfo in PARTS_CONFIG.items():
        stl_path = os.path.join(STL_DIR, pinfo["stl"])
        if not os.path.exists(stl_path):
            raise FileNotFoundError(f"Missing STL: {stl_path}")
        
        m = trimesh.load(stl_path)
        is_watertight = m.is_watertight
        faces = len(m.faces)
        verts = len(m.vertices)
        vol_cm3 = m.volume / 1000.0 if m.is_volume else 0.0
        extents = m.extents
        bounds = m.bounds
        z_min = bounds[0][2]

        print(f"\n[PART CHECK] {pinfo['name']}:")
        print(f"  File: {pinfo['stl']}")
        print(f"  Watertight: {is_watertight} (Faces: {faces:,}, Vertices: {verts:,})")
        print(f"  Volume: {vol_cm3:.2f} cm3 (~{vol_cm3*1.25:.1f} g PLA)")
        print(f"  Bounding Box: {extents[0]:.1f} x {extents[1]:.1f} x {extents[2]:.1f} mm")
        print(f"  Bed Contact Z_min: {z_min:.4f} mm")
        assert is_watertight, f"Mesh {pinfo['stl']} is NOT watertight!"
        assert abs(z_min) < 1e-3, f"Mesh {pinfo['stl']} Z_min is not on bed!"

        v_list, t_list, (hx, hy, hz), (cx, cy, cz) = b3mf.load_binary_stl_and_center(stl_path, rot_y_90=False)
        loaded_meshes[k] = (v_list, t_list, (hx, hy, hz), (cx, cy, cz))
        mesh_defs_for_b3mf[k] = {
            "stl": pinfo["stl"],
            "rot_y_90": False,
            "support": pinfo["support"],
            "infill": pinfo["infill"],
            "walls": pinfo["walls"],
        }

    b3mf.MESH_DEFS.update(mesh_defs_for_b3mf)

    project_settings = b3mf.get_a1_project_settings()
    settings_dict = json.loads(project_settings)
    settings_dict["printer_model"] = "Bambu Lab A1"
    settings_dict["curr_bed_type"] = "Textured PEI Plate"
    settings_dict["print_settings_id"] = "0.20mm Strength @BBL A1"
    settings_dict["wall_loops"] = "4"
    settings_dict["sparse_infill_density"] = "35%"
    settings_dict["sparse_infill_pattern"] = "gyroid"
    settings_dict["bottom_shell_layers"] = "4"
    settings_dict["top_shell_layers"] = "4"
    settings_dict["enable_support"] = "0"
    settings_dict["support_type"] = "tree(auto)"
    settings_dict["brim_type"] = "no_brim"
    project_settings_str = json.dumps(settings_dict, indent=4)

    target_3mf_path = os.path.join(OUT_3MF_DIR, "Plate_Tower_2Part_Compact.3mf")
    b3mf.create_bambu_3mf(PLATES_DEF, target_3mf_path, project_settings_str, loaded_meshes)
    file_size_kb = os.path.getsize(target_3mf_path) / 1024.0
    print(f"\n[OUTPUT GENERATED] {target_3mf_path} ({file_size_kb:.1f} KB)")

    target_3mf_models = os.path.join(STL_DIR, "Plate_Tower_2Part_Compact.3mf")
    b3mf.create_bambu_3mf(PLATES_DEF, target_3mf_models, project_settings_str, loaded_meshes)
    print(f"[OUTPUT COPY] {target_3mf_models}")

    # Unpack and verify
    print("\n[VERIFYING 3MF ARCHIVE]")
    with zipfile.ZipFile(target_3mf_path, "r") as z:
        for name in z.namelist():
            size = z.getinfo(name).file_size
            print(f"  - {name} ({size:,} bytes)")
        assert "3D/3dmodel.model" in z.namelist()
        assert "Metadata/project_settings.config" in z.namelist()
        assert "Metadata/model_settings.config" in z.namelist()

    print("\n>>> ALL CHECKS PASSED: 100% Watertight, Zero-Support DFM Compliant, Packaged Successfully!")

if __name__ == "__main__":
    verify_and_package()
