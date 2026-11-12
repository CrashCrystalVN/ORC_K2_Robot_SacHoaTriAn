
$fn = 60;
stl_file = "C:/Users/vuasu/.gemini/antigravity/scratch/ORC_K2_Robot_SacHoaTriAn/3D_Models/01D_Riser_Standoff_44mm_2S2P.stl";

module m3_hex_nut() {
    // DIN 934 Hex Nut: Outer corner d=6.35mm, flat-to-flat s=5.50mm, thickness=2.40mm
    cylinder(d = 6.35, h = 2.40, $fn = 6);
}

module m3_screw_shank(h = 12.0) {
    // Standard M3 screw shank: diameter 3.0mm
    cylinder(d = 3.0, h = h);
}

// 1. Intersection with Lower Nut
translate([0, 0, 0])
intersection() {
    import(stl_file);
    translate([0, 0, 3.675]) m3_hex_nut();
}

// 2. Intersection with Upper Nut
translate([20, 0, 0])
intersection() {
    import(stl_file);
    translate([0, 0, 37.925]) m3_hex_nut();
}

// 3. Intersection with Bottom Screw (Z = 0 to 12 mm)
translate([40, 0, 0])
intersection() {
    import(stl_file);
    translate([0, 0, 0.0]) m3_screw_shank(12.0);
}

// 4. Intersection with Top Screw (Z = h-12 to h mm)
translate([60, 0, 0])
intersection() {
    import(stl_file);
    translate([0, 0, 32.000]) m3_screw_shank(12.0);
}
