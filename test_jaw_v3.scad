
 = 48;
GEAR_M = 1.5;
GEAR_Z = 20;
GEAR_RF = 13.125;
BACKLASH = 0.38;
PIVOT_X_LEFT = -15.0;
PIVOT_X_RIGHT = 15.0;
JAW_HEIGHT = 13.0;
JAW_LENGTH = 105.0;
PIN_HOLE_D = 3.4;
POST_BORE_D = 8.3;
POST_BORE_H = 9.5;
HUB_OUTER_R = 9.0;

module involute_tooth_2d(m = GEAR_M, z = GEAR_Z, bl = BACKLASH) {
    Rp = m * z / 2.0;
    Rb = Rp * cos(20.0);
    Ra = Rp + m;
    Rf = Rp - 1.25 * m;
    polygon(points = [
        [10.0 * cos(-7.0), 10.0 * sin(-7.0)],
        [Rf * cos(-5.5),   Rf * sin(-5.5)],
        [Rb * cos(-5.01),  Rb * sin(-5.01)],
        [14.5 * cos(-4.75), 14.5 * sin(-4.75)],
        [15.0 * cos(-4.14), 15.0 * sin(-4.14)],
        [15.5 * cos(-3.38), 15.5 * sin(-3.38)],
        [16.0 * cos(-2.48), 16.0 * sin(-2.48)],
        [Ra * cos(-1.46),  Ra * sin(-1.46)],
        [Ra * cos(1.46),   Ra * sin(1.46)],
        [16.0 * cos(2.48),  16.0 * sin(2.48)],
        [15.5 * cos(3.38),  15.5 * sin(3.38)],
        [15.0 * cos(4.14),  15.0 * sin(4.14)],
        [14.5 * cos(4.75),  14.5 * sin(4.75)],
        [Rb * cos(5.01),   Rb * sin(5.01)],
        [Rf * cos(5.5),    Rf * sin(5.5)],
        [10.0 * cos(7.0),  10.0 * sin(7.0)]
    ]);
}

module sector_gear_2d(is_left = true) {
    circle(r = GEAR_RF);
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

module gripper_jaw_v3(is_left = true) {
    pivot_x = is_left ? PIVOT_X_LEFT : PIVOT_X_RIGHT;
    sx = is_left ? -1.0 : 1.0;
    H = JAW_HEIGHT;
    H_gear = 7.5;

    difference() {
        union() {
            // 1. Hub
            translate([pivot_x, 0, 0]) {
                cylinder(r = HUB_OUTER_R, h = H);
            }
            // 2. Sector gear
            translate([pivot_x, 0, 0]) {
                linear_extrude(height = H_gear) {
                    sector_gear_2d(is_left = is_left);
                }
                // Transition chamfer
                translate([0, 0, H_gear])
                    cylinder(r1 = GEAR_RF, r2 = HUB_OUTER_R, h = 1.5);
            }
            // 3. Arm spine
            hull() {
                translate([pivot_x, 0, 0]) cylinder(r = HUB_OUTER_R, h = H);
                translate([sx * 18.0, 16.0, 0]) cylinder(r = 5.0, h = H);
            }
            hull() {
                translate([sx * 18.0, 14.0, 0]) cylinder(r = 5.0, h = H);
                translate([sx * 24.0, 36.0, 0]) cylinder(r = 5.0, h = H);
            }
            hull() {
                translate([sx * 24.0, 36.0, 0]) cylinder(r = 5.0, h = H);
                translate([sx * 23.0, 65.0, 0]) cylinder(r = 4.5, h = H);
            }
            hull() {
                translate([sx * 23.0, 65.0, 0]) cylinder(r = 4.5, h = H);
                translate([sx * 17.0, 88.0, 0]) cylinder(r = 4.0, h = H);
            }
            hull() {
                translate([sx * 17.0, 88.0, 0]) cylinder(r = 4.0, h = H);
                translate([sx * 10.0, JAW_LENGTH, 0]) cylinder(r = 3.5, h = H);
            }
            // Inner webbing
            hull() {
                translate([sx * 14.0, 20.0, 0]) cylinder(r = 3.5, h = H);
                translate([sx * 16.0, 50.0, 0]) cylinder(r = 3.5, h = H);
                translate([sx * 13.0, 80.0, 0]) cylinder(r = 3.5, h = H);
                translate([sx * 8.0, JAW_LENGTH - 5.0, 0]) cylinder(r = 3.0, h = H);
            }
            // Bottom retaining lip (3.2mm thick, slopes up)
            hull() {
                translate([sx * 8.5, 26.0, 0]) cylinder(r = 2.5, h = 3.0);
                translate([sx * 9.5, 65.0, 0]) cylinder(r = 2.5, h = 3.0);
                translate([sx * 5.5, JAW_LENGTH - 4.0, 0]) cylinder(r = 2.0, h = 3.0);
            }
            hull() {
                translate([sx * 8.5, 26.0, 3.0]) cylinder(r1 = 2.5, r2 = 0.8, h = 1.5);
                translate([sx * 9.5, 65.0, 3.0]) cylinder(r1 = 2.5, r2 = 0.8, h = 1.5);
                translate([sx * 5.5, JAW_LENGTH - 4.0, 3.0]) cylinder(r1 = 2.0, r2 = 0.8, h = 1.5);
            }
        }

        // Center split cut (leaves 4mm gap at 0 deg)
        if (is_left) {
            translate([-2.5, 12.0, -1.0]) cube([40.0, 130.0, H + 2.0]);
        } else {
            translate([-37.5, 12.0, -1.0]) cube([40.0, 130.0, H + 2.0]);
        }

        // Rear gear clearance
        translate([-12.0, 6.0, -1.0]) cube([24.0, 10.0, H + 2.0]);

        // Zone 1: D33mm flower tube cradle at Y = 36.0mm
        translate([0, 36.0, 3.0]) {
            cylinder(d = 33.0, h = H + 2.0);
            translate([0, 0, -1.0]) cylinder(d1 = 30.0, d2 = 33.0, h = 1.2);
        }

        // Zone 2: 90 deg V-groove at Y = 65.0mm
        translate([0, 65.0, 3.0]) {
            rotate([0, 0, 45]) cube([22.0, 22.0, H + 2.0], center = true);
        }

        // Zone 3: Serrated grip pads (4 ridges at Y = 82..98)
        for (ys = [82.0 : 4.0 : 98.0]) {
            translate([sx * 5.2, ys, -1.0])
                rotate([0, 0, sx * 45])
                    cube([2.0, 2.0, H + 2.0]);
        }

        // Front cut flat
        translate([-50.0, JAW_LENGTH, -1.0]) cube([100.0, 20.0, H + 2.0]);

        // Pivot post bore and pin hole
        translate([pivot_x, 0, -0.2]) cylinder(d = POST_BORE_D, h = POST_BORE_H);
        translate([pivot_x, 0, POST_BORE_H - 0.05])
            cylinder(d1 = POST_BORE_D, d2 = PIN_HOLE_D, h = (POST_BORE_D - PIN_HOLE_D) / 2.0);
        translate([pivot_x, 0, -1.0])
            cylinder(d = PIN_HOLE_D, h = H + 2.0);

        // Right jaw servo horn recess
        if (!is_left) {
            translate([pivot_x, 0, H - 2.8]) cylinder(d = 20.8, h = 3.2);
            translate([pivot_x - 4.1, -18.0, H - 2.8]) cube([8.2, 36.0, 3.2]);
            translate([pivot_x, 0, -1.0]) cylinder(d = 6.5, h = H + 2.0);
            for (a = [0 : 45 : 315]) {
                hx = pivot_x + 7.0 * cos(a);
                hy = 7.0 * sin(a);
                translate([hx, hy, -1.0]) cylinder(d = 2.9, h = H + 2.0);
            }
        }
    }
}

gripper_jaw_v3(is_left = true);
