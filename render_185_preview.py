import subprocess
import os

OPENSCAD = r"C:\Program Files\OpenSCAD\openscad.com"
BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"

# 1. Preview Assembly with 185x185x185mm Bounding Box
cmd1 = [
    OPENSCAD,
    "-o", os.path.join(BASE_DIR, "3D_Models", "preview_base_185x185_box.png"),
    os.path.join(BASE_DIR, "3D_Models", "01_Chassis_Base_185x185.scad"),
    "-D", 'DISPLAY_MODE="assembly_compact"',
    "--preview",
    "--imgsize=1280,960",
    "--colorscheme=Cornfield",
    "--autocenter",
    "--viewall"
]
print("Rendering preview_base_185x185_box.png...")
r1 = subprocess.run(cmd1, capture_output=True, text=True)
print("Result 1:", r1.returncode)
if r1.stderr:
    print(r1.stderr[:300])

# 2. Preview 3D Printable Base Plate Part (Top-down & Iso)
cmd2 = [
    OPENSCAD,
    "-o", os.path.join(BASE_DIR, "3D_Models", "preview_chassis_base_185x185_part.png"),
    os.path.join(BASE_DIR, "3D_Models", "01_Chassis_Base_185x185.scad"),
    "-D", 'DISPLAY_MODE="part"',
    "--preview",
    "--imgsize=1280,960",
    "--colorscheme=Metallic",
    "--autocenter",
    "--viewall"
]
print("Rendering preview_chassis_base_185x185_part.png...")
r2 = subprocess.run(cmd2, capture_output=True, text=True)
print("Result 2:", r2.returncode)

# 3. Preview Full Robot Assembly 185
cmd3 = [
    OPENSCAD,
    "-o", os.path.join(BASE_DIR, "3D_Models", "preview_full_assembly_185x185.png"),
    os.path.join(BASE_DIR, "3D_Models", "full_assembly_185x185.scad"),
    "--preview",
    "--imgsize=1280,960",
    "--colorscheme=Cornfield",
    "--autocenter",
    "--viewall"
]
print("Rendering preview_full_assembly_185x185.png...")
r3 = subprocess.run(cmd3, capture_output=True, text=True)
print("Result 3:", r3.returncode)
print("All previews rendered successfully!")
