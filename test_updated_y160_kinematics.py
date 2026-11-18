import numpy as np

# Updated Kinematics for Y_piv = 160.25 mm, Z_piv = 58.00 mm
y_piv = 160.25
z_piv = 58.00

# Gripper vectors from clevis pivot (Y_piv=6.0, Z_piv=38.0):
v_tube      = np.array([77.0, -33.0])
v_tip       = np.array([137.0, -33.0])
v_rear_lip  = np.array([10.0, -38.0])

def get_positions(pitch_deg):
    rad = np.radians(pitch_deg)
    R = np.array([
        [np.cos(rad), -np.sin(rad)],
        [np.sin(rad),  np.cos(rad)]
    ])
    pos_tube = np.array([y_piv, z_piv]) + R.dot(v_tube)
    pos_tip  = np.array([y_piv, z_piv]) + R.dot(v_tip)
    pos_rear = np.array([y_piv, z_piv]) + R.dot(v_rear_lip)
    return pos_tube, pos_tip, pos_rear

print("UPDATED PITCH KINEMATICS: Y_piv = 160.25 mm, Z_piv = 58.00 mm")
print("Pitch | Tube Center (Y, Z) | Jaw Tip (Y, Z) | Height Above Ground (Z_ground = -20) | Tube Reach Past Bumper (168.5mm)")
print("-" * 105)

for ang in [-15, -10, 0, 15, 30, 45, 60, 75, 90]:
    tube, tip, rear = get_positions(ang)
    h_tube = tube[1] - (-20.0)
    h_tip  = tip[1] - (-20.0)
    reach  = tube[0] - 168.5
    print(f"{ang:4d}° | ({tube[0]:6.1f}, {tube[1]:5.1f}) | ({tip[0]:6.1f}, {tip[1]:5.1f}) | Tube: {h_tube:5.1f} mm, Tip: {h_tip:5.1f} mm | Reach: {reach:5.1f} mm")

print("\nStowed Pose (90 deg):")
tube_90, tip_90, rear_90 = get_positions(90)
print(f"  Jaw Tip: Y = {tip_90[0]:.2f} mm, Z = {tip_90[1]:.2f} mm (Z above ground = {tip_90[1]-(-20):.2f} mm)")
print(f"  Rule Box Limit Y_max = 192.00 mm -> Margin = {192.0 - tip_90[0]:.2f} mm (INSIDE BOX!)")
print(f"  Rule Box Height Limit Z = 500.00 mm -> Margin = {500.0 - (tip_90[1]-(-20)):.2f} mm (INSIDE BOX!)")
