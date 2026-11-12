use <01_Chassis_Base_UltraCompact_Omni.scad>;

$fn = 28;

WHEEL_CONFIG = "OMNI_58"; // "OMNI_58", "OMNI_48", "MECANUM_60"

WHEEL_D = (WHEEL_CONFIG == "OMNI_58") ? 58.0 : ((WHEEL_CONFIG == "OMNI_48") ? 48.0 : 60.0);
WHEEL_W = (WHEEL_CONFIG == "OMNI_58") ? 16.0 : ((WHEEL_CONFIG == "OMNI_48") ? 15.0 : 28.0);
GROUND_CLEAR = WHEEL_D / 2.0 - 20.0; // 9.0mm (Omni 58) or 4.0mm (Omni 48)

CHASSIS_W = 118.0;
Y_REAR = 32.0;
Y_FRONT = 142.0;

TOTAL_W = CHASSIS_W + 2 * (2.0 + WHEEL_W);
TOTAL_L = (Y_FRONT + WHEEL_D/2.0) - (Y_REAR - WHEEL_D/2.0);

echo("Total Width:", TOTAL_W, "mm");
echo("Total Length:", TOTAL_L, "mm");

// Base Plate
color("DarkSlateGray")
    translate([0, 0, GROUND_CLEAR])
        chassis_base_ultracompact_omni();

// 4 Wheels
for (side = [-1, 1]) {
    x_pos = side * (CHASSIS_W/2 + 2.0 + WHEEL_W/2.0);
    translate([x_pos, Y_REAR, 20.0 + GROUND_CLEAR])
        omni_wheel_sim(wheel_d = WHEEL_D, wheel_w = WHEEL_W);
    translate([x_pos, Y_FRONT, 20.0 + GROUND_CLEAR])
        omni_wheel_sim(wheel_d = WHEEL_D, wheel_w = WHEEL_W);
}

// 4 GA25 Motors
for (side = [-1, 1]) {
    // Rear Encoder Motor (63mm)
    translate([side * (CHASSIS_W/2 + 6.0), Y_REAR, 20.0 + GROUND_CLEAR])
        rotate([0, side > 0 ? -90 : 90, 0]) {
            color("Silver") cylinder(d=25.0, h=48.0);
            color("DimGray") translate([0, 0, 48.0]) cylinder(d=24.4, h=15.0);
        }
    // Front DC Motor (48mm)
    translate([side * (CHASSIS_W/2 + 6.0), Y_FRONT, 20.0 + GROUND_CLEAR])
        rotate([0, side > 0 ? -90 : 90, 0]) {
            color("Silver") cylinder(d=25.0, h=48.0);
        }
}

// Battery Pack 2S2P Brick
color("RoyalBlue", 0.85)
    translate([-19.0, 51.0, GROUND_CLEAR + 4.0])
        cube([38.0, 70.0, 38.0]);

// K2 Control Hub Deck
color("Black")
    translate([-60.5, 30.0, GROUND_CLEAR + 44.0])
        cube([121.0, 86.0, 26.0]);

// Wireframe Box 185mm Cube
color("Red", 0.25) {
    translate([-92.5, 0, 0]) {
        cube([185, 1.5, 1.5]);
        cube([1.5, 185, 1.5]);
        translate([0, 183.5, 0]) cube([185, 1.5, 1.5]);
        translate([183.5, 0, 0]) cube([1.5, 185, 1.5]);
        translate([0, 0, 183.5]) {
            cube([185, 1.5, 1.5]);
            cube([1.5, 185, 1.5]);
            translate([0, 183.5, 0]) cube([185, 1.5, 1.5]);
            translate([183.5, 0, 0]) cube([1.5, 185, 1.5]);
        }
        cube([1.5, 1.5, 185]);
        translate([183.5, 0, 0]) cube([1.5, 1.5, 185]);
        translate([0, 183.5, 0]) cube([1.5, 1.5, 185]);
        translate([183.5, 183.5, 0]) cube([1.5, 1.5, 185]);
    }
}
