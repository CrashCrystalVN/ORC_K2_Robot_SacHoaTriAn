
use <c:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\3D_Models\full_assembly.scad>;
use <c:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\3D_Models\gripper_v3_mg996r.scad>;

$fn = 48;

// Display full robot in stowed vs deployed with new gripper
translate([0, 0, 0]) {
    // Base robot assembly
    full_assembly_dfm();
}
