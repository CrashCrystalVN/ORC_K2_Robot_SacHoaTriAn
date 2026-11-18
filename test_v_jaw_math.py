import numpy as np

# Derivation of V-Jaw Geometry for D=32mm cylinder (R=16mm)
# Let local jaw coordinate frame have pivot at (X_pivot, 0).
# For Left Jaw: pivot is at (-15, 0).
# For Right Jaw: pivot is at (+15, 0).
# Target tube position: Center at (0, Y_c).
# Let Y_c = 45.0 mm.

R_tube = 16.0 # mm

# For a symmetric 90-degree V-groove (included angle 2*beta = 90 deg, beta = 45 deg):
# Face 1: Rear slope at +45 deg to X axis
# Face 2: Front slope at -45 deg to X axis
# When clamping with jaws parallel (theta = 0):
# Contact point 1 (rear):
# Normal is at angle (-135 deg) from center of tube to contact point on left jaw:
# cp1_x = - R_tube * cos(45 deg) = -16.0 * 0.7071 = -11.314 mm
# cp1_y = Y_c - R_tube * sin(45 deg) = 45.0 - 11.314 = 33.686 mm
# Contact point 2 (front):
# cp2_x = - R_tube * cos(45 deg) = -11.314 mm
# cp2_y = Y_c + R_tube * sin(45 deg) = 45.0 + 11.314 = 56.314 mm
# Vertex of 90-degree V:
# v_x = - R_tube * sqrt(2) = -16.0 * 1.4142 = -22.627 mm
# v_y = Y_c = 45.0 mm

# What if the V-groove angle is 100 deg or 120 deg?
# Let 2*beta be included angle.
# Distance to vertex: d_v = R_tube / sin(beta)
# Normal angle: beta to the transverse axis.
for angle_deg in [75, 90, 105, 120]:
    beta = np.radians(angle_deg / 2.0)
    d_v = R_tube / np.sin(beta)
    cp_x = - R_tube * np.sin(beta)
    cp_dy = R_tube * np.cos(beta)
    v_x = - d_v
    print(f"Included Angle {angle_deg:3d} deg: Vertex depth X = {v_x:.2f} mm, Contact X = {cp_x:.2f} mm, Contact dY = +- {cp_dy:.2f} mm")
