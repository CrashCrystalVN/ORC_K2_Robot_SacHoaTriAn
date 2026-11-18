// Preview Scene for Plate_Tower_2Part_Compact.3mf (Option A)
// Build plate 256 x 256 mm

$fn = 32;

BASE_DIR = "C:/Users/vuasu/.gemini/antigravity/scratch/ORC_K2_Robot_SacHoaTriAn/3D_Models/";

// Textured PEI Plate outline
color([0.2, 0.2, 0.2, 0.4]) {
    translate([0, 0, -1.0])
        cube([256, 256, 1.0]);
}

// Grid lines & plate border
color([0.9, 0.6, 0.1, 0.8]) {
    translate([10, 10, -0.5])
        difference() {
            cube([236, 236, 0.6]);
            translate([2, 2, -0.1]) cube([232, 232, 1.0]);
        }
}

// Part 1: local_x = 80.0, local_y = 128.0, center = (31.50, 32.125, 7.0)
color([0.2, 0.55, 0.85]) {
    translate([80.0 - 31.50, 128.0 - 32.125, 0])
        import(str(BASE_DIR, "01_Tower_Left_Stanchion_v2.stl"));
}

// Part 2: local_x = 176.0, local_y = 128.0, center = (37.45, 137.625, 7.5)
color([0.95, 0.45, 0.1]) {
    translate([176.0 - 37.45, 128.0 - 137.625, 0])
        import(str(BASE_DIR, "02_Tower_Right_Stanchion_v2.stl"));
}
