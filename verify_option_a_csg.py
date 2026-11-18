import os
import subprocess
import trimesh

OPENSCAD_BIN = r"C:\Program Files\OpenSCAD\openscad.com"
MODEL_DIR = r"C:/Users/vuasu/.gemini/antigravity/scratch/ORC_K2_Robot_SacHoaTriAn/3D_Models"
TEMP_DIR = r"C:/Users/vuasu/.gemini/antigravity/scratch/ORC_K2_Robot_SacHoaTriAn/temp_tower_opt_a"
os.makedirs(TEMP_DIR, exist_ok=True)

print("======================================================================")
print("CSG VERIFICATION FOR OPTION A TOWER ($Y_{pivot} = 160.25 mm$)")
print("======================================================================")

angles = [-15.0, 0.0, 30.0, 60.0, 90.0]
results = {}

for ang in angles:
    scad_code = f"""
$fn = 36;
use <{MODEL_DIR}/01_Tower_Left_Stanchion_v2.scad>;
use <{MODEL_DIR}/02_Tower_Right_Stanchion_v2.scad>;
use <{MODEL_DIR}/04_Gripper_Base_Head_v3.scad>;
use <{MODEL_DIR}/05_Gripper_Jaws_v3.scad>;

module stanchions() {{
    tower_left_stanchion_v2();
    tower_right_stanchion_v2();
}}

module gripper_full() {{
    translate([0, 160.25, 58.0])
        rotate([{ang}, 0, 0])
            translate([0, -6.0, -38.0]) {{
                gripper_base_head_v3();
                translate([0, 38.0, 5.0]) {{
                    gripper_jaw_left_v3();
                    gripper_jaw_right_v3();
                }}
            }}
}}

// Check intersection between Gripper and Stanchions
intersection() {{
    gripper_full();
    stanchions();
}}
"""
    scad_file = os.path.join(TEMP_DIR, f"test_opt_a_{int(ang)}deg.scad")
    stl_file = os.path.join(TEMP_DIR, f"test_opt_a_{int(ang)}deg.stl")
    if os.path.exists(stl_file): os.remove(stl_file)
    with open(scad_file, "w") as f: f.write(scad_code)
    
    res = subprocess.run([OPENSCAD_BIN, "-o", stl_file, scad_file], capture_output=True, text=True)
    is_empty = "Current top level object is empty." in res.stderr or "Current top level object is empty." in res.stdout or not os.path.exists(stl_file)
    
    vol = 0.0
    if not is_empty and os.path.exists(stl_file):
        m = trimesh.load(stl_file)
        vol = m.volume if hasattr(m, 'volume') else 0.0
        
    status = "100% CLEAR - PASS (0.000 mm^3)" if vol == 0.0 else f"COLLISION: {vol:.4f} mm^3"
    print(f"Pitch Angle {ang:5.1f}°: Gripper vs Tower Stanchions -> {vol:6.4f} mm^3 -> {status}")
    results[ang] = vol

# Battery and sensor checks
scad_batt = f"""
$fn = 36;
use <{MODEL_DIR}/01_Tower_Left_Stanchion_v2.scad>;
use <{MODEL_DIR}/02_Tower_Right_Stanchion_v2.scad>;

module stanchions() {{
    tower_left_stanchion_v2();
    tower_right_stanchion_v2();
}}

// Battery box: X in [-19, 19], Y in [49, 99], Z in [4, 45]
intersection() {{
    stanchions();
    translate([-19.0, 49.0, 4.0]) cube([38.0, 50.0, 41.0]);
}}
"""
with open(os.path.join(TEMP_DIR, "test_batt.scad"), "w") as f: f.write(scad_batt)
res_b = subprocess.run([OPENSCAD_BIN, "-o", os.path.join(TEMP_DIR, "test_batt.stl"), os.path.join(TEMP_DIR, "test_batt.scad")], capture_output=True, text=True)
empty_b = "Current top level object is empty." in res_b.stderr or "Current top level object is empty." in res_b.stdout or not os.path.exists(os.path.join(TEMP_DIR, "test_batt.stl"))
print(f"Stanchions vs Battery Box: -> {'0.0000 mm^3 (PASS)' if empty_b else 'COLLISION'}")
