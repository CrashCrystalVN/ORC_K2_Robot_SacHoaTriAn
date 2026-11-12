import os
import sys
import subprocess
import time
import trimesh
import numpy as np

WORKSPACE = r"c:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
OPENSCAD_BIN = r"C:\Program Files\OpenSCAD\openscad.exe"
MODELS_DIR = os.path.join(WORKSPACE, "3D_Models")
SCAD_LIB = os.path.join(MODELS_DIR, "gripper_v3_mg996r.scad")

PARTS = [
    {
        "name": "04_Gripper_Base_Head_V3",
        "scad": f'use <{SCAD_LIB}>;\nexport_gripper_base_v3();\n',
        "desc": "Gripper Base Head V3 (MG996R S2 Elevated Cantilever Truss Bridge, Wrist Clevis 90° S3 & 4xM3 Mounting)",
        "is_part": True
    },
    {
        "name": "05_Gripper_Jaw_Left_V3",
        "scad": f'use <{SCAD_LIB}>;\nexport_jaw_left_v3();\n',
        "desc": "Gripper Jaw Left V3 (m=1.5 Involute Gear Sector 0-90°, D32 Cradle, 90° V-Groove, Serrations)",
        "is_part": True
    },
    {
        "name": "06_Gripper_Jaw_Right_V3",
        "scad": f'use <{SCAD_LIB}>;\nexport_jaw_right_v3();\n',
        "desc": "Gripper Jaw Right V3 (MG996R 25T Disc Horn Recess, m=1.5 Gear Sector 0-90°, D32 Cradle)",
        "is_part": True
    },
    {
        "name": "Gripper_V3_Assembly_Closed_0deg",
        "scad": f'use <{SCAD_LIB}>;\ngripper_v3_assembly(grip_angle = 0.0);\n',
        "desc": "Complete Gripper V3 Assembly - Closed State 0.0° (Ultra-Compact Width 60mm)",
        "is_part": False
    },
    {
        "name": "Gripper_V3_Assembly_Open_45deg",
        "scad": f'use <{SCAD_LIB}>;\ngripper_v3_assembly(grip_angle = 45.0);\n',
        "desc": "Complete Gripper V3 Assembly - Open State 45.0° (Total 90° Wide Opening, Tip Gap > 175mm)",
        "is_part": False
    },
    {
        "name": "Gripper_V3_Assembly_Open_90deg",
        "scad": f'use <{SCAD_LIB}>;\ngripper_v3_assembly(grip_angle = 90.0);\n',
        "desc": "Complete Gripper V3 Assembly - Transverse Folded 90.0° (Forward Reach reduced to 50mm)",
        "is_part": False
    }
]

def compile_part(p):
    stl_path = os.path.join(MODELS_DIR, p["name"] + ".stl")
    scad_tmp = os.path.join(MODELS_DIR, p["name"] + ".scad")
    with open(scad_tmp, "w", encoding="utf-8") as f:
        f.write(p["scad"])
    
    print(f"--> Compiling {p['name']}.stl ...")
    t0 = time.time()
    res = subprocess.run([OPENSCAD_BIN, "-o", stl_path, scad_tmp], capture_output=True, text=True)
    dt = time.time() - t0
    
    if res.returncode != 0:
        print(f"FAILED to compile {p['name']}.stl! Exit code: {res.returncode}")
        print("STDERR:", res.stderr)
        return False, None
    
    size_kb = os.path.getsize(stl_path) / 1024.0
    print(f"    Compiled successfully in {dt:.2f}s ({size_kb:.1f} KB)")
    return True, stl_path

def analyze_mesh(p, stl_path):
    mesh = trimesh.load(stl_path)
    b_min, b_max = mesh.bounds
    dx = float(b_max[0] - b_min[0])
    dy = float(b_max[1] - b_min[1])
    dz = float(b_max[2] - b_min[2])
    z_min = float(b_min[2])
    
    shells = len(mesh.split())
    vol = float(mesh.volume) if mesh.is_volume else 0.0
    
    info = {
        "name": p["name"],
        "desc": p["desc"],
        "watertight": mesh.is_watertight,
        "is_volume": mesh.is_volume,
        "volume_mm3": round(vol, 1),
        "shells": shells,
        "vertices": len(mesh.vertices),
        "faces": len(mesh.faces),
        "dx": round(dx, 2),
        "dy": round(dy, 2),
        "dz": round(dz, 2),
        "z_min": round(z_min, 2),
        "bounds": [list(np.round(b_min, 2)), list(np.round(b_max, 2))]
    }
    return info

def main():
    print("====================================================================")
    print("BAT DAU BIEN DICH VA KIEM TRA CO CAU KEP GRIPPER V3.0 (MG996R)")
    print("====================================================================")
    results = []
    for p in PARTS:
        ok, stl_path = compile_part(p)
        if not ok:
            print(f"STOPPING due to error in {p['name']}")
            return
        info = analyze_mesh(p, stl_path)
        results.append(info)
        
    print("\n================ KET QUA PHAN TICH HINH HOC 3D ================")
    for r in results:
        status = "PASS" if r["watertight"] or ("Assembly" in r["name"]) else "WARN"
        print(f"[{status}] {r['name']}:")
        print(f"    Mo ta:     {r['desc']}")
        print(f"    Kich thuoc: {r['dx']} x {r['dy']} x {r['dz']} mm")
        print(f"    The tich:  {r['volume_mm3']} mm3 | Watertight: {r['watertight']} | Shells: {r['shells']}")
        print(f"    PEI Z_min: {r['z_min']} mm")

if __name__ == "__main__":
    main()
