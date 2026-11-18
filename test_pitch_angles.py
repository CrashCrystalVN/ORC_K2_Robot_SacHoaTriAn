import numpy as np

# Detailed rotation analysis about Tower Pivot (Y_piv, Z_piv)
# Let's test Y_piv = 145.0 mm and Z_piv = 58.0 mm (matching standard tower hole Y=145, Z=58!)
# Or Y_piv = 135.5 mm (midpoint of stanchion foot)

# In Gripper V3 base head frame:
# Clevis pivot: (0, 6.0, 38.0)
# Jaw base plane: Z = 5.0 mm
# Jaw axles: (±15.0, 38.0, 5.0)
# Tube center: (0, 83.0, 5.0)
# Jaw tip: (±8.0, 143.0, 5.0)

# Local vector from clevis pivot (6.0, 38.0) in Gripper V3:
v_jaw_pivot = np.array([32.0, -33.0])
v_tube      = np.array([77.0, -33.0])
v_tip       = np.array([137.0, -33.0])
v_rear_lip  = np.array([10.0, -38.0]) # bottom rear of gripper base head (Y=16, Z=0) -> (16-6, 0-38) = (10, -38)
v_servo_top = np.array([38.0 - 6.0, 25.5 + 36.5 - 38.0]) # top of MG996R S2 -> (32.0, +24.0)

def get_positions(y_piv, z_piv, pitch_deg):
    rad = np.radians(pitch_deg)
    # Rotation matrix around X axis (Y -> Z):
    # [y_new] = [ cos(th)  -sin(th)] [y]
    # [z_new]   [ sin(th)   cos(th)] [z]
    # Note: Positive pitch rotates gripper UPWARDS (+Z, -Y)
    R = np.array([
        [np.cos(rad), -np.sin(rad)],
        [np.sin(rad),  np.cos(rad)]
    ])
    
    pos_tube = np.array([y_piv, z_piv]) + R.dot(v_tube)
    pos_tip  = np.array([y_piv, z_piv]) + R.dot(v_tip)
    pos_jaw_piv = np.array([y_piv, z_piv]) + R.dot(v_jaw_pivot)
    pos_rear = np.array([y_piv, z_piv]) + R.dot(v_rear_lip)
    pos_top  = np.array([y_piv, z_piv]) + R.dot(v_servo_top)
    
    return {
        "tube": pos_tube,
        "tip": pos_tip,
        "jaw_piv": pos_jaw_piv,
        "rear": pos_rear,
        "top": pos_top
    }

print("PITCH SIMULATION: Y_piv = 140.0 mm, Z_piv = 58.0 mm")
print("Pitch Angle | Tube (Y, Z) | Jaw Tip (Y, Z) | Height Above Ground (Z_ground = -20)")
print("-" * 75)

for ang in [-25, -20, -15, -10, 0, 15, 30, 45, 60, 75, 90]:
    pts = get_positions(140.0, 58.0, ang)
    tube = pts["tube"]
    tip = pts["tip"]
    h_tube_ground = tube[1] - (-20.0)
    h_tip_ground = tip[1] - (-20.0)
    print(f"{ang:10d}° | ({tube[0]:6.1f}, {tube[1]:5.1f}) | ({tip[0]:6.1f}, {tip[1]:5.1f}) | Tube: {h_tube_ground:5.1f} mm, Tip: {h_tip_ground:5.1f} mm")
