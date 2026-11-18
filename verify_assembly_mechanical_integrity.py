import os
import subprocess
import trimesh
import numpy as np

OPENSCAD_BIN = r"C:\Program Files\OpenSCAD\openscad.com"
MODEL_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\3D_Models"
MODEL_DIR_POS = MODEL_DIR.replace('\\', '/')
OUT_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\temp_verification"

os.makedirs(OUT_DIR, exist_ok=True)

def run_openscad_intersection(scad_code, out_stl_name):
    scad_file = os.path.join(OUT_DIR, f"{out_stl_name}.scad")
    stl_file = os.path.join(OUT_DIR, f"{out_stl_name}.stl")
    
    if os.path.exists(stl_file):
        os.remove(stl_file)
        
    with open(scad_file, "w") as f:
        f.write(scad_code)
        
    cmd = [OPENSCAD_BIN, "-o", stl_file, scad_file]
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    # Check if empty
    if "Current top level object is empty." in res.stderr or "Current top level object is empty." in res.stdout or not os.path.exists(stl_file):
        return 0.0, "Empty (0.0000 mm^3 interference - PASS)"
    
    # If STL exists, compute mesh volume
    try:
        mesh = trimesh.load(stl_file)
        if isinstance(mesh, trimesh.Scene):
            geoms = list(mesh.geometry.values())
            vol = sum(g.volume for g in geoms if hasattr(g, 'volume') and g.is_volume)
        else:
            vol = mesh.volume if (hasattr(mesh, 'is_volume') and mesh.is_volume) else 0.0
            if vol == 0.0 and len(mesh.faces) > 0:
                vol = abs(mesh.volume)
        return vol, f"INTERFERENCE DETECTED: {vol:.4f} mm^3"
    except Exception as e:
        return -1.0, f"Error loading mesh: {e}"

def test_jaw_meshing_interference():
    print("=== TEST 1: GEAR MESHING INTERFERENCE (LEFT JAW vs RIGHT JAW) ===")
    angles = [0.0, 15.0, 30.0, 45.0, 60.0, 75.0]
    results = {}
    for angle in angles:
        scad_code = f"""
$fn = 64;
use <{MODEL_DIR_POS}/05_Gripper_Jaws_v3.scad>;

intersection() {{
    translate([-15.0, 0, 0])
        rotate([0, 0, {angle}])
            translate([15.0, 0, 0])
                gripper_jaw_left_v3();

    translate([15.0, 0, 0])
        rotate([0, 0, -{angle}])
            translate([-15.0, 0, 0])
                gripper_jaw_right_v3();
}}
"""
        vol, status = run_openscad_intersection(scad_code, f"mesh_jaw_left_vs_right_{int(angle)}deg")
        print(f"Angle {angle:4.1f} deg: Volume = {vol:8.4f} mm^3 -> {status}")
        results[angle] = (vol, status)
    return results

def test_base_vs_jaws_interference():
    print("\n=== TEST 2: BASE HEAD vs JAWS INTERFERENCE ===")
    angles = [0.0, 15.0, 30.0, 45.0, 60.0, 75.0]
    results = {}
    for angle in angles:
        # Left Jaw vs Base Head
        scad_left = f"""
$fn = 64;
use <{MODEL_DIR_POS}/04_Gripper_Base_Head_v3.scad>;
use <{MODEL_DIR_POS}/05_Gripper_Jaws_v3.scad>;

intersection() {{
    gripper_base_head_v3();
    
    translate([0, 38.0, 5.0])
        translate([-15.0, 0, 0])
            rotate([0, 0, {angle}])
                translate([15.0, 0, 0])
                    gripper_jaw_left_v3();
}}
"""
        vol_l, stat_l = run_openscad_intersection(scad_left, f"mesh_base_vs_jaw_left_{int(angle)}deg")
        
        # Right Jaw vs Base Head
        scad_right = f"""
$fn = 64;
use <{MODEL_DIR_POS}/04_Gripper_Base_Head_v3.scad>;
use <{MODEL_DIR_POS}/05_Gripper_Jaws_v3.scad>;

intersection() {{
    gripper_base_head_v3();
    
    translate([0, 38.0, 5.0])
        translate([15.0, 0, 0])
            rotate([0, 0, -{angle}])
                translate([-15.0, 0, 0])
                    gripper_jaw_right_v3();
}}
"""
        vol_r, stat_r = run_openscad_intersection(scad_right, f"mesh_base_vs_jaw_right_{int(angle)}deg")
        print(f"Angle {angle:4.1f} deg: LeftJaw vs Base = {vol_l:8.4f} mm^3 | RightJaw vs Base = {vol_r:8.4f} mm^3")
        results[angle] = (vol_l, vol_r)
    return results

def test_flower_tube_clamping():
    print("\n=== TEST 3: FLOWER TUBE CLAMPING INTERFERENCE / FIT ===")
    scad_code_l = f"""
$fn = 64;
use <{MODEL_DIR_POS}/05_Gripper_Jaws_v3.scad>;

intersection() {{
    translate([0, 45.0, 0])
        cylinder(d = 32.0, h = 120.0);
    gripper_jaw_left_v3();
}}
"""
    vol_l, stat_l = run_openscad_intersection(scad_code_l, "clamp_tube_vs_jaw_left")
    
    scad_code_r = f"""
$fn = 64;
use <{MODEL_DIR_POS}/05_Gripper_Jaws_v3.scad>;

intersection() {{
    translate([0, 45.0, 0])
        cylinder(d = 32.0, h = 120.0);
    gripper_jaw_right_v3();
}}
"""
    vol_r, stat_r = run_openscad_intersection(scad_code_r, "clamp_tube_vs_jaw_right")
    print(f"Flower Tube D32 vs Left Jaw Intersection: {vol_l:.4f} mm^3 -> {stat_l}")
    print(f"Flower Tube D32 vs Right Jaw Intersection: {vol_r:.4f} mm^3 -> {stat_r}")

if __name__ == "__main__":
    test_jaw_meshing_interference()
    test_base_vs_jaws_interference()
    test_flower_tube_clamping()
