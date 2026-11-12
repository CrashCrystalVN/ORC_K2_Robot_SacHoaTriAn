import trimesh
import numpy as np

m = trimesh.load("3D_Models/01_Chassis_Base_200x200.stl")

slice_5 = m.section(plane_origin=[0, 0, 5.0], plane_normal=[0, 0, 1])
if slice_5:
    print("Number of contours at Z=5.0mm:", len(slice_5.discrete))
    for i, line in enumerate(slice_5.discrete):
        min_pt = np.min(line, axis=0)
        max_pt = np.max(line, axis=0)
        sz = max_pt - min_pt
        print(f"Contour {i}: X in [{min_pt[0]:.1f}, {max_pt[0]:.1f}], Y in [{min_pt[1]:.1f}, {max_pt[1]:.1f}], sz=({sz[0]:.1f}, {sz[1]:.1f})")
