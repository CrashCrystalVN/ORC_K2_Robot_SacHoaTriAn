import os
import subprocess
import time

WORKSPACE = r"c:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
OPENSCAD_BIN = r"C:\Program Files\OpenSCAD\openscad.exe"
MODELS_DIR = os.path.join(WORKSPACE, "3D_Models")

RENDERS = [
    {
        "name": "preview_robot_stowed_gripper_v3.png",
        "scad": f'''
$fn = 48;
ARM_STATE = "stowed";
JAW_GRIP_ANGLE = 0.0;
include <{os.path.join(MODELS_DIR, "full_assembly.scad")}>;
''',
        "camera": "0,90,90,55,0,30,520",
        "desc": "ORC K2 Robot - Stowed Configuration with Gripper V3 Closed (0°)"
    },
    {
        "name": "preview_robot_deployed_gripper_v3_open45.png",
        "scad": f'''
$fn = 48;
ARM_STATE = "deployed";
JAW_GRIP_ANGLE = 45.0;
include <{os.path.join(MODELS_DIR, "full_assembly.scad")}>;
''',
        "camera": "0,130,80,55,0,30,550",
        "desc": "ORC K2 Robot - Deployed Configuration with Gripper V3 Wide Open (45° per jaw, Total 90°)"
    },
    {
        "name": "preview_robot_stowed_gripper_v3_open90.png",
        "scad": f'''
$fn = 48;
ARM_STATE = "stowed";
JAW_GRIP_ANGLE = 90.0;
include <{os.path.join(MODELS_DIR, "full_assembly.scad")}>;
''',
        "camera": "0,90,90,55,0,30,520",
        "desc": "ORC K2 Robot - Stowed Configuration with Gripper V3 Folded Flat Transverse (90°)"
    }
]

for r in RENDERS:
    scad_tmp = os.path.join(MODELS_DIR, "temp_" + r["name"].replace(".png", ".scad"))
    out_png = os.path.join(MODELS_DIR, r["name"])
    with open(scad_tmp, "w", encoding="utf-8") as f:
        f.write(r["scad"])
    cmd = [
        OPENSCAD_BIN,
        "--preview",
        "--camera=" + r["camera"],
        "--imgsize=1600,1200",
        "--colorscheme=Tomorrow Night",
        "-o", out_png,
        scad_tmp
    ]
    print(f"Rendering {r['name']} ...")
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Rendered in {time.time()-t0:.2f}s ({os.path.getsize(out_png):,} bytes)")
    try:
        os.remove(scad_tmp)
    except:
        pass

print("ALL ROBOT PREVIEWS RENDERED!")
