import os, subprocess, struct, collections

scad_text = """$fn = 64;

module involute_tooth_2d(m = 1.5, z = 20, backlash = 0.36) {
    Rp = m * z / 2;
    Rb = Rp * cos(20);
    Ra = Rp + m;
    Rf = Rp - 1.25 * m;

    polygon(points = [
        [10.0 * cos(-7.0), 10.0 * sin(-7.0)],
        [Rf * cos(-5.5),   Rf * sin(-5.5)],
        [Rb * cos(-5.01),  Rb * sin(-5.01)],
        [14.5 * cos(-4.75), 14.5 * sin(-4.75)],
        [15.0 * cos(-4.16), 15.0 * sin(-4.16)],
        [15.5 * cos(-3.38), 15.5 * sin(-3.38)],
        [16.0 * cos(-2.48), 16.0 * sin(-2.48)],
        [Ra * cos(-1.46),  Ra * sin(-1.46)],
        // Tip
        [Ra * cos(1.46),   Ra * sin(1.46)],
        // Left flank
        [16.0 * cos(2.48),  16.0 * sin(2.48)],
        [15.5 * cos(3.38),  15.5 * sin(3.38)],
        [15.0 * cos(4.16),  15.0 * sin(4.16)],
        [14.5 * cos(4.75),  14.5 * sin(4.75)],
        [Rb * cos(5.01),   Rb * sin(5.01)],
        [Rf * cos(5.5),    Rf * sin(5.5)],
        [10.0 * cos(7.0),  10.0 * sin(7.0)]
    ]);
}

module sector_gear(is_left = true, h = 6.0) {
    linear_extrude(height = h) {
        circle(r = 13.125);
        if (is_left) {
            for (a = [-18, 0, 18, 36, 54]) {
                rotate([0, 0, a]) involute_tooth_2d();
            }
        } else {
            for (a = [135, 153, 171, 189]) {
                rotate([0, 0, a]) involute_tooth_2d();
            }
        }
    }
}

// Assemble pair
translate([-15, 0, 0]) sector_gear(is_left = true, h = 6.0);
translate([15, 0, 0])  sector_gear(is_left = false, h = 6.0);
"""

with open("test_gears.scad", "w", encoding="utf-8") as f:
    f.write(scad_text)

res = subprocess.run([r"C:\Program Files\OpenSCAD\openscad.exe", "-o", "test_gears.stl", "test_gears.scad"], capture_output=True, text=True)
print("Return code:", res.returncode)
print("STDERR:", res.stderr)
print("STL exists:", os.path.exists("test_gears.stl"))
if os.path.exists("test_gears.stl"):
    print("STL size:", os.path.getsize("test_gears.stl"))
