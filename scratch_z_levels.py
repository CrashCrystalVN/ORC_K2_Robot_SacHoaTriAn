import trimesh
import numpy as np

m = trimesh.load("3D_Models/01_Chassis_Base_200x200.stl")

for z in [0.2, 1.0, 2.0, 3.5, 3.9, 4.0, 4.2, 5.0]:
    slice_2d = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    if slice_2d is None:
        continue
    entities = slice_2d.discrete
    tower_holes = []
    target_pts = [
        (-16.0, 110.5), (16.0, 110.5),
        (-24.0, 116.0), (24.0, 116.0),
        (-16.0, 122.0), (16.0, 122.0),
        (-24.0, 160.25), (24.0, 160.25),
        (-16.0, 160.25), (16.0, 160.25)
    ]
    for line in entities:
        min_pt = np.min(line, axis=0)
        max_pt = np.max(line, axis=0)
        c = (min_pt + max_pt) / 2.0
        sz = max_pt - min_pt
        for tx, ty in target_pts:
            if abs(c[0] - tx) < 1.0 and abs(c[1] - ty) < 1.0:
                tower_holes.append((tx, ty, sz[0], sz[1]))
                break
    print(f"\n--- Z = {z:.1f} mm: Matched {len(tower_holes)} / 10 tower holes ---")
    for th in sorted(tower_holes, key=lambda x: (x[1], x[0])):
        print(f"  Target ({th[0]:5.1f}, {th[1]:6.2f}) -> Hole size ({th[2]:.2f}, {th[3]:.2f})")
