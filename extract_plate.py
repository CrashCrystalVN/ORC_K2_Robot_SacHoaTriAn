import sys
sys.path.append(r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn")
import generate_redesigned_parts

for part in generate_redesigned_parts.PARTS:
    if part["stl_name"] == "01D_K2_Hub_Adapter_Plate.stl":
        with open(r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\test_cur_plate.scad", "w", encoding="utf-8") as f:
            f.write(part["scad_code"])
        print("Wrote test_cur_plate.scad successfully")
        break
