import os
import subprocess
import time

WORKSPACE = r"c:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
OPENSCAD_BIN = r"C:\Program Files\OpenSCAD\openscad.exe"
MODELS_DIR = os.path.join(WORKSPACE, "3D_Models")
SCAD_LIB = os.path.join(MODELS_DIR, "gripper_v3_mg996r.scad")

RENDERS = [
    {
        "name": "preview_gripper_v3_closed_0deg_iso.png",
        "scad": f'''
use <{SCAD_LIB}>;
$fn = 64;
gripper_v3_assembly(grip_angle = 0.0);
''',
        "camera": "0,70,60,60,0,35,420", # eye x,y,z, rot x,y,z, dist
        "desc": "Gripper V3 Assembly - Closed 0.0° (Ultra-Compact Width 58mm)"
    },
    {
        "name": "preview_gripper_v3_open_45deg_iso.png",
        "scad": f'''
use <{SCAD_LIB}>;
$fn = 64;
gripper_v3_assembly(grip_angle = 45.0);
''',
        "camera": "0,70,60,60,0,35,420",
        "desc": "Gripper V3 Assembly - Open 45.0° (Total 90° Opening, Tip Gap 177mm)"
    },
    {
        "name": "preview_gripper_v3_open_90deg_iso.png",
        "scad": f'''
use <{SCAD_LIB}>;
$fn = 64;
gripper_v3_assembly(grip_angle = 90.0);
''',
        "camera": "0,70,60,60,0,35,420",
        "desc": "Gripper V3 Assembly - Folded Transverse 90.0° (Forward Reach reduced to 16.5mm)"
    },
    {
        "name": "preview_gripper_v3_top_comparison.png",
        "scad": f'''
use <{SCAD_LIB}>;
$fn = 64;

// Left: Closed 0 deg
translate([-120, 0, 0]) {{
    gripper_v3_assembly(grip_angle = 0.0);
}}

// Center: Open 45 deg (Total 90 deg)
translate([0, 0, 0]) {{
    gripper_v3_assembly(grip_angle = 45.0);
}}

// Right: Open 90 deg (Sideways flat)
translate([140, 0, 0]) {{
    gripper_v3_assembly(grip_angle = 90.0);
}}
''',
        "camera": "10,70,120,0,0,0,650", # Top-down view
        "desc": "Gripper V3 - Top View Comparison: Closed 0° vs Open 45° (Total 90°) vs Folded 90°"
    }
]

def render_preview(r):
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
    print(f"--> Rendering {r['name']} ...")
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    dt = time.time() - t0
    
    if res.returncode != 0:
        print(f"FAILED to render {r['name']}: {res.stderr}")
        return False
        
    size_kb = os.path.getsize(out_png) / 1024.0
    print(f"    Rendered {r['name']} in {dt:.2f}s ({size_kb:.1f} KB)")
    try:
        os.remove(scad_tmp)
    except:
        pass
    return True

def main():
    print("====================================================================")
    print("BAT DAU RENDER HINH ANH PHOI CANH 3D CO CAU KEP V3.0 (MG996R)")
    print("====================================================================")
    for r in RENDERS:
        render_preview(r)
    print("HOAN TAT RENDER ANH PREVIEW!")

if __name__ == "__main__":
    main()
