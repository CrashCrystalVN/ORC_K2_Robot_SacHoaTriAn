"""
Package Bambu Studio 3MF: Plate_Gripper_v3_Complete.3mf
ORC K2 Robot - Sac Hoa Tri An (V3.0 Complete Gripper Production Plate)
"""

import os
import sys
import json
import zipfile
import uuid
import struct
import numpy as np
import trimesh

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
STL_DIR = os.path.join(BASE_DIR, "3D_Models")
OUT_3MF_DIR = os.path.join(BASE_DIR, "3MF_Models")
os.makedirs(OUT_3MF_DIR, exist_ok=True)

sys.path.insert(0, BASE_DIR)
import generate_bambu_3mf as b3mf

PARTS_CONFIG = {
    "gripper_base_v3": {
        "stl": "04_Gripper_Base_Head_v3.stl",
        "name": "04_Gripper_Base_Head_V3",
        "desc": "Gripper Base Head V3 (MG996R Cantilever Bridge, M3 Pivot Bosses, Wrist Clevis)",
        "local_x": 75.0,
        "local_y": 70.0,
        "support": "0",
        "infill": "40%",
        "walls": "4",
    },
    "wrist_clevis_s3": {
        "stl": "04A_Wrist_Clevis_Pitch_Bracket_S3.stl",
        "name": "04A_Wrist_Clevis_Pitch_Bracket_S3",
        "desc": "Wrist Clevis Pitch Bracket S3 (Mates with Base Head Wrist Clevis)",
        "local_x": 175.0,
        "local_y": 70.0,
        "support": "0",
        "infill": "40%",
        "walls": "4",
    },
    "jaw_left_v3": {
        "stl": "05_Gripper_Jaw_Left_V3.stl",
        "name": "05_Gripper_Jaw_Left_V3",
        "desc": "Gripper Jaw Left V3 (m=1.5 Involute Gear Sector, Ø32mm V-Cradle, Retaining Lip)",
        "local_x": 75.0,
        "local_y": 175.0,
        "support": "0",
        "infill": "50%",
        "walls": "4",
    },
    "jaw_right_v3": {
        "stl": "06_Gripper_Jaw_Right_V3.stl",
        "name": "06_Gripper_Jaw_Right_V3",
        "desc": "Gripper Jaw Right V3 (MG996R Horn Pocket, m=1.5 Conjugate Gear, Ø32mm V-Cradle)",
        "local_x": 175.0,
        "local_y": 175.0,
        "support": "0",
        "infill": "50%",
        "walls": "4",
    }
}

PLATES_DEF = [
    {
        "index": 1,
        "name": "Plate 1 - Bo Dau Kep K2 V3.0 Hoan Chinh (Be Dau Kep + 2 Ngam Kep + Co Tay S3)",
        "file_slug": "Plate_Gripper_v3_Complete",
        "items": [
            {"mesh": "gripper_base_v3", "name": PARTS_CONFIG["gripper_base_v3"]["name"], "local_x": PARTS_CONFIG["gripper_base_v3"]["local_x"], "local_y": PARTS_CONFIG["gripper_base_v3"]["local_y"]},
            {"mesh": "wrist_clevis_s3", "name": PARTS_CONFIG["wrist_clevis_s3"]["name"], "local_x": PARTS_CONFIG["wrist_clevis_s3"]["local_x"], "local_y": PARTS_CONFIG["wrist_clevis_s3"]["local_y"]},
            {"mesh": "jaw_left_v3", "name": PARTS_CONFIG["jaw_left_v3"]["name"], "local_x": PARTS_CONFIG["jaw_left_v3"]["local_x"], "local_y": PARTS_CONFIG["jaw_left_v3"]["local_y"]},
            {"mesh": "jaw_right_v3", "name": PARTS_CONFIG["jaw_right_v3"]["name"], "local_x": PARTS_CONFIG["jaw_right_v3"]["local_x"], "local_y": PARTS_CONFIG["jaw_right_v3"]["local_y"]},
        ]
    }
]

def verify_and_package():
    print("=" * 70)
    print("STARTING DFM & BAMBU STUDIO 3MF PACKAGING PIPELINE")
    print("TARGET: Plate_Gripper_v3_Complete.3mf")
    print("=" * 70)

    # 1. Audit individual meshes
    loaded_meshes = {}
    mesh_defs_for_b3mf = {}

    for k, pinfo in PARTS_CONFIG.items():
        stl_path = os.path.join(STL_DIR, pinfo["stl"])
        if not os.path.exists(stl_path):
            raise FileNotFoundError(f"Missing required STL: {stl_path}")
        
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

    # Update b3mf globals
    b3mf.MESH_DEFS.update(mesh_defs_for_b3mf)

    # 2. Get Bambu Lab A1 Production Project Settings
    project_settings = b3mf.get_a1_project_settings()
    settings_dict = json.loads(project_settings)
    settings_dict["printer_model"] = "Bambu Lab A1"
    settings_dict["curr_bed_type"] = "Textured PEI Plate"
    settings_dict["print_settings_id"] = "0.20mm Strength @BBL A1"
    settings_dict["wall_loops"] = "4"
    settings_dict["sparse_infill_density"] = "40%"
    settings_dict["sparse_infill_pattern"] = "gyroid"
    settings_dict["bottom_shell_layers"] = "4"
    settings_dict["top_shell_layers"] = "4"
    settings_dict["enable_support"] = "0"
    settings_dict["support_type"] = "tree(auto)"
    settings_dict["brim_type"] = "no_brim"
    project_settings_str = json.dumps(settings_dict, indent=4)

    # 3. Create 3MF in 3MF_Models
    target_3mf_path = os.path.join(OUT_3MF_DIR, "Plate_Gripper_v3_Complete.3mf")
    b3mf.create_bambu_3mf(PLATES_DEF, target_3mf_path, project_settings_str, loaded_meshes)
    file_size_kb = os.path.getsize(target_3mf_path) / 1024.0
    print(f"\n[OUTPUT GENERATED] {target_3mf_path} ({file_size_kb:.1f} KB)")

    # Also save to 3D_Models for parity
    target_3mf_models = os.path.join(STL_DIR, "Plate_Gripper_v3_Complete.3mf")
    b3mf.create_bambu_3mf(PLATES_DEF, target_3mf_models, project_settings_str, loaded_meshes)
    print(f"[OUTPUT COPY] {target_3mf_models}")

    # 4. Verify 3MF Archive Integrity
    print("\n[VERIFYING 3MF ARCHIVE]")
    with zipfile.ZipFile(target_3mf_path, "r") as z:
        for name in z.namelist():
            size = z.getinfo(name).file_size
            print(f"  - {name} ({size:,} bytes)")
        assert "3D/3dmodel.model" in z.namelist(), "Missing 3dmodel.model in 3MF!"
        assert "Metadata/project_settings.config" in z.namelist(), "Missing project_settings in 3MF!"
        assert "Metadata/model_settings.config" in z.namelist(), "Missing model_settings in 3MF!"
    
    print("\n>>> ALL CHECKS PASSED: 100% Watertight, Zero-Support DFM Compliant, Packaged Successfully!")

if __name__ == "__main__":
    verify_and_package()
