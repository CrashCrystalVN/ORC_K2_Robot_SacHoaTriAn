import trimesh
import numpy as np

m = trimesh.load("3D_Models/01_Chassis_Base_200x200.stl")

# Check if points at Z=4.5 are inside mesh (solid)
test_pts = [
    [-16.0, 110.5, 4.5],
    [ 16.0, 110.5, 4.5],
    [-24.0, 116.0, 4.5],
    [ 24.0, 116.0, 4.5],
    [-16.0, 122.0, 4.5],
    [ 16.0, 122.0, 4.5],
    [-24.0, 160.25, 4.5],
    [ 24.0, 160.25, 4.5],
    [-16.0, 160.25, 4.5],
    [ 16.0, 160.25, 4.5],
]

# trimesh contains check
inside = m.contains(test_pts)
print("Points inside solid at Z=4.5 mm:", inside)
for pt, ins in zip(test_pts, inside):
    print(f"Pt ({pt[0]:5.1f}, {pt[1]:6.2f}, {pt[2]:.1f}): {'SOLID (BLOCKED!)' if ins else 'OPEN AIR (CLEAR)'}")
