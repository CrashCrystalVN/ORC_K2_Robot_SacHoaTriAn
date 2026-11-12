
$fn = 50;

chassis_file = "C:/Users/vuasu/.gemini/antigravity/scratch/ORC_K2_Robot_SacHoaTriAn/3D_Models/01_Chassis_Base_200x200.stl";
clamp_file = "C:/Users/vuasu/.gemini/antigravity/scratch/ORC_K2_Robot_SacHoaTriAn/3D_Models/02_GA25_Rear_Motor_Clamp_Universal.stl";
standoff_file = "C:/Users/vuasu/.gemini/antigravity/scratch/ORC_K2_Robot_SacHoaTriAn/3D_Models/01D_Riser_Standoff_44mm_2S2P.stl";

// Battery Brick 2S2P: 38 x 38 x 70 mm
// Placed symmetrically in battery bay: X in [-19, +19], Y in [48 + (76-70)/2, 48 + (76-70)/2 + 70] = [51, 121], Z in [4.0, 42.0]
module bat_brick_2s2p() {
    translate([-19.0, 51.0, 4.0])
        cube([38.0, 70.0, 38.0]);
}

// 4x Standoffs 44mm mounted on floor Z = 4.0 mm
// X = +-33.0, Y = 49.0 & 99.0
// Rear row Y = 49.0: D-flat facing -Y (rotation [0, 0, 0])
// Front row Y = 99.0: D-flat facing -Y or arbitrary
module four_standoffs() {
    for (sx = [-33.0, 33.0]) {
        // Rear standoffs (Y = 49.0), D-flat facing -Y
        translate([sx, 49.0, 4.0])
            import(standoff_file);
        // Front standoffs (Y = 99.0)
        translate([sx, 99.0, 4.0])
            import(standoff_file);
    }
}

// 2x Rear Motor Clamps Universal at X = +-44.0, Y = 32.0, Z = 20.0
// Note: 02_GA25_Rear_Motor_Clamp_Universal.stl was exported lying flat for 3D printing
// (translate([0,0,4]) rotate([0,-90,0]) canonical).
// Its canonical in-situ orientation on the robot is rotate([0, 90, 0]) translate([0, 0, -4.0]) STL.
module canonical_clamp() {
    rotate([0, 90, 0])
        translate([0, 0, -4.0])
            import(clamp_file);
}

module rear_clamps() {
    translate([-44.0, 32.0, 20.0])
        canonical_clamp();
    translate([44.0, 32.0, 20.0])
        canonical_clamp();
}

// CHECK 1: Standoffs vs Clamps Intersection
intersection() {
    four_standoffs();
    rear_clamps();
}
