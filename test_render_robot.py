import os
import subprocess
import time

WORKSPACE = r"c:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
OPENSCAD_BIN = r"C:\Program Files\OpenSCAD\openscad.exe"
MODELS_DIR = os.path.join(WORKSPACE, "3D_Models")

# SCAD scene: Full robot with Gripper V3
scad_full_robot = f'''
use <{os.path.join(MODELS_DIR, "full_assembly.scad")}>;
use <{os.path.join(MODELS_DIR, "gripper_v3_mg996r.scad")}>;

$fn = 48;

// Display full robot in stowed vs deployed with new gripper
translate([0, 0, 0]) {{
    // Base robot assembly
    full_assembly_dfm();
}}
'''

test_scad_p = os.path.join(MODELS_DIR, "test_full_robot_v3.scad")
out_png_p = os.path.join(MODELS_DIR, "preview_full_robot_with_gripper_v3.png")

with open(test_scad_p, "w", encoding="utf-8") as f:
    f.write(scad_full_robot)

cmd = [
    OPENSCAD_BIN,
    "--preview",
    "--camera=0,100,100,60,0,35,550",
    "--imgsize=1600,1200",
    "--colorscheme=Tomorrow Night",
    "-o", out_png_p,
    test_scad_p
]
print("Rendering full robot with gripper V3...")
t0 = time.time()
res = subprocess.run(cmd, capture_output=True, text=True)
print(f"Result code: {res.returncode} in {time.time()-t0:.2f}s")
if os.path.exists(out_png_p):
    print(f"Rendered image size: {os.path.getsize(out_png_p):,} bytes")
