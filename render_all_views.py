"""
Render all 3D previews for Balanced Omni Base and Full Assembly
"""

import os
import subprocess
import time

OPENSCAD_EXE = r"C:\Program Files\OpenSCAD\openscad.exe"
MODELS_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\3D_Models"

renders = [
    # Full Assembly Balanced Omni
    {
        "scad": os.path.join(MODELS_DIR, "full_assembly_balanced_omni.scad"),
        "png": os.path.join(MODELS_DIR, "preview_full_assembly_balanced_iso.png"),
        "camera": "0,85,60,55,0,25,450",
        "size": "1024,768"
    },
    {
        "scad": os.path.join(MODELS_DIR, "full_assembly_balanced_omni.scad"),
        "png": os.path.join(MODELS_DIR, "preview_full_assembly_balanced_top.png"),
        "camera": "0,85,60,0,0,0,380",
        "size": "1024,768"
    },
    {
        "scad": os.path.join(MODELS_DIR, "full_assembly_balanced_omni.scad"),
        "png": os.path.join(MODELS_DIR, "preview_full_assembly_balanced_front.png"),
        "camera": "0,85,35,90,0,0,380",
        "size": "1024,768"
    },
    # Chassis Base Balanced Omni
    {
        "scad": os.path.join(MODELS_DIR, "01_Chassis_Base_Balanced_Omni.scad"),
        "png": os.path.join(MODELS_DIR, "preview_chassis_balanced_iso.png"),
        "camera": "0,85,35,55,0,25,360",
        "size": "1024,768"
    },
    {
        "scad": os.path.join(MODELS_DIR, "01_Chassis_Base_Balanced_Omni.scad"),
        "png": os.path.join(MODELS_DIR, "preview_chassis_balanced_top.png"),
        "camera": "0,85,20,0,0,0,320",
        "size": "1024,768"
    }
]

for r in renders:
    t0 = time.time()
    cmd = [
        OPENSCAD_EXE,
        "-o", r["png"],
        "--camera=" + r["camera"],
        "--imgsize=" + r["size"],
        "--colorscheme=Tomorrow Night",
        r["scad"]
    ]
    print(f"Rendering {os.path.basename(r['png'])}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"  -> SUCCESS ({os.path.getsize(r['png']):,} bytes in {time.time() - t0:.1f}s)")
    else:
        print(f"  -> FAILED: {res.stderr[:200]}")

print("All renders completed.")
