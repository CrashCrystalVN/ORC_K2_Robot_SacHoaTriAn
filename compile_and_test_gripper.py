import os
import sys
import subprocess
import time
import trimesh

OPENSCAD_BIN = r"C:\Program Files\OpenSCAD\openscad.exe"
WORKSPACE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
SCAD_LIB_FILE = os.path.join(WORKSPACE_DIR, "gripper_v2.scad")

TESTS = [
    {
        "name": "test_jaw_left",
        "scad_call": "use <gripper_v2.scad>;\nexport_jaw_left();\n",
        "desc": "Universal Hybrid Jaw Left V2 (m=1.5 Involute Gear, V-Groove, Serrations, I-Beam)"
    },
    {
        "name": "test_jaw_right",
        "scad_call": "use <gripper_v2.scad>;\nexport_jaw_right();\n",
        "desc": "Universal Hybrid Jaw Right V2 (MG996R Servo Horn Recess, m=1.5 Involute Gear, V-Groove)"
    },
    {
        "name": "test_gripper_base",
        "scad_call": "use <gripper_v2.scad>;\nexport_gripper_base();\n",
        "desc": "Gripper Base Head V2 (Pitch Clevis 90°, Servo S2 Bridge, Double-Shear M3 Posts)"
    },
    {
        "name": "test_gripper_assembly",
        "scad_call": "use <gripper_v2.scad>;\ngripper_v2_assembly(grip_angle = 0.0);\n",
        "desc": "Complete Gripper V2 Assembly (Closed 0.0°)"
    }
]

def compile_test(test):
    stl_name = test["name"] + ".stl"
    scad_name = test["name"] + ".scad"
    stl_path = os.path.join(WORKSPACE_DIR, stl_name)
    scad_path = os.path.join(WORKSPACE_DIR, scad_name)
    
    with open(scad_path, "w", encoding="utf-8") as f:
        f.write(test["scad_call"])
        
    print(f"=== Compiling {stl_name} with OpenSCAD ===")
    t0 = time.time()
    res = subprocess.run([OPENSCAD_BIN, "-o", stl_path, scad_path], capture_output=True, text=True)
    dt = time.time() - t0
    
    if res.returncode != 0:
        print(f"FAILED to compile {stl_name}! Exit code: {res.returncode}")
        print("STDERR:", res.stderr)
        return False
        
    print(f"Successfully compiled {stl_name} in {dt:.2f}s ({os.path.getsize(stl_path):,} bytes)")
    return True

def analyze_mesh(test):
    stl_name = test["name"] + ".stl"
    stl_path = os.path.join(WORKSPACE_DIR, stl_name)
    if not os.path.exists(stl_path):
        return {"file": stl_name, "error": "Not found"}
        
    mesh = trimesh.load(stl_path)
    # If assembly, it's expected to have multiple bodies (base + 2 jaws)
    is_assembly = "assembly" in test["name"]
    shells = mesh.split()
    bounds = mesh.bounds
    
    b_min = bounds[0]
    b_max = bounds[1]
    
    analysis = {
        "file": stl_name,
        "desc": test["desc"],
        "is_watertight": mesh.is_watertight,
        "is_volume": mesh.is_volume,
        "volume_mm3": round(float(mesh.volume), 2) if mesh.is_volume else 0.0,
        "num_shells": len(shells),
        "vertices": len(mesh.vertices),
        "faces": len(mesh.faces),
        "bounds_min": [round(x, 2) for x in b_min],
        "bounds_max": [round(x, 2) for x in b_max],
        "dx": round(float(b_max[0] - b_min[0]), 2),
        "dy": round(float(b_max[1] - b_min[1]), 2),
        "dz": round(float(b_max[2] - b_min[2]), 2),
        "z_min": round(float(b_min[2]), 2)
    }
    
    print(f"\n--- Topology Analysis for {stl_name} ---")
    print(f"  Description:   {analysis['desc']}")
    print(f"  Watertight:    {analysis['is_watertight']}")
    print(f"  Valid Volume:  {analysis['is_volume']} ({analysis['volume_mm3']} mm3)")
    print(f"  Shells count:  {analysis['num_shells']} {'(PASS: 1 shell)' if analysis['num_shells']==1 or is_assembly else '(FAIL: multiple shells)'}")
    print(f"  Z_min (PEI):   {analysis['z_min']} mm {'(PASS: 0.00mm flat bed)' if abs(analysis['z_min']) < 0.05 else '(FAIL: not on bed)'}")
    print(f"  Bounding Box:  X:[{b_min[0]:.1f}, {b_max[0]:.1f}], Y:[{b_min[1]:.1f}, {b_max[1]:.1f}], Z:[{b_min[2]:.1f}, {b_max[2]:.1f}]")
    print(f"  Dimensions:    {analysis['dx']} x {analysis['dy']} x {analysis['dz']} mm")
    
    return analysis

if __name__ == "__main__":
    results = []
    all_ok = True
    for t in TESTS:
        ok = compile_test(t)
        if not ok:
            all_ok = False
            continue
        res = analyze_mesh(t)
        results.append(res)
        
    print("\n================ SUMMARY ================")
    for r in results:
        status = "PASSED" if r["is_watertight"] and (r["num_shells"] == 1 or "assembly" in r["file"]) and abs(r["z_min"]) < 0.05 else "FAILED"
        print(f"[{status}] {r['file']}: Watertight={r['is_watertight']}, Shells={r['num_shells']}, Z_min={r['z_min']}mm, Vol={r.get('volume_mm3', 0)}mm3")
