import subprocess, os

test_scad = """
$fn = 40;

module involute_tooth_2d(m = 1.5, z = 20, pressure_angle = 20, backlash = 0.35) {
    rp = m * z / 2;
    rb = rp * cos(pressure_angle);
    ra = rp + 1.0 * m;
    rf = rp - 1.25 * m;
    
    jt = backlash / cos(pressure_angle);
    delta_s = jt / 2;
    psi_p = (180 / (2 * z)) - (delta_s / (2 * rp) * 180 / 3.14159265);
    inv_alpha = tan(pressure_angle) * 180 / 3.14159265 - pressure_angle;
    
    steps = 8;
    pts_r = [
        for (i = [0 : steps])
            let(r = rb + (ra - rb) * (i / steps),
                alpha_r = acos(rb / r),
                inv_ar = tan(alpha_r) * 180 / 3.14159265 - alpha_r,
                theta = psi_p + inv_alpha - inv_ar)
            [r * cos(theta), r * sin(theta)]
    ];
    
    theta_root = psi_p + inv_alpha;
    pt_root_r = [[rf * cos(theta_root), rf * sin(theta_root)]];
    
    right_side = concat(pt_root_r, pts_r);
    left_side = [ for (p = right_side) [p[0], -p[1]] ];
    left_rev = [ for (i = [len(left_side)-1 : -1 : 0]) left_side[i] ];
    
    polygon(points = concat(left_rev, right_side));
}

module sector_gear(is_left = true) {
    circle(r = 15.0 - 1.25 * 1.5);
    if (is_left) {
        for (a = [18, 0, -18, -36, -54, -72, -90, -108]) {
            rotate([0, 0, a]) involute_tooth_2d();
        }
    } else {
        for (a = [153, 171, 189, 207, 225, 243, 261, 279]) {
            rotate([0, 0, a]) involute_tooth_2d();
        }
    }
}

linear_extrude(height = 6) sector_gear(true);
"""

with open("test_gear.scad", "w", encoding="utf-8") as f:
    f.write(test_scad)

res = subprocess.run([r"C:\Program Files\OpenSCAD\openscad.exe", "-o", "test_gear.stl", "test_gear.scad"], capture_output=True, text=True)
print("Return code:", res.returncode)
if res.stderr:
    print("Stderr:", res.stderr)
if os.path.exists("test_gear.stl"):
    print("STL created! Size:", os.path.getsize("test_gear.stl"))
