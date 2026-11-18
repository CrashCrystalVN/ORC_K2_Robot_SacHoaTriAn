import numpy as np

# Comparative Analysis of V-Jaw Profiles for Ø32mm Cylinder
# Profile 1: Classical 90-degree Straight V-Groove
# Profile 2: Curved Gothic Arch / Bi-Radial V-Groove (R_arc = 20mm, centers offset)
# Profile 3: Hybrid V-Jaw with Entrance Funnel Lead-in (Lead-in angle 30-40 deg)

R_tube = 16.0 # mm

# In Profile 2: Each flank is a circular arc of radius R_arc > R_tube.
# Let R_arc = 22.0 mm.
# Two arcs centered at (X_c1, Y_c1) and (X_c2, Y_c2).
# When the cylinder R=16 sits at (0, Y_c), it touches both arcs tangentially.
# The distance between cylinder center and arc center must be |R_arc - R_tube| = 22 - 16 = 6.0 mm.
# To have 45-degree contact normals (identical to a 90-deg V):
# Center of rear arc: X_c1 = -6.0 * cos(45 deg) = -4.24 mm, Y_c1 = Y_c - 6.0 * sin(45 deg) = Y_c - 4.24 mm
# Center of front arc: X_c2 = -6.0 * cos(45 deg) = -4.24 mm, Y_c2 = Y_c + 6.0 * sin(45 deg) = Y_c + 4.24 mm

print("Profile 2 (Curved Gothic Arch):")
print(f"  Arc Radius R_arc = 22.0 mm")
print(f"  Arc 1 Center (Rear):  X = {-6.0 * np.cos(np.pi/4):.3f} mm, dY = {-6.0 * np.sin(np.pi/4):.3f} mm")
print(f"  Arc 2 Center (Front): X = {-6.0 * np.cos(np.pi/4):.3f} mm, dY = {+6.0 * np.sin(np.pi/4):.3f} mm")
print(f"  Contact points at (X = {-16.0*np.cos(np.pi/4):.3f}, dY = +- {16.0*np.sin(np.pi/4):.3f}) mm")
print(f"  Vertex cusp blend at X = - {4.24 + 22.0:.3f} = -26.24 mm")
