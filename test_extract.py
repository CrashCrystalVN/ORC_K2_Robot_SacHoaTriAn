import os
import subprocess

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
OPENSCAD = r"C:\Program Files\OpenSCAD\openscad.exe"

test_plate_scad = os.path.join(BASE_DIR, "test_plate_hardened.scad")
test_plate_stl = os.path.join(BASE_DIR, "test_plate_hardened.stl")
test_clip_scad = os.path.join(BASE_DIR, "test_clip_hardened.scad")
test_clip_stl = os.path.join(BASE_DIR, "test_clip_hardened.stl")

# Read SCAD_LIBRARY from generate_redesigned_parts.py
with open(os.path.join(BASE_DIR, "generate_redesigned_parts.py"), "r", encoding="utf-8") as f:
    code = f.read()

# Extract SCAD_LIBRARY
match = code.find('SCAD_LIBRARY = """')
if match != -1:
    start = match + len('SCAD_LIBRARY = """')
    end = code.find('"""\n\n# ====================================================================\n# EXPORT CONFIGURATION', start)
    if end == -1:
        end = code.find('"""\n\nPARTS_TO_GENERATE', start)
    scad_library = code[start:end]
else:
    print("Could not find SCAD_LIBRARY")
    exit(1)

print("SCAD_LIBRARY extracted successfully, length:", len(scad_library))
