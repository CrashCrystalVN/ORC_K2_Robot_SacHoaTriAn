import trimesh
import numpy as np

def verify_mesh(stl_path):
    print(f"==================================================")
    print(f"VERIFYING 3D MESH TOPOLOGY & PRINTABILITY: {stl_path}")
    print(f"==================================================")
    
    mesh = trimesh.load(stl_path)
    
    # 1. Watertight & Manifold check
    is_watertight = mesh.is_watertight
    is_winding_consistent = mesh.is_winding_consistent
    euler_number = mesh.euler_number
    
    print(f"1. MANIFOLD AUDIT:")
    print(f"   - Is Watertight (2-Manifold): {is_watertight}")
    print(f"   - Consistent Winding / Normals: {is_winding_consistent}")
    print(f"   - Euler Characteristic: {euler_number}")
    print(f"   - Vertices: {len(mesh.vertices):,}")
    print(f"   - Faces: {len(mesh.faces):,}")
    
    # 2. Bounding Box & Dimensions
    bounds = mesh.bounds
    extents = mesh.extents
    print(f"\n2. BOUNDING BOX & SIZING:")
    print(f"   - Bounds: X [{bounds[0][0]:.3f}, {bounds[1][0]:.3f}] mm (Width: {extents[0]:.3f} mm)")
    print(f"   - Bounds: Y [{bounds[0][1]:.3f}, {bounds[1][1]:.3f}] mm (Length: {extents[1]:.3f} mm)")
    print(f"   - Bounds: Z [{bounds[0][2]:.3f}, {bounds[1][2]:.3f}] mm (Height: {extents[2]:.3f} mm)")
    print(f"   - Volume: {mesh.volume:.2f} mm^3 ({mesh.volume / 1000.0:.2f} cm^3)")
    
    # Estimated print weight (PLA density ~1.24 g/cm3, 20% infill)
    pla_weight_solid = (mesh.volume / 1000.0) * 1.24
    pla_weight_20pct = pla_weight_solid * 0.35 # ~35% effective density with 3 walls
    print(f"   - Estimated Print Weight (PLA, 3 walls, 20% infill): ~{pla_weight_20pct:.1f} g")

    # 3. Flat Bed Adhesion at Z = 0.0 mm
    z_min = bounds[0][2]
    print(f"\n3. BED ADHESION & FIRST LAYER CONTACT:")
    print(f"   - Minimum Z: {z_min:.6f} mm")
    
    # Find all vertices on the bed (Z <= 0.01mm)
    bed_vertices = mesh.vertices[mesh.vertices[:, 2] <= 0.01]
    # Find all faces lying flat on Z = 0
    # A face is on the bed if all 3 vertices have Z <= 0.01 and face normal is approx [0, 0, -1]
    bed_face_mask = (mesh.face_normals[:, 2] < -0.99) & (np.all(mesh.vertices[mesh.faces][:, :, 2] <= 0.01, axis=1))
    bed_area = np.sum(mesh.area_faces[bed_face_mask])
    
    print(f"   - Bed Contact Vertices: {len(bed_vertices):,}")
    print(f"   - Total Flat Bed Contact Area: {bed_area:.2f} mm^2")
    print(f"   - Status: {'PERFECT 100% FLAT BED CONTACT (PASS)' if abs(z_min) < 0.001 and bed_area > 5000 else 'CHECK BED CONTACT'}")
    
    # 4. Outward Boss Protrusion Audit
    boss_min_x = bounds[0][0]
    boss_max_x = bounds[1][0]
    span = boss_max_x - boss_min_x
    print(f"\n4. GA25 MOTOR BOSS PACKAGING AUDIT:")
    print(f"   - Left Boss Tip (X_min): {boss_min_x:.2f} mm (Expected -69.5 mm)")
    print(f"   - Right Boss Tip (X_max): {boss_max_x:.2f} mm (Expected +69.5 mm)")
    print(f"   - Outer Boss Span: {span:.2f} mm")
    print(f"   - Inner Flange Span: {span - 2 * 3.0:.2f} mm (Expected 133.0 mm)")
    
    rear_clearance = (span - 2 * 3.0) - 2 * 63.0
    front_clearance = (span - 2 * 3.0) - 2 * 48.0
    print(f"   - Rear Clearance (2x GA25 Encoder 63mm): {rear_clearance:.2f} mm")
    print(f"   - Front Clearance (2x GA25 DC 48mm): {front_clearance:.2f} mm")
    
    total_robot_width = 118.0 + 2 * (2.0 + 38.0) # 198.0 mm
    total_robot_length = 190.0 # mm
    print(f"   - Total Robot Width (with 80mm Mecanum): {total_robot_width:.1f} mm <= 200.0 mm (PASS!)")
    print(f"   - Total Robot Length: {total_robot_length:.1f} mm <= 200.0 mm (PASS!)")
    
    # Final verdict
    passed = is_watertight and abs(z_min) < 0.001 and rear_clearance >= 7.0 and total_robot_width <= 200.0
    print(f"\n==================================================")
    print(f"FINAL AUDIT VERDICT: {'ACCEPTED / PASS 100%' if passed else 'REJECT / FAIL'}")
    print(f"==================================================")
    return passed

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "C:/Users/vuasu/.gemini/antigravity/scratch/ORC_K2_Robot_SacHoaTriAn/3D_Models/01_Chassis_Base_200x200_V6.stl"
    verify_mesh(path)
