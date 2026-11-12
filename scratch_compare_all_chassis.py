import trimesh
import numpy as np
import glob
import os

workspace = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
os.chdir(workspace)

chassis_stls = [
    "3D_Models/01_Chassis_Base_200x200.stl",
    "3D_Models/01_Chassis_Base_200x200_V6.stl",
    "3D_Models/01_Chassis_Lower_Base.stl",
    "3D_Models/01_K2_Chassis_Base_GA25_Mecanum.stl",
    "3D_Models/01_Monocoque_Chassis_GA25_Mecanum.stl"
]

target_pts = [
    (-16.0, 110.5), (16.0, 110.5),
    (-24.0, 116.0), (24.0, 116.0),
    (-16.0, 122.0), (16.0, 122.0),
    (-24.0, 160.25), (24.0, 160.25),
    (-16.0, 160.25), (16.0, 160.25)
]

for stl_path in chassis_stls:
    if not os.path.exists(stl_path):
        continue
    m = trimesh.load(stl_path)
    b = m.bounds
    # Determine Y offset
    # If Y bounds start near -88, shift is +88
    # If Y bounds start near 0, shift is 0
    y_shift = 88.0 if b[0][1] < -50 else 0.0
    
    slice_2 = m.section(plane_origin=[0, 0, 2.0], plane_normal=[0, 0, 1])
    if slice_2 is None:
        print(f"{stl_path}: cannot slice at Z=2.0")
        continue
    entities = slice_2.discrete
    matched = 0
    matched_pts = []
    for line in entities:
        min_p = np.min(line, axis=0)
        max_p = np.max(line, axis=0)
        c = (min_p + max_p) / 2.0
        cx = c[0]
        cy = c[1] + y_shift
        for tx, ty in target_pts:
            if abs(cx - tx) < 1.2 and abs(cy - ty) < 1.2:
                matched += 1
                matched_pts.append((tx, ty))
                break
    print(f"=== {stl_path} ===")
    print(f"  Bounds: X in [{b[0][0]:.1f}, {b[1][0]:.1f}], Y in [{b[0][1]:.1f}, {b[1][1]:.1f}], Z in [{b[0][2]:.1f}, {b[1][2]:.1f}]")
    print(f"  Matched tower holes at Z=2.0mm: {matched} / 10")
