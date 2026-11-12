import trimesh
import numpy as np
import os

workspace = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
os.chdir(workspace)

old_base_path = "3D_Models/01_Monocoque_Chassis_GA25_Mecanum.stl"
tower_l_path = "3D_Models/01B_Lift_Tower_Left_FlatPrint.stl"
tower_r_path = "3D_Models/01C_Lift_Tower_Right_MG996R_FlatPrint.stl"
riser_path = "3D_Models/01D_Base_Riser_Frame.stl"

print("=== Old Base ===")
m_base = trimesh.load(old_base_path)
print("Bounds:", m_base.bounds.tolist())

# Let's inspect 01D_Base_Riser_Frame.scad if exists or stl
if os.path.exists(riser_path):
    m_riser = trimesh.load(riser_path)
    print("=== Riser Frame ===")
    print("Bounds:", m_riser.bounds.tolist())

# Let's inspect Tower Left & Right
if os.path.exists(tower_l_path):
    m_tl = trimesh.load(tower_l_path)
    print("=== Tower Left FlatPrint ===")
    print("Bounds:", m_tl.bounds.tolist())

# Let's check 01D_Base_Riser_Frame.scad
with open("3D_Models/01D_Base_Riser_Frame.scad", "r", encoding="utf-8") as f:
    print("=== 01D_Base_Riser_Frame.scad ===")
    print(f.read())
