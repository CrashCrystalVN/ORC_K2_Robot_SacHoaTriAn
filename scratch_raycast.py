import trimesh
import numpy as np

m = trimesh.load("3D_Models/01_Chassis_Base_200x200.stl")

coords = [
    # Left
    ("L1", -16.0, 110.5),
    ("L2", -16.0, 122.0),
    ("L3", -16.0, 160.25),
    ("L4", -24.0, 116.0),
    ("L5", -24.0, 160.25),
    # Right
    ("R1", 16.0, 110.5),
    ("R2", 16.0, 122.0),
    ("R3", 16.0, 160.25),
    ("R4", 24.0, 116.0),
    ("R5", 24.0, 160.25)
]

print("=== RAY CASTING AT HOLE CENTERS ===")
ray_origins = []
ray_directions = []
for name, x, y in coords:
    ray_origins.append([x, y, -5.0])
    ray_directions.append([0.0, 0.0, 1.0])

locations, index_ray, index_tri = m.ray.intersects_location(
    ray_origins=ray_origins,
    ray_directions=ray_directions
)

for i, (name, x, y) in enumerate(coords):
    hits = locations[index_ray == i]
    if len(hits) == 0:
        print(f"{name} ({x:5.1f}, {y:6.2f}): THROUGH HOLE (0 hits) - Completely Clear!")
    else:
        z_hits = sorted(hits[:, 2].tolist())
        print(f"{name} ({x:5.1f}, {y:6.2f}): BLOCKED! Hits at Z = {z_hits}")

print("\n=== SAMPLING NEARBY POINTS (to measure hole diameter) ===")
for name, cx, cy in coords:
    # check radius 1.0, 1.4, 1.7, 2.0 mm
    radii = [0.8, 1.2, 1.5, 1.6, 1.8, 2.5]
    clear_r = []
    for r in radii:
        all_clear = True
        for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
            px = cx + r * np.cos(angle)
            py = cy + r * np.sin(angle)
            hits, _, _ = m.ray.intersects_location(
                ray_origins=[[px, py, -5.0]],
                ray_directions=[[0.0, 0.0, 1.0]]
            )
            if len(hits) > 0:
                # check if hits floor Z in [0, 4]
                z_in_floor = [h[2] for h in hits if 0.0 <= h[2] <= 4.0]
                if len(z_in_floor) > 0:
                    all_clear = False
                    break
        if all_clear:
            clear_r.append(r)
    max_r = max(clear_r) if clear_r else 0.0
    print(f"{name} ({cx:5.1f}, {cy:6.2f}): Clear radius >= {max_r:.1f} mm (Clear Dia approx {2*max_r:.1f} mm)")
