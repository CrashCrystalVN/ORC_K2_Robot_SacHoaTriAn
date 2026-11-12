import trimesh
import numpy as np

m = trimesh.load("3D_Models/01_Chassis_Base_200x200.stl")

slice_2d = m.section(plane_origin=[0, 0, 2.0], plane_normal=[0, 0, 1])
if slice_2d is not None:
    entities = slice_2d.discrete
    print(f"Total contours at Z=2.0mm: {len(entities)}")
    
    # Check bounding box of each contour to find holes
    holes = []
    for line in entities:
        min_pt = np.min(line, axis=0)
        max_pt = np.max(line, axis=0)
        center = (min_pt + max_pt) / 2.0
        size = max_pt - min_pt
        if size[0] < 10.0 and size[1] < 10.0:
            holes.append((center[0], center[1], size[0], size[1]))
            
    print(f"Small holes found (size < 10mm): {len(holes)}")
    # Sort by Y then X
    holes.sort(key=lambda h: (round(h[1], 1), round(h[0], 1)))
    for h in holes:
        print(f"  Hole at X={h[0]:6.2f}, Y={h[1]:6.2f} | size=({h[2]:.2f}, {h[3]:.2f})")
