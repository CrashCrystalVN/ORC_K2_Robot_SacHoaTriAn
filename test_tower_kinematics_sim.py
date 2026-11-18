import numpy as np

# Let's write a script to simulate the pitch kinematics
# Coordinates of Gripper Base Head V3 relative to its clevis pivot (Y_piv=6.0, Z_piv=38.0):
# In Gripper V3 local frame:
# Clevis Pivot: (0, 6.0, 38.0)
# Jaw Pivot Axles: (±15.0, 38.0, 5.0)
# Tube Center (when clamped): (0, 38.0 + 45.0, 5.0) = (0, 83.0, 5.0)
# Jaw Tips: (±8.0, 38.0 + 105.0, 5.0) = (±8.0, 143.0, 5.0)
# Base Head Rear bulk: (0, 16.0, 0.0)

# Relative vectors from Clevis Pivot (0, 6.0, 38.0):
vec_jaw_pivot = np.array([0.0, 38.0 - 6.0, 5.0 - 38.0])   # (0, 32.0, -33.0)
vec_tube_center = np.array([0.0, 83.0 - 6.0, 5.0 - 38.0]) # (0, 77.0, -33.0)
vec_jaw_tip = np.array([0.0, 143.0 - 6.0, 5.0 - 38.0])    # (0, 137.0, -33.0)

# Pitch rotation: angle theta_pitch around X axis
# Let theta_pitch = 0 be the nominal horizontal gripping pose.
# In nominal pose, the jaw base floor is horizontal (parallel to XY plane).
# In this pose:
# relative vectors are exactly vec_jaw_pivot, vec_tube_center, vec_jaw_tip.

# If the tower pivot is placed at (Y_tower_piv, Z_tower_piv) in robot coordinates:
# Then:
# pos_tube = (Y_tower_piv + dy, Z_tower_piv + dz)

# Ground is at Z = -20.0 mm in chassis coordinates.
# Chassis floor top is at Z = 4.0 mm.
# Front bumper is at Y = 168.5 mm.

print(f"Vector from Clevis Pivot to Tube Center: dY = {vec_tube_center[1]:.1f} mm, dZ = {vec_tube_center[2]:.1f} mm")
print(f"Vector from Clevis Pivot to Jaw Tip:     dY = {vec_jaw_tip[1]:.1f} mm, dZ = {vec_jaw_tip[2]:.1f} mm")

# Let's test various candidate tower pivot locations:
# On the chassis, tower bolt holes span Y in [110.5, 160.25].
# The center of the stanchion base is around Y = 135.5 mm.
# If tower pivot is at Y_piv = 135.0 mm:
for y_piv in [125.0, 130.0, 135.0, 140.0, 145.0]:
    for z_piv in [55.0, 60.0, 65.0, 70.0, 75.0, 80.0]:
        # At theta_pitch = 0 (horizontal):
        y_tube = y_piv + vec_tube_center[1]
        z_tube = z_piv + vec_tube_center[2] # jaw floor level
        # Tube clearance from ground (ground is Z = -20):
        h_ground = z_tube - (-20.0)
        # Jaw tip Y:
        y_tip = y_piv + vec_jaw_tip[1]
        
        # Check conditions:
        # 1. y_tube must be in front of bumper (y_tube > 168.5 + 16.0 = 184.5 mm)
        # 2. h_ground must be between 10mm and 40mm (so tube bottom is near ground)
        if y_tube >= 190.0 and 15.0 <= h_ground <= 45.0:
            print(f"Candidate: Y_piv={y_piv:.1f}, Z_piv={z_piv:.1f} -> Y_tube={y_tube:.1f} mm (Tip at {y_tip:.1f} mm), Height above ground={h_ground:.1f} mm")
