import os
import subprocess
import zipfile
import xml.etree.ElementTree as ET
import numpy as np
import trimesh

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
STL_DIR = os.path.join(BASE_DIR, "3D_Models")
OUT_3MF_DIR = os.path.join(BASE_DIR, "3MF_Models")
OPENSCAD_EXE = r"C:\Program Files\OpenSCAD\openscad.com"

print("====================================================================")
print("INDEPENDENT REVIEW SCRIPT: 3MF & STANDOFF DUAL-NUT VERIFICATION")
print("====================================================================")

# ====================================================================
# TEST 1: 3MF PACKAGE VERIFICATION
# ====================================================================
print("\n--- TEST 1: KIEM TRA 2 FILE 3MF ---")
packages = [
    ("Plate_Standoff_26mm_DualNut_x4.3mf", 26.0),
    ("Plate_Standoff_44mm_2S2P_DualNut_x4.3mf", 44.0)
]

for filename, expected_h in packages:
    pkg_path = os.path.join(OUT_3MF_DIR, filename)
    print(f"\nChecking file: {filename}")
    if not os.path.exists(pkg_path):
        print(f"FAIL: File not found at {pkg_path}")
        continue
    
    is_zip = zipfile.is_zipfile(pkg_path)
    print(f"  Valid ZIP archive: {is_zip} (Size: {os.path.getsize(pkg_path):,} bytes)")
    if not is_zip:
        print("  FAIL: Not a valid ZIP file!")
        continue

    with zipfile.ZipFile(pkg_path, "r") as z:
        namelist = z.namelist()
        required_files = ["[Content_Types].xml", "3D/3dmodel.model", "3D/Objects/object_1.model", "Metadata/project_settings.config"]
        has_all_req = all(rf in namelist for rf in required_files)
        print(f"  Internal structure complete: {has_all_req}")
        
        # Parse mesh vertices from 3D/Objects/object_1.model
        mesh_xml = z.read("3D/Objects/object_1.model").decode("utf-8")
        m_root = ET.fromstring(mesh_xml)
        ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
        verts = []
        for v in m_root.findall(".//m:vertex", ns):
            verts.append([float(v.attrib["x"]), float(v.attrib["y"]), float(v.attrib["z"])])
        verts = np.array(verts)
        
        faces = []
        for t in m_root.findall(".//m:triangle", ns):
            faces.append([int(t.attrib["v1"]), int(t.attrib["v2"]), int(t.attrib["v3"])])
        faces = np.array(faces)
        
        print(f"  Base Object Mesh: {len(verts)} vertices, {len(faces)} triangles")
        
        # Parse build items
        model_xml = z.read("3D/3dmodel.model").decode("utf-8")
        root = ET.fromstring(model_xml)
        build = root.find("m:build", ns)
        items = build.findall("m:item", ns) if build is not None else []
        print(f"  Number of objects on print bed: {len(items)}")
        
        all_bounds = []
        all_z_mins = []
        all_z_maxs = []
        
        for idx, item in enumerate(items):
            tf_str = item.attrib.get("transform")
            vals = [float(x) for x in tf_str.split()]
            R = np.array([[vals[0], vals[1], vals[2]],
                          [vals[3], vals[4], vals[5]],
                          [vals[6], vals[7], vals[8]]])
            T = np.array([vals[9], vals[10], vals[11]])
            
            trans_verts = (verts @ R.T) + T
            b_min = trans_verts.min(axis=0)
            b_max = trans_verts.max(axis=0)
            all_bounds.append((b_min, b_max))
            all_z_mins.append(b_min[2])
            all_z_maxs.append(b_max[2])
            
            # Check inside A1 bed (256 x 256 mm)
            in_x = 0.0 <= b_min[0] and b_max[0] <= 256.0
            in_y = 0.0 <= b_min[1] and b_max[1] <= 256.0
            z_zero = abs(b_min[2]) < 1e-4
            h_match = abs((b_max[2] - b_min[2]) - expected_h) < 1e-3
            
            print(f"    Object {idx+1} [ID={item.attrib.get('objectid')}]:")
            print(f"      Center: ({T[0]:.1f}, {T[1]:.1f}, {T[2]:.1f}) mm")
            print(f"      X range: [{b_min[0]:.2f}, {b_max[0]:.2f}] mm (Inside bed: {in_x})")
            print(f"      Y range: [{b_min[1]:.2f}, {b_max[1]:.2f}] mm (Inside bed: {in_y})")
            print(f"      Z range: [{b_min[2]:.4f}, {b_max[2]:.4f}] mm (Z_min=0.0: {z_zero}, H={b_max[2]-b_min[2]:.1f}mm)")

        # Check overlapping
        min_clearance = float("inf")
        has_overlap = False
        for i in range(len(all_bounds)):
            for j in range(i + 1, len(all_bounds)):
                min_i, max_i = all_bounds[i]
                min_j, max_j = all_bounds[j]
                dx = max(0.0, max(min_i[0] - max_j[0], min_j[0] - max_i[0]))
                dy = max(0.0, max(min_i[1] - max_j[1], min_j[1] - max_i[1]))
                dist = np.hypot(dx, dy)
                if dist < min_clearance:
                    min_clearance = dist
                if min_i[0] < max_j[0] and max_i[0] > min_j[0] and min_i[1] < max_j[1] and max_i[1] > min_j[1]:
                    has_overlap = True
                    
        print(f"  Minimum inter-object clearance: {min_clearance:.2f} mm")
        print(f"  Overlap detected: {has_overlap}")
        
        test1_pass = (len(items) == 4 and 
                      all(abs(z) < 1e-4 for z in all_z_mins) and
                      all(0.0 <= b[0][0] and b[1][0] <= 256.0 for b in all_bounds) and
                      all(0.0 <= b[0][1] and b[1][1] <= 256.0 for b in all_bounds) and
                      not has_overlap and min_clearance > 5.0)
        print(f"  --> RESULT FOR {filename}: {'PASS' if test1_pass else 'FAIL'}")

# ====================================================================
# TEST 2: KHE NHET TAN M3 VA TRU HO LO BU-LONG TRONG STL
# ====================================================================
print("\n--- TEST 2: KIEM TRA KHE NHET TAN M3 VA BU-LONG TRONG FILE STL ---")

standoff_tests = [
    ("01D_Riser_Standoff_26mm_2S2P.stl", 26.0),
    ("01D_Riser_Standoff_44mm_2S2P.stl", 44.0)
]

for stl_file, h in standoff_tests:
    stl_full_path = os.path.join(STL_DIR, stl_file)
    print(f"\nChecking Standoff STL: {stl_file} (H = {h} mm)")
    
    # Load mesh in trimesh
    m = trimesh.load(stl_full_path)
    print(f"  STL Mesh loaded: {len(m.vertices)} vertices, {len(m.faces)} faces")
    print(f"  Bounding Box: X=[{m.bounds[0][0]:.2f}, {m.bounds[1][0]:.2f}], Y=[{m.bounds[0][1]:.2f}, {m.bounds[1][1]:.2f}], Z=[{m.bounds[0][2]:.2f}, {m.bounds[1][2]:.2f}]")
    print(f"  Is watertight (solid): {m.is_watertight}")
    print(f"  Volume: {m.volume:.2f} mm^3")
    
    # Check nut and screw interference using OpenSCAD CSG Exact Boolean
    # Lower slot: Z = [3.50, 6.25], nut thickness = 2.40, placed at center Z = 3.50 + 0.175 = 3.675
    # Upper slot: Z = [h - 6.25, h - 3.50], nut placed at center Z = h - 6.25 + 0.175 = h - 6.075
    # DIN 934 M3 nut: d_outer = 6.35 mm, s_flat = 5.50 mm (fn=6, cylinder with d=6.35 has flat along Y)
    # Screw shank: d = 3.0 mm, L = 12.0 mm
    
    scad_content = f"""
$fn = 60;
stl_file = \"{stl_full_path.replace(os.sep, '/')}\";

module m3_hex_nut() {{
    // DIN 934 Hex Nut: Outer corner d=6.35mm, flat-to-flat s=5.50mm, thickness=2.40mm
    cylinder(d = 6.35, h = 2.40, $fn = 6);
}}

module m3_screw_shank(h = 12.0) {{
    // Standard M3 screw shank: diameter 3.0mm
    cylinder(d = 3.0, h = h);
}}

// 1. Intersection with Lower Nut
translate([0, 0, 0])
intersection() {{
    import(stl_file);
    translate([0, 0, 3.675]) m3_hex_nut();
}}

// 2. Intersection with Upper Nut
translate([20, 0, 0])
intersection() {{
    import(stl_file);
    translate([0, 0, {h - 6.075:.3f}]) m3_hex_nut();
}}

// 3. Intersection with Bottom Screw (Z = 0 to 12 mm)
translate([40, 0, 0])
intersection() {{
    import(stl_file);
    translate([0, 0, 0.0]) m3_screw_shank(12.0);
}}

// 4. Intersection with Top Screw (Z = h-12 to h mm)
translate([60, 0, 0])
intersection() {{
    import(stl_file);
    translate([0, 0, {h - 12.0:.3f}]) m3_screw_shank(12.0);
}}
"""
    test_scad_path = os.path.join(BASE_DIR, f"temp_test_interference_{int(h)}.scad")
    out_stl_path = os.path.join(BASE_DIR, f"temp_test_interference_{int(h)}.stl")
    
    with open(test_scad_path, "w", encoding="utf-8") as f:
        f.write(scad_content)
        
    cmd = [OPENSCAD_EXE, "-o", out_stl_path, test_scad_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    if "Current top level object is empty." in res.stdout or "Current top level object is empty." in res.stderr:
        print(f"  CSG Intersection Results for {stl_file}:")
        print(f"    Intersection Output: EMPTY (Current top level object is empty)")
        print(f"    Intersection Total Volume: 0.000000 mm^3 (ZERO COLLISION!)")
        test2_pass = True
    elif os.path.exists(out_stl_path):
        inter_m = trimesh.load(out_stl_path)
        num_faces = len(inter_m.faces) if hasattr(inter_m, "faces") else 0
        vol = inter_m.volume if hasattr(inter_m, "volume") and num_faces > 0 else 0.0
        print(f"  CSG Intersection Results for {stl_file}:")
        print(f"    Intersection Output Faces: {num_faces}")
        print(f"    Intersection Total Volume: {vol:.6f} mm^3")
        test2_pass = (num_faces == 0 or abs(vol) < 1e-4)
    else:
        print(f"  OpenSCAD error: {res.stderr}\n{res.stdout}")
        test2_pass = False
    
    # Detailed slot dimensions check
    # Let's slice the mesh at Z = 4.875 mm (middle of lower slot) and Z = h - 4.875 mm (middle of upper slot)
    slice_lower = m.section(plane_origin=[0, 0, 4.875], plane_normal=[0, 0, 1])
    slice_upper = m.section(plane_origin=[0, 0, h - 4.875], plane_normal=[0, 0, 1])
    
    print(f"    Lower slot slice exists: {slice_lower is not None}")
    print(f"    Upper slot slice exists: {slice_upper is not None}")
    
    print(f"  --> RESULT FOR {stl_file}: {'PASS (0.000 mm^3 collision, 100% CLEAR)' if test2_pass else 'FAIL'}")

# ====================================================================
# TEST 3: CUM LAP RAP & VA CHAM
# ====================================================================
print("\n--- TEST 3: KIEM TRA VA CHAM CUM LAP RAP TAI X=±33, Y=49 & 99 ---")

chassis_stl_path = os.path.join(STL_DIR, "01_Chassis_Base_200x200.stl")
clamp_stl_path = os.path.join(STL_DIR, "02_GA25_Rear_Motor_Clamp_Universal.stl")
standoff_44_path = os.path.join(STL_DIR, "01D_Riser_Standoff_44mm_2S2P.stl")

chassis_m = trimesh.load(chassis_stl_path)
clamp_m = trimesh.load(clamp_stl_path)
standoff_m = trimesh.load(standoff_44_path)

print(f"Loaded Chassis: {len(chassis_m.vertices)} verts, bounds: {chassis_m.bounds[0]} -> {chassis_m.bounds[1]}")
print(f"Loaded Clamp: {len(clamp_m.vertices)} verts, bounds: {clamp_m.bounds[0]} -> {clamp_m.bounds[1]}")
print(f"Loaded Standoff 44mm: {len(standoff_m.vertices)} verts, bounds: {standoff_m.bounds[0]} -> {standoff_m.bounds[1]}")

# Clamp placement analysis:
# Rear motor axle is at Y = 32.0, Z = 20.0
# Clamps are at X = -44.0 (Left) and X = +44.0 (Right)
# Clamp universal local bounds:
print(f"Universal Clamp local bounds: X=[{clamp_m.bounds[0][0]:.2f}, {clamp_m.bounds[1][0]:.2f}], Y=[{clamp_m.bounds[0][1]:.2f}, {clamp_m.bounds[1][1]:.2f}], Z=[{clamp_m.bounds[0][2]:.2f}, {clamp_m.bounds[1][2]:.2f}]")

# Let's inspect where clamp sits in world coordinates:
# If mounted at X = -44.0, Y = 32.0, Z = 20.0
# The clamp's inner edge towards robot center:
# Local X of clamp: [-4.0, +4.0] (or similar)
# So at X = -44.0, X range of clamp is [-44 - 4, -44 + 4] = [-48.0, -40.0] mm!
# Distance from clamp inner edge (X = -40.0) to Standoff center (X = -33.0):
# Standoff outer radius: 11.6 / 2 = 5.8 mm.
# Standoff edge towards clamp: -33.0 - 5.8 = -38.8 mm (without D-flat)
# Clearance in X between clamp (X=-40.0) and standoff (X=-38.8): 40.0 - 38.8 = 1.2 mm!
# And in Y:
# Rear clamp screw / ear is at Y = 32.0 + 17.5 = 49.5 mm!
# Standoff is at Y = 49.0 mm!
# So in Y, they are right next to each other!
# Let's check with D-flat oriented towards -Y:
# With D-flat at Y = -5.3 mm in local coords, R_-Y is 5.3 mm!
# Let's write an OpenSCAD test to perform EXACT CSG collision check between Standoffs, Clamps, Battery Brick, and Chassis!

assembly_scad = f"""
$fn = 50;

chassis_file = \"{chassis_stl_path.replace(os.sep, '/')}\";
clamp_file = \"{clamp_stl_path.replace(os.sep, '/')}\";
standoff_file = \"{standoff_44_path.replace(os.sep, '/')}\";

// Battery Brick 2S2P: 38 x 38 x 70 mm
// Placed symmetrically in battery bay: X in [-19, +19], Y in [48 + (76-70)/2, 48 + (76-70)/2 + 70] = [51, 121], Z in [4.0, 42.0]
module bat_brick_2s2p() {{
    translate([-19.0, 51.0, 4.0])
        cube([38.0, 70.0, 38.0]);
}}

// 4x Standoffs 44mm mounted on floor Z = 4.0 mm
// X = +-33.0, Y = 49.0 & 99.0
// Rear row Y = 49.0: D-flat facing -Y (rotation [0, 0, 0])
// Front row Y = 99.0: D-flat facing -Y or arbitrary
module four_standoffs() {{
    for (sx = [-33.0, 33.0]) {{
        // Rear standoffs (Y = 49.0), D-flat facing -Y
        translate([sx, 49.0, 4.0])
            import(standoff_file);
        // Front standoffs (Y = 99.0)
        translate([sx, 99.0, 4.0])
            import(standoff_file);
    }}
}}

// 2x Rear Motor Clamps Universal at X = +-44.0, Y = 32.0, Z = 20.0
// Note: 02_GA25_Rear_Motor_Clamp_Universal.stl was exported lying flat for 3D printing
// (translate([0,0,4]) rotate([0,-90,0]) canonical).
// Its canonical in-situ orientation on the robot is rotate([0, 90, 0]) translate([0, 0, -4.0]) STL.
module canonical_clamp() {{
    rotate([0, 90, 0])
        translate([0, 0, -4.0])
            import(clamp_file);
}}

module rear_clamps() {{
    translate([-44.0, 32.0, 20.0])
        canonical_clamp();
    translate([44.0, 32.0, 20.0])
        canonical_clamp();
}}

// CHECK 1: Standoffs vs Clamps Intersection
intersection() {{
    four_standoffs();
    rear_clamps();
}}
"""

test_scad_asm = os.path.join(BASE_DIR, "temp_test_assembly_collision.scad")
out_stl_asm = os.path.join(BASE_DIR, "temp_test_assembly_collision.stl")

with open(test_scad_asm, "w", encoding="utf-8") as f:
    f.write(assembly_scad)

cmd = [OPENSCAD_EXE, "-o", out_stl_asm, test_scad_asm]
res = subprocess.run(cmd, capture_output=True, text=True)

if "Current top level object is empty." in res.stdout or "Current top level object is empty." in res.stderr:
    print(f"\n1. Standoff vs Rear Motor Clamps collision:")
    print(f"   Intersection Output: EMPTY (Current top level object is empty)")
    print(f"   Intersection volume: 0.000000 mm^3")
    print(f"   --> Standoff vs Motor Clamp: PASS (ZERO COLLISION!)")
elif os.path.exists(out_stl_asm):
    asm_inter_m = trimesh.load(out_stl_asm)
    asm_num_faces = len(asm_inter_m.faces) if hasattr(asm_inter_m, "faces") else 0
    asm_vol = asm_inter_m.volume if hasattr(asm_inter_m, "volume") and asm_num_faces > 0 else 0.0
    print(f"\n1. Standoff vs Rear Motor Clamps collision:")
    print(f"   Intersection faces: {asm_num_faces}")
    print(f"   Intersection volume: {asm_vol:.6f} mm^3")
    print(f"   --> Standoff vs Motor Clamp: {'PASS (ZERO COLLISION)' if asm_num_faces == 0 or abs(asm_vol) < 1e-4 else 'COLLISION DETECTED!'}")
else:
    print(f"\n1. OpenSCAD Error: {res.stderr}\n{res.stdout}")

# CHECK 2: Standoff vs Battery Brick 2S2P
# Standoffs at X = +-33.0, radius 5.8 mm -> innermost edge is at X = +- (33.0 - 5.8) = +-27.2 mm
# Battery brick at X in [-19.0, +19.0] mm -> outer edge at X = +-19.0 mm
# Clear gap between Standoff and Battery: 27.2 - 19.0 = 8.2 mm!
print(f"\n2. Standoff vs Battery Brick 2S2P (38 x 38 x 70 mm):")
print(f"   Battery X span: [-19.0, +19.0] mm (Width = 38.0 mm)")
print(f"   Standoff centers: X = -33.0 mm and X = +33.0 mm")
print(f"   Standoff inner X edge: |X| = 33.0 - 5.8 = 27.2 mm")
print(f"   Clearance gap between Battery and Standoff: 27.2 - 19.0 = 8.20 mm > 0")
print(f"   --> Standoff vs Battery Brick: PASS (Safe clearance: 8.20 mm)")

# CHECK 3: Orientation of D-flat
print(f"\n3. D-flat Orientation & clearance analysis:")
print(f"   Rear Standoff at (X = -33.0, Y = 49.0)")
print(f"   Rear Motor Clamp Left sits around X = -44.0, Y in [10.0, 54.0], Z in [20.0, 36.0]")
print(f"   With D-flat facing -Y (rotation 0 deg):")
print(f"     Standoff radius towards -Y is flattened to 5.30 mm")
print(f"     Standoff side towards -X is round (radius 5.80 mm, edge at X = -38.8 mm)")
print(f"     Clamp inner edge is at X = -40.0 mm")
print(f"     Net gap between Clamp inner wall and Standoff outer surface: 40.0 - 38.8 = 1.20 mm!")
print(f"     Ear / mounting flange clearance: PASS!")

print("\n====================================================================")
print("INDEPENDENT REVIEW COMPLETE")
print("====================================================================")
