import os
import sys

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
sys.path.insert(0, BASE_DIR)

import generate_bambu_3mf as b3mf

STL_DIR = os.path.join(BASE_DIR, "3D_Models")
OUT_3MF_DIR = os.path.join(BASE_DIR, "3MF_Models")
os.makedirs(OUT_3MF_DIR, exist_ok=True)

GRIPPER_V3_MESH_DEFS = {
    "gripper_base_v3": {
        "stl": "04_Gripper_Base_Head_V3.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "40%",
        "walls": "4",
    },
    "jaw_left_v3": {
        "stl": "05_Gripper_Jaw_Left_V3.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "50%",
        "walls": "4",
    },
    "jaw_right_v3": {
        "stl": "06_Gripper_Jaw_Right_V3.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "50%",
        "walls": "4",
    },
    "wrist_s3": {
        "stl": "04A_Wrist_Clevis_Pitch_Bracket_S3.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "40%",
        "walls": "4",
    }
}

GRIPPER_V3_PLATES = [
    {
        "index": 1,
        "name": "Plate 1 - Bo Dau Kep V3.0 MG996R Goc Mo 0-90 Do (Be 04 + 2 Ngam 05, 06 + Co Tay 04A)",
        "file_slug": "Plate_Gripper_V3_MG996R_FlatPrint",
        "items": [
            {"mesh": "gripper_base_v3", "name": "04_Gripper_Base_Head_V3", "local_x": 80.0, "local_y": 75.0},
            {"mesh": "wrist_s3", "name": "04A_Wrist_Clevis_Pitch_Bracket_S3", "local_x": 175.0, "local_y": 75.0},
            {"mesh": "jaw_left_v3", "name": "05_Gripper_Jaw_Left_V3", "local_x": 75.0, "local_y": 175.0},
            {"mesh": "jaw_right_v3", "name": "06_Gripper_Jaw_Right_V3", "local_x": 175.0, "local_y": 175.0},
        ],
    }
]

def main():
    b3mf.MESH_DEFS.update(GRIPPER_V3_MESH_DEFS)
    loaded_meshes = {}
    for mk, mdef in GRIPPER_V3_MESH_DEFS.items():
        stl_path = os.path.join(STL_DIR, mdef["stl"])
        verts, tris, (hx, hy, hz), (cx, cy, cz) = b3mf.load_binary_stl_and_center(
            stl_path, rot_y_90=mdef["rot_y_90"]
        )
        loaded_meshes[mk] = (verts, tris, (hx, hy, hz), (cx, cy, cz))
        print(
            f"  [{mk:18s}] verts={len(verts):5d}, tris={len(tris):5d}, size={2*hx:6.2f}x{2*hy:6.2f}x{2*hz:6.2f}mm, z_bot={cz-hz:6.2f}mm"
        )

    project_settings_str = b3mf.get_a1_project_settings()

    out_3mf_path = os.path.join(OUT_3MF_DIR, "Plate_Gripper_V3_MG996R_0_to_90_deg.3mf")
    b3mf.create_bambu_3mf(GRIPPER_V3_PLATES, out_3mf_path, project_settings_str, loaded_meshes)
    print(f"[3MF] Created {out_3mf_path}")

    out_3mf_models = os.path.join(STL_DIR, "Plate_Gripper_V3_MG996R_0_to_90_deg.3mf")
    b3mf.create_bambu_3mf(GRIPPER_V3_PLATES, out_3mf_models, project_settings_str, loaded_meshes)
    print(f"[3MF] Created {out_3mf_models}")

if __name__ == "__main__":
    main()
