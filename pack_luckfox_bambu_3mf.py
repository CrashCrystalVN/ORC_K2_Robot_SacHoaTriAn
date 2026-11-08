"""
pack_luckfox_bambu_3mf.py
Đóng gói bộ file in 3D Case bảo vệ Luckfox Pico Max (gá 2 ống Ø8.0mm tâm cách nhau 48.0mm)
thành file chuẩn Bambu Studio / OrcaSlicer (.3mf) đặt phẳng 100% tại Z=0, không cần Support (enable_support = 0).
"""

import os
import sys

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
sys.path.insert(0, BASE_DIR)

import generate_bambu_3mf as b3mf

CASE_STL_DIR = os.path.join(BASE_DIR, "3D_Models", "Luckfox_Pico_Max_Case")
OUT_3MF_DIR = os.path.join(BASE_DIR, "3MF_Models")
os.makedirs(OUT_3MF_DIR, exist_ok=True)

LUCKFOX_MESH_DEFS = {
    "bottom_sidemount": {
        "stl": "01A_Luckfox_Case_Bottom_SideMount_48mm.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "30%",
        "walls": "4",
    },
    "bottom_undermount": {
        "stl": "01B_Luckfox_Case_Bottom_UnderMount_48mm.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "30%",
        "walls": "4",
    },
    "bottom_vertical": {
        "stl": "01C_Luckfox_Case_Bottom_Vertical_48mm.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "30%",
        "walls": "4",
    },
    "top_lid": {
        "stl": "02_Luckfox_Case_Top_Lid.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "30%",
        "walls": "4",
    },
    "rod_locks": {
        "stl": "03_Rod_8mm_Lock_Caps_48mm.stl",
        "rot_y_90": False,
        "support": "0",
        "infill": "40%",
        "walls": "4",
    },
}

LUCKFOX_PLATES = [
    {
        "index": 1,
        "name": "Plate 1 - Bo Case Luckfox Pico Max Tieuchuan (Than Duoi Ngam Sau 48mm + Nap Tren + Khoa Kep Ong 8mm)",
        "file_slug": "Plate_Luckfox_Pico_Max_Case_Standard_48mm",
        "items": [
            {"mesh": "bottom_sidemount", "name": "01A_Luckfox_Case_Bottom_SideMount_48mm", "local_x": 128.0, "local_y": 85.0},
            {"mesh": "top_lid", "name": "02_Luckfox_Case_Top_Lid", "local_x": 128.0, "local_y": 140.0},
            {"mesh": "rod_locks", "name": "03_Rod_8mm_Lock_Caps_48mm", "local_x": 128.0, "local_y": 195.0},
        ],
    },
    {
        "index": 2,
        "name": "Plate 2 - Tat Ca Cac Tuy Chon Ga Ngang & Doc (01A + 01B + 01C + Nap 02 + Khoa 03)",
        "file_slug": "Plate_Luckfox_Pico_Max_All_Mount_Options_48mm",
        "items": [
            {"mesh": "bottom_sidemount", "name": "01A_Luckfox_Case_Bottom_SideMount_48mm", "local_x": 75.0, "local_y": 75.0},
            {"mesh": "bottom_undermount", "name": "01B_Luckfox_Case_Bottom_UnderMount_48mm", "local_x": 180.0, "local_y": 75.0},
            {"mesh": "bottom_vertical", "name": "01C_Luckfox_Case_Bottom_Vertical_48mm", "local_x": 75.0, "local_y": 165.0},
            {"mesh": "top_lid", "name": "02_Luckfox_Case_Top_Lid", "local_x": 180.0, "local_y": 145.0},
            {"mesh": "rod_locks", "name": "03_Rod_8mm_Lock_Caps_48mm", "local_x": 180.0, "local_y": 205.0},
        ],
    },
]


def main():
    b3mf.MESH_DEFS.update(LUCKFOX_MESH_DEFS)
    loaded_meshes = {}
    for mk, mdef in LUCKFOX_MESH_DEFS.items():
        stl_path = os.path.join(CASE_STL_DIR, mdef["stl"])
        verts, tris, (hx, hy, hz), (cx, cy, cz) = b3mf.load_binary_stl_and_center(
            stl_path, rot_y_90=mdef["rot_y_90"]
        )
        loaded_meshes[mk] = (verts, tris, (hx, hy, hz), (cx, cy, cz))
        print(
            f"  [{mk:18s}] verts={len(verts):5d}, tris={len(tris):5d}, size={2*hx:6.2f}x{2*hy:6.2f}x{2*hz:6.2f}mm, z_bot={cz-hz:6.2f}mm"
        )

    project_settings_str = b3mf.get_a1_project_settings()

    out_master = os.path.join(OUT_3MF_DIR, "Luckfox_Pico_Max_Case_48mm_RodMount_Bambu_A1.3mf")
    b3mf.create_bambu_3mf(LUCKFOX_PLATES, out_master, project_settings_str, loaded_meshes)
    print(f"[3MF] Created {out_master}")

    out_std = os.path.join(CASE_STL_DIR, "Luckfox_Pico_Max_Case_48mm_RodMount_Bambu_A1.3mf")
    b3mf.create_bambu_3mf([LUCKFOX_PLATES[0]], out_std, project_settings_str, loaded_meshes)
    print(f"[3MF] Created {out_std}")


if __name__ == "__main__":
    main()

