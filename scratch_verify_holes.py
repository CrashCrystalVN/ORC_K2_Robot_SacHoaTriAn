import trimesh
import numpy as np

m = trimesh.load("3D_Models/01_Chassis_Base_200x200.stl")

# 10 tower holes
coords = [
    # Left
    (-16.0, 110.5), (-16.0, 122.0), (-16.0, 160.25),
    (-24.0, 116.0), (-24.0, 160.25),
    # Right
    (16.0, 110.5), (16.0, 122.0), (16.0, 160.25),
    (24.0, 116.0), (24.0, 160.25)
]

print("=== CHECKING 10 TOWER HOLES IN 01_Chassis_Base_200x200.stl ===")
# Let's slice horizontally at Z = 0.5, 2.0, 3.5, 4.0, 5.0 mm
for z in [0.5, 2.0, 3.8, 4.2]:
    slice_2d = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    if slice_2d is None:
        print(f"Z={z}: No slice")
        continue
    polys = slice_2d.to_planar()[0].polygons_full
    print(f"\n--- Z = {z} mm (Found {len(polys)} outer polygons) ---")
    
    # For each coordinate, test if it is contained in a hole (interior ring) or outside
    for x, y in coords:
        # Check point containment in slice
        # In planar, polygon has exterior and interiors
        inside_solid = False
        inside_hole = False
        for poly in polys:
            p = trimesh.path.polygons.Point(x, y)
            if poly.contains(p):
                # Point is inside polygon outline, but could be in a hole
                # shapely poly contains returns False if inside an interior hole!
                inside_solid = True
            elif poly.exterior.contains(p):
                # inside exterior but outside poly -> inside hole!
                inside_hole = True
        
        status = "SOLID" if inside_solid else ("HOLE" if inside_hole else "OUTSIDE/VOID")
        print(f"Point ({x:5.1f}, {y:6.2f}): {status}")
