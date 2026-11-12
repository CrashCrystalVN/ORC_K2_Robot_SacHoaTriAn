import trimesh
import os
import glob

workspace = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
os.chdir(workspace)

files = [
    "01_Monocoque_Chassis_GA25_Mecanum.stl",
    "3D_Models/01_Chassis_Base_200x200.stl",
    "3D_Models/01_Chassis_Base_200x200_V6.stl"
]

for f in files:
    if os.path.exists(f):
        m = trimesh.load(f)
        print(f"=== {f} ===")
        print("Bounds:", m.bounds.tolist())
        print("Watertight:", m.is_watertight)
        print("Volume:", m.volume)
    else:
        print(f"File not found: {f}")
