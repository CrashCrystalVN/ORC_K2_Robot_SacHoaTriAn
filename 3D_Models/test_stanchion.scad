$fn = 48;

module left_stanchion() {
    difference() {
        union() {
            // Column main body in (Y, Z) extruded along X from -27 to -19 (thickness 8mm)
            translate([-19.0, 0, 0])
            rotate([0, -90, 0])
            linear_extrude(height = 8.0) {
                difference() {
                    polygon(points = [
                        // Rear base
                        [4.0, 105.0],
                        [10.0, 105.0],
                        // Rear leg rising towards pivot (Y=140, Z=58)
                        [50.0, 131.0],
                        // Crown around pivot (Y=140, Z=58, R=9)
                        [58.0, 131.0],
                        [64.5, 133.5],
                        [67.0, 140.0],
                        [64.5, 146.5],
                        [58.0, 149.0],
                        [50.0, 149.0],
                        // Front leg down to base
                        [10.0, 166.0],
                        [4.0, 166.0]
                    ]);
                    // Central lightening window
                    polygon(points = [
                        [12.0, 122.0],
                        [12.0, 151.0],
                        [46.0, 140.0]
                    ]);
                }
            }

            // Inward Foot Pads (from X = -19.0 to -13.0, width 6.0mm, height Z = 4.0 .. 10.0)
            // Rear foot pad (Y in [105.0, 126.0])
            translate([-19.0, 105.0, 4.0]) cube([6.0, 21.0, 6.0]);
            // Front foot pad (Y in [154.0, 166.0])
            translate([-19.0, 154.0, 4.0]) cube([6.0, 12.0, 6.0]);
        }

        // 5 Bolt holes (clearance Dia 3.4mm, counterbore Dia 6.5mm x 3.5mm deep)
        // Bolt positions:
        // [-16, 110.5], [-16, 122.0], [-16, 160.25], [-24, 116.0], [-24, 160.25]
        for (pt = [[-16.0, 110.5], [-16.0, 122.0], [-16.0, 160.25], [-24.0, 116.0], [-24.0, 160.25]]) {
            translate([pt[0], pt[1], 3.0]) cylinder(d = 3.4, h = 8.0);
            translate([pt[0], pt[1], 6.5]) cylinder(d = 6.5, h = 5.0);
        }

        // Pivot hole M3 through at (Y=140, Z=58)
        translate([-28.0, 140.0, 58.0]) rotate([0, 90, 0]) cylinder(d = 3.4, h = 10.0);

        // Captive hex nut pocket on inner face (X = -19.0)
        translate([-18.99, 140.0, 58.0]) rotate([0, -90, 0])
            cylinder(d = 6.45, h = 3.2, $fn = 6);
    }
}

left_stanchion();
