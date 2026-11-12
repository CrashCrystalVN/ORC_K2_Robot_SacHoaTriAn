"""
Pack Bambu Lab 3MF Production Package for Balanced Omni Base
Plate_01_Chassis_Base_Balanced_Omni.3mf
"""

import os
import shutil
from export_bambu_3mf_packages import export_3mf_package, load_base_project_settings, BASE_DIR, STL_DIR, OUT_3MF_DIR

def pack_plate_01_balanced_omni():
    settings = load_base_project_settings()
    
    # Bambu Lab A1 Mini build plate is 180x180mm. Center is at (90, 90).
    # Part bounds: X = 136mm, Y = 160.5mm.
    # Placed at (90, 90) on A1 Mini or (128, 128) on A1 standard.
    # We place at (90.0, 90.0) so it's directly centered on Bambu Lab A1 Mini 180x180 plate!
    items = [
        {
            "stl_name": "01_Chassis_Base_Balanced_Omni.stl",
            "display_name": "01_Chassis_Base_Balanced_Omni",
            "pos_x": 90.0,
            "pos_y": 90.0,
            "walls": "4",       # 4 walls for extra stiffness and thread holding
            "infill": "25%",     # Gyroid 25% infill
            "support": "0"      # 0% support - 100% self supporting with teardrop 45°
        }
    ]
    
    out_3mf_1 = os.path.join(OUT_3MF_DIR, "Plate_01_Chassis_Base_Balanced_Omni.3mf")
    export_3mf_package(out_3mf_1, "Plate 01: Chassis Base Balanced Omni", items, settings)
    print(f"Generated: {out_3mf_1} ({os.path.getsize(out_3mf_1):,} bytes)")
    
    # Also copy to 3D_Models for easy access in CAD folder
    out_3mf_2 = os.path.join(STL_DIR, "Plate_01_Chassis_Base_Balanced_Omni.3mf")
    shutil.copyfile(out_3mf_1, out_3mf_2)
    print(f"Copied to: {out_3mf_2} ({os.path.getsize(out_3mf_2):,} bytes)")

if __name__ == "__main__":
    pack_plate_01_balanced_omni()
