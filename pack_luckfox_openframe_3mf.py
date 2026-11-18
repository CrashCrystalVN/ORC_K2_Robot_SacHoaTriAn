"""
pack_luckfox_openframe_3mf.py
Đóng gói bộ file STL Open-Frame Luckfox Pico Max / Pro & ToF VL53L5CX V2
gá trên 2 ống Ø8.0mm (C-C 56.0mm) thành file .3mf chuẩn Bambu Studio / OrcaSlicer.
100% phẳng tại Z = 0.0mm, enable_support = 0 (0% Support).
"""

import os
import sys

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
sys.path.insert(0, BASE_DIR)

import generate_bambu_3mf as b3mf

CASE_STL_DIR = os.path.join(BASE_DIR, "3D_Models", "Luckfox_Pico_OpenFrame_56mm")
OUT_3MF_DIR = os.path.join(BASE_DIR, "3MF_Models")
os.makedirs(OUT_3MF_DIR, exist_ok=True)

MESH_DEFS = {
    "undermount_base": {
        "stl": "01A_Luckfox_OpenFrame_UnderMount_56mm.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "30%",
        "walls": "4",
    },
    "backmount_base": {
        "stl": "01B_Luckfox_OpenFrame_BackMount_56mm.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "30%",
        "walls": "4",
    },
    "dual_bar_undermount": {
        "stl": "02A_Rod_Clamp_Dual_Bar_56mm.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "40%",
        "walls": "4",
    },
    "dual_bar_backmount": {
        "stl": "02B_Rod_Clamp_BackMount_56mm.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "40%",
        "walls": "4",
    },
    "pcb_retainer": {
        "stl": "03_Luckfox_PCB_Top_Retainer.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "30%",
        "walls": "4",
    },
    "tof_bracket": {
        "stl": "04_VL53L5CX_V2_Sensor_Bracket.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "40%",
        "walls": "4",
    },
}

PLATES = [
    {
        "index": 1,
        "name": "Plate 1 - OpenFrame UnderMount 56mm + Khoa Ong + Nep PCB + Gia ToF VL53L5CX",
        "file_slug": "Plate_Luckfox_OpenFrame_UnderMount_56mm_Full",
        "items": [
            {"mesh": "undermount_base", "name": "01A_Luckfox_OpenFrame_UnderMount_56mm", "local_x": 128.0, "local_y": 70.0},
            {"mesh": "dual_bar_undermount", "name": "02A_Rod_Clamp_Dual_Bar_56mm", "local_x": 128.0, "local_y": 120.0},
            {"mesh": "pcb_retainer", "name": "03_Luckfox_PCB_Top_Retainer", "local_x": 128.0, "local_y": 165.0},
            {"mesh": "tof_bracket", "name": "04_VL53L5CX_V2_Sensor_Bracket", "local_x": 128.0, "local_y": 205.0},
        ],
    },
    {
        "index": 2,
        "name": "Plate 2 - OpenFrame BackMount 56mm (Ong Dung Z) + Khoa Ong + Nep PCB + Gia ToF",
        "file_slug": "Plate_Luckfox_OpenFrame_BackMount_56mm_Full",
        "items": [
            {"mesh": "backmount_base", "name": "01B_Luckfox_OpenFrame_BackMount_56mm", "local_x": 128.0, "local_y": 70.0},
            {"mesh": "dual_bar_backmount", "name": "02B_Rod_Clamp_BackMount_56mm", "local_x": 128.0, "local_y": 120.0},
            {"mesh": "pcb_retainer", "name": "03_Luckfox_PCB_Top_Retainer", "local_x": 128.0, "local_y": 165.0},
            {"mesh": "tof_bracket", "name": "04_VL53L5CX_V2_Sensor_Bracket", "local_x": 128.0, "local_y": 205.0},
        ],
    },
]

def main():
    b3mf.MESH_DEFS.update(MESH_DEFS)
    loaded_meshes = {}
    for mk, mdef in MESH_DEFS.items():
        stl_path = os.path.join(CASE_STL_DIR, mdef["stl"])
        verts, tris, (hx, hy, hz), (cx, cy, cz) = b3mf.load_binary_stl_and_center(
            stl_path, rot_y_90=mdef["rot_y_90"]
        )
        loaded_meshes[mk] = (verts, tris, (hx, hy, hz), (cx, cy, cz))
        print(
            f"  [{mk:20s}] verts={len(verts):5d}, tris={len(tris):5d}, size={2*hx:6.2f}x{2*hy:6.2f}x{2*hz:6.2f}mm, z_bot={cz-hz:6.2f}mm"
        )

    project_settings_str = b3mf.get_a1_project_settings()

    out_master = os.path.join(OUT_3MF_DIR, "Luckfox_Pico_OpenFrame_56mm_RodMount_Bambu_A1.3mf")
    b3mf.create_bambu_3mf(PLATES, out_master, project_settings_str, loaded_meshes)
    print(f"[3MF] Created {out_master}")

    out_local = os.path.join(CASE_STL_DIR, "Luckfox_Pico_OpenFrame_56mm_RodMount_Bambu_A1.3mf")
    b3mf.create_bambu_3mf(PLATES, out_local, project_settings_str, loaded_meshes)
    print(f"[3MF] Created {out_local}")

if __name__ == "__main__":
    main()
