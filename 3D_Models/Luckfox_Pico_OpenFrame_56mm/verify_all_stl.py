import trimesh
import os
import numpy as np

dir_path = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\3D_Models\Luckfox_Pico_OpenFrame_56mm"

parts = [
    ("01A_Luckfox_OpenFrame_UnderMount_56mm", "UnderMount Base 56mm"),
    ("01B_Luckfox_OpenFrame_BackMount_56mm", "BackMount Base 56mm (Primary)"),
    ("02A_Rod_Clamp_Dual_Bar_56mm", "Rod Clamp UnderMount Dual Bar"),
    ("02B_Rod_Clamp_BackMount_56mm", "Rod Clamp BackMount"),
    ("03_Luckfox_PCB_Top_Retainer", "Luckfox PCB Top Retainer"),
    ("04_VL53L5CX_V2_Sensor_Bracket", "VL53L5CX V2 Sensor Bracket"),
]

print("="*75)
print("TRIMESH VERIFICATION REPORT FOR ALL RENDERED STLS")
print("="*75)

all_passed = True

for fname, title in parts:
    stl_path = os.path.join(dir_path, fname + ".stl")
    if not os.path.exists(stl_path):
        print(f"FAILED: File {fname}.stl does not exist!")
        all_passed = False
        continue
    
    mesh = trimesh.load(stl_path)
    
    # Check watertightness
    is_watertight = mesh.is_watertight
    
    # Check volume
    volume_mm3 = mesh.volume if is_watertight else 0.0
    
    # Check bounds (min/max X, Y, Z)
    min_b, max_b = mesh.bounds[0], mesh.bounds[1]
    dimensions = max_b - min_b
    
    # Check if seated flat on Z=0
    z_min_seated = abs(min_b[2]) < 1e-3
    
    print(f"\n[{fname}] ({title})")
    print(f"  Watertight (solid closed mesh): {'PASS (100% Manifold)' if is_watertight else 'FAIL'}")
    print(f"  Faces / Vertices: {len(mesh.faces)} faces / {len(mesh.vertices)} vertices")
    print(f"  Volume: {volume_mm3:,.1f} mm3")
    print(f"  Bounding Box [X, Y, Z]:")
    print(f"    X: [{min_b[0]:.2f}, {max_b[0]:.2f}] (span = {dimensions[0]:.2f} mm)")
    print(f"    Y: [{min_b[1]:.2f}, {max_b[1]:.2f}] (span = {dimensions[1]:.2f} mm)")
    print(f"    Z: [{min_b[2]:.2f}, {max_b[2]:.2f}] (span = {dimensions[2]:.2f} mm)")
    print(f"  Seated Flat on Z=0: {'PASS (Z_min = 0.00mm)' if z_min_seated else f'FAIL (Z_min = {min_b[2]:.3f}mm)'}")

    if not is_watertight or not z_min_seated or volume_mm3 <= 0:
        all_passed = False

print("\n" + "="*75)
print(f"OVERALL TRIMESH STATUS: {'ALL PARTS 100% PASSED' if all_passed else 'SOME PARTS FAILED'}")
print("="*75)
