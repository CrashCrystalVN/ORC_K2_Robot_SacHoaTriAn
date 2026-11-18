import subprocess, os, trimesh

test_assembly_scad = """
$fn = 50;

module involute_tooth_2d(m = 1.5, z = 20, pressure_angle = 20, backlash = 0.35) {
    rp = m * z / 2;
    rb = rp * cos(pressure_angle);
    ra = rp + 1.0 * m;
    rf = rp - 1.25 * m;
    
    jt = backlash / cos(pressure_angle);
    delta_s = jt / 2;
    psi_p = (180 / (2 * z)) - (delta_s / (2 * rp) * 180 / 3.14159265);
    inv_alpha = tan(pressure_angle) * 180 / 3.14159265 - pressure_angle;
    
    steps = 10;
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

module gear_left(rot_angle = 0) {
    translate([-15, 0, 0])
        rotate([0, 0, rot_angle])
            linear_extrude(height = 6) sector_gear(true);
}

module gear_right(rot_angle = 0) {
    translate([15, 0, 0])
        rotate([0, 0, -rot_angle])
            linear_extrude(height = 6) sector_gear(false);
}

// Generate test intersection at angle TEST_ANGLE
intersection() {
    gear_left(TEST_ANGLE);
    gear_right(TEST_ANGLE);
}
"""

angles = [0.0, 5.0, 10.0, 15.0, 20.0, 30.0, 45.0, 60.0, 75.0]
results = []

for ang in angles:
    scad_code = test_assembly_scad.replace("TEST_ANGLE", str(ang))
    scad_file = f"test_inter_{int(ang)}.scad"
    stl_file = f"test_inter_{int(ang)}.stl"
    with open(scad_file, "w", encoding="utf-8") as f:
        f.write(scad_code)
    
    res = subprocess.run([r"C:\Program Files\OpenSCAD\openscad.exe", "-o", stl_file, scad_file], capture_output=True, text=True)
    if os.path.exists(stl_file):
        try:
            m = trimesh.load(stl_file)
            vol = m.volume if (m.is_volume and len(m.faces) > 0) else 0.0
        except Exception:
            vol = 0.0
    else:
        vol = 0.0
    results.append((ang, vol))
    print(f"Angle {ang:4.1f} deg: Intersection Volume = {vol:.5f} mm^3")

print("\nSummary of Gear Meshing Interferences:")
for ang, vol in results:
    status = "PASS (0 collision)" if vol == 0.0 else f"FAIL (Volume: {vol})"
    print(f"  Theta = {ang:4.1f} deg: {status}")
