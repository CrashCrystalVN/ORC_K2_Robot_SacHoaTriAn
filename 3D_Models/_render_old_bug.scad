
use <01_Chassis_Base_Zigzag_Omni.scad>;
difference() {
    color([0.976, 0.549, 0.0])
        chassis_base_zigzag_omni();
    // Re-introduce the buggy 14mm chamfer at rear left that caused the crescent & sliver
    translate([-76.0/2.0 - 1.0, 8.0 - 1.0, -1.0])
        rotate([0, 0, 45])
            cube([14.0, 14.0, 32.0]);
}
