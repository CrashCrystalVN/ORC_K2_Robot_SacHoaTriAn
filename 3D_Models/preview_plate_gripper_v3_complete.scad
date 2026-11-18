// Preview Scene for Plate_Gripper_v3_Complete.3mf
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

// 1. Gripper Base Head V3
color([0.3, 0.5, 0.7]) {
    translate([75 - 1.00, 70 - 22.75, 0])
        import(str(BASE_DIR, "04_Gripper_Base_Head_v3.stl"));
}

// 2. Wrist Clevis Pitch Bracket S3
color([0.4, 0.7, 0.5]) {
    translate([175 - (-6.50), 70 - (-26.75), 0])
        import(str(BASE_DIR, "04A_Wrist_Clevis_Pitch_Bracket_S3.stl"));
}

// 3. Left Gripper Jaw V3
color([0.95, 0.55, 0.15]) {
    translate([75 - (-16.25), 175 - 44.25, 0])
        import(str(BASE_DIR, "05_Gripper_Jaw_Left_V3.stl"));
}

// 4. Right Gripper Jaw V3
color([0.85, 0.2, 0.2]) {
    translate([175 - 16.32, 175 - 44.32, 0])
        import(str(BASE_DIR, "06_Gripper_Jaw_Right_V3.stl"));
}
