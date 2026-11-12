import os
import subprocess
import re
import struct

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
STL_DIR = os.path.join(BASE_DIR, "3D_Models")
OPENSCAD = r"C:\Program Files\OpenSCAD\openscad.exe"

# Import generate_redesigned_parts
import generate_redesigned_parts as grp

# Find the two target parts
target_stls = ["01D_K2_Hub_Adapter_Plate.stl", "01D_Snap_Clip_K2_Hub.stl"]
parts_to_render = [p for p in grp.PARTS if p["stl_name"] in target_stls]

print(f"Found {len(parts_to_render)} parts to render:")
for p in parts_to_render:
    stl_path = os.path.join(STL_DIR, p["stl_name"])
    temp_scad = os.path.join(STL_DIR, "_temp_" + p["stl_name"].replace(".stl", ".scad"))
    with open(temp_scad, "w", encoding="utf-8") as f:
        f.write(p["scad_code"])
    print(f"-> Rendering {p['stl_name']}...")
    res = subprocess.run([OPENSCAD, "-o", stl_path, temp_scad], capture_output=True, text=True)
    if os.path.exists(temp_scad):
        os.remove(temp_scad)
    if res.returncode == 0 and os.path.exists(stl_path):
        grp.convert_stl_to_binary(stl_path)
        print(f"   [SUCCESS] {p['stl_name']} (Binary size: {os.path.getsize(stl_path):,} bytes)")
    else:
        print(f"   [FAILED] {p['stl_name']}: {res.stderr}")
