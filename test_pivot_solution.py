import os
import subprocess
import trimesh

OPENSCAD_BIN = r"C:\Program Files\OpenSCAD\openscad.com"
MODEL_DIR = r"C:/Users/vuasu/.gemini/antigravity/scratch/ORC_K2_Robot_SacHoaTriAn/3D_Models"
TEMP_DIR = r"C:/Users/vuasu/.gemini/antigravity/scratch/ORC_K2_Robot_SacHoaTriAn/temp_tower_verification"

# Test kinematic assembly if pivot is at Y = 160.25, Z = 58.0
# and stanchions slope backward from Y=160.25 to Y=105.0 (NO forward leg)
scad_test = f"""
$fn = 36;
use <{MODEL_DIR}/04_Gripper_Base_Head_v3.scad>;
use <{MODEL_DIR}/05_Gripper_Jaws_v3.scad>;

// Idealized A-frame stanchion with vertical/sloping-back column from Y=160.25 back to Y=105
module rear_braced_stanchions() {{
    for (sx = [-27.0, 19.0]) {{
        // Stanchion body: X in [sx, sx + 8.0]
        // Rear leg from Y=105 to Y=160.25
        hull() {{
            translate([sx, 105.0, 4.0]) cube([8.0, 20.0, 6.0]);
            translate([sx, 160.25 - 6.0, 58.0 - 12.0]) cube([8.0, 12.0, 24.0]);
        }}
        // Vertical front column at Y=160.25 (NOT extending past Y=160.25!)
        hull() {{
            translate([sx, 160.25 - 10.0, 4.0]) cube([8.0, 10.0, 6.0]);
            translate([sx, 160.25 - 6.0, 58.0 - 12.0]) cube([8.0, 12.0, 24.0]);
        }}
    }}
}}

module gripper_at_pitch(ang) {{
    translate([0, 160.25, 58.0])
        rotate([ang, 0, 0])
            translate([0, -6.0, -38.0]) {{
                gripper_base_head_v3();
                translate([0, 38.0, 5.0]) {{
                    gripper_jaw_left_v3();
                    gripper_jaw_right_v3();
                }}
            }}
}}

for (a = [-15, 0, 30, 60, 90]) {{
    // Check intersection
    intersection() {{
        gripper_at_pitch(a);
        rear_braced_stanchions();
    }}
}}
"""

with open(os.path.join(TEMP_DIR, "test_rear_braced.scad"), "w") as f:
    f.write(scad_test)

for ang in [-15, 0, 30, 60, 90]:
    single_scad = f"""
$fn = 36;
use <{MODEL_DIR}/04_Gripper_Base_Head_v3.scad>;
use <{MODEL_DIR}/05_Gripper_Jaws_v3.scad>;

module rear_braced_stanchions() {{
    for (sx = [-27.0, 19.0]) {{
        hull() {{
            translate([sx, 105.0, 4.0]) cube([8.0, 20.0, 6.0]);
            translate([sx, 160.25 - 6.0, 58.0 - 12.0]) cube([8.0, 12.0, 24.0]);
        }}
        hull() {{
            translate([sx, 160.25 - 10.0, 4.0]) cube([8.0, 10.0, 6.0]);
            translate([sx, 160.25 - 6.0, 58.0 - 12.0]) cube([8.0, 12.0, 24.0]);
        }}
    }}
}}

module gripper_at_pitch() {{
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

intersection() {{
    gripper_at_pitch();
    rear_braced_stanchions();
}}
"""
    scad_f = os.path.join(TEMP_DIR, f"test_rear_{ang}.scad")
    stl_f = os.path.join(TEMP_DIR, f"test_rear_{ang}.stl")
    if os.path.exists(stl_f): os.remove(stl_f)
    with open(scad_f, "w") as f: f.write(single_scad)
    res = subprocess.run([OPENSCAD_BIN, "-o", stl_f, scad_f], capture_output=True, text=True)
    is_empty = "Current top level object is empty." in res.stderr or "Current top level object is empty." in res.stdout or not os.path.exists(stl_f)
    vol = 0.0
    if not is_empty and os.path.exists(stl_f):
        m = trimesh.load(stl_f)
        vol = m.volume
    print(f"Angle {ang:3d} deg: Intersection volume = {vol:6.4f} mm^3 -> {'PASS (0.000 mm^3)' if vol == 0.0 else 'COLLISION'}")
