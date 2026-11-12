import trimesh
import numpy as np

m = trimesh.load("3D_Models/01_Monocoque_Chassis_GA25_Mecanum.stl")
print("Bounds:", m.bounds.tolist())

# Note: Old base has Y in [-88, 88].
# Shift Y by +88.0:
# Y=110.5 -> y_old = 110.5 - 88 = 22.5
# Y=116.0 -> y_old = 116.0 - 88 = 28.0
# Y=122.0 -> y_old = 122.0 - 88 = 34.0
# Y=160.25 -> y_old = 160.25 - 88 = 72.25

slice_2d = m.section(plane_origin=[0, 0, 2.0], plane_normal=[0, 0, 1])
if slice_2d:
    entities = slice_2d.discrete
    print(f"Old Base: Contours at Z=2.0mm: {len(entities)}")
    holes = []
    for line in entities:
        min_pt = np.min(line, axis=0)
        max_pt = np.max(line, axis=0)
        c = (min_pt + max_pt) / 2.0
        sz = max_pt - min_pt
        if sz[0] < 10.0 and sz[1] < 10.0:
            holes.append((c[0], c[1], sz[0], sz[1]))
    holes.sort(key=lambda h: (round(h[1], 1), round(h[0], 1)))
    print(f"Holes in Old Base (size < 10mm): {len(holes)}")
    for h in holes:
        # print both centered Y and shifted Y (+88)
        print(f"  X={h[0]:6.2f}, Y_centered={h[1]:6.2f} (Y_shifted={h[1]+88.0:6.2f}) | size=({h[2]:.2f}, {h[3]:.2f})")
