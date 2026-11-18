import numpy as np

m = 1.5
z = 20
alpha_deg = 20.0
backlash = 0.35

alpha = np.radians(alpha_deg)
rp = m * z / 2.0
rb = rp * np.cos(alpha)
ra = rp + 1.0 * m
rf = rp - 1.25 * m

jt = backlash / np.cos(alpha)
delta_s = jt / 2.0
psi_p = (np.pi / (2 * z)) - (delta_s / (2 * rp))
inv_alpha = np.tan(alpha) - alpha

radii = np.linspace(rb, ra, 50)
pts_r = []
for r in radii:
    ar = np.arccos(rb / r)
    inv_ar = np.tan(ar) - ar
    th = psi_p + inv_alpha - inv_ar
    pts_r.append((r * np.cos(th), r * np.sin(th)))

th_root = psi_p + inv_alpha
pt_root_r = [(rf * np.cos(th_root), rf * np.sin(th_root))]
right_side = pt_root_r + pts_r
left_side = [(x, -y) for x, y in reversed(right_side)]
one_tooth = np.array(left_side + right_side)

# Left gear teeth at [18, 0, -18, -36, -54, -72, -90, -108]
# Right gear teeth at [153, 171, 189, 207, 225, 243, 261, 279]
angles_l = [18, 0, -18, -36, -54, -72, -90, -108]
angles_r = [153, 171, 189, 207, 225, 243, 261, 279]

def get_gear_points(angles, is_left=True, rot=0.0):
    all_pts = []
    for a in angles:
        net_a = a + (rot if is_left else -rot)
        rad = np.radians(net_a)
        ca, sa = np.cos(rad), np.sin(rad)
        rot_tooth = np.column_stack([
            one_tooth[:, 0] * ca - one_tooth[:, 1] * sa,
            one_tooth[:, 0] * sa + one_tooth[:, 1] * ca
        ])
        center = np.array([-15.0, 0.0]) if is_left else np.array([15.0, 0.0])
        all_pts.append(rot_tooth + center)
    return np.vstack(all_pts)

for ang in [0.0, 5.0, 9.0, 15.0, 18.0, 25.0, 35.0, 45.0, 60.0, 75.0]:
    pts_l = get_gear_points(angles_l, is_left=True, rot=ang)
    pts_r = get_gear_points(angles_r, is_left=False, rot=ang)
    
    # Filter points near meshing zone (|X| < 10, |Y| < 10)
    mask_l = (np.abs(pts_l[:, 0]) < 8.0) & (np.abs(pts_l[:, 1]) < 8.0)
    mask_r = (np.abs(pts_r[:, 0]) < 8.0) & (np.abs(pts_r[:, 1]) < 8.0)
    
    sub_l = pts_l[mask_l]
    sub_r = pts_r[mask_r]
    
    # Distance matrix
    diff = sub_l[:, None, :] - sub_r[None, :, :]
    dist = np.sqrt(np.sum(diff**2, axis=-1))
    min_dist = np.min(dist)
    print(f"Angle {ang:4.1f} deg: Min Clearance between teeth = {min_dist:.4f} mm")
