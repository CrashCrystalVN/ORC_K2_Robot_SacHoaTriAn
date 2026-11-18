$fn = 64;

// ====================================================================
// THÔNG SỐ HÌNH HỌC HỆ THỐNG
// ====================================================================

// 1. Hệ 2 ống tròn Ø8.0 mm
rod_D       = 8.25;         // Đường kính kẹp ôm ống Ø8.0mm (+0.25mm dung sai ôm khít)
rod_CC      = 56.0;         // Khoảng cách tâm - đến - tâm (C-C) = 56.0mm (X = -28.0 và +28.0)
rod_out     = 64.0;         // Mép ngoài - ngoài = 64.0mm (tại X = -32.0 và +32.0)
rod_in      = 48.0;         // Mép trong - trong = 48.0mm (tại X = -24.0 và +24.0)

// 2. Bo Luckfox Pico Max / Pro
pcb_L       = 72.0;         // Chiều dài PCB Luckfox (mm) (X = -36.0 .. +36.0)
pcb_W       = 21.0;         // Chiều rộng PCB Luckfox (mm) (Y = -10.5 .. +10.5)
pcb_T       = 1.6;          // Độ dày PCB (mm)

cav_L       = 72.8;         // Chiều dài hốc chứa PCB (+0.8mm dung sai)
cav_W       = 21.6;         // Chiều rộng hốc chứa PCB (+0.6mm dung sai)

// 3. Chân GPIO Luckfox (40 chân quay xuống dưới)
gpio_L      = 50.8;         // Chiều dài 2 hàng chân 20x1 (X = -35.2 .. +15.6)
gpio_H      = 11.5;         // Độ sâu chân thò xuống dưới PCB (mm)
gpio_Y      = 8.89;         // Khoảng cách tâm 2 hàng chân (Y = -8.89 và +8.89)

// 4. Module Cảm biến ToF VL53L5CX V2
tof_pcb_L   = 24.7;         // Chiều dài tổng thể PCB gồm 2 tai bắt ốc (mm)
tof_pcb_H   = 10.5;         // Chiều cao thân PCB (mm)
tof_pcb_T   = 1.2;          // Độ dày PCB ToF (mm)
tof_hole_CC = 20.0;         // Khoảng cách tâm 2 lỗ ốc M2 = 20.0mm (X = -10.0 và +10.0)
tof_hole_D  = 2.3;          // Đường kính lỗ ốc M2 (mm)
tof_sensor_W = 6.4;         // Kích thước mắt cảm biến (mm)
tof_sensor_H = 3.0;

// Import các chi tiết
use <01B_Luckfox_OpenFrame_BackMount_56mm.scad>
use <02B_Rod_Clamp_BackMount_56mm.scad>
use <03_Luckfox_PCB_Top_Retainer.scad>
use <04_VL53L5CX_V2_Sensor_Bracket.scad>
use <01A_Luckfox_OpenFrame_UnderMount_56mm.scad>
use <02A_Rod_Clamp_Dual_Bar_56mm.scad>

// 1. Hai ống tròn Ø8.0mm dựng đứng dọc trục Z (C-C = 56.0mm chuẩn)
module render_rods_vertical() {
    color([0.75, 0.78, 0.80, 0.9]) {
        for (sx = [-1, 1]) {
            translate([sx*(rod_CC/2), 21.2, -15.0])
                cylinder(d=8.0, h=60.0);
        }
    }
}

// 2. Bo mạch Luckfox Pico Max / Pro
module render_luckfox_board() {
    z_bot = 16.0;
    // PCB (Xanh lá công nghiệp)
    color([0.1, 0.55, 0.25, 0.95])
        translate([-pcb_L/2, -pcb_W/2, z_bot])
            cube([pcb_L, pcb_W, pcb_T]);

    // Cổng RJ45 (Bạc kim loại)
    color([0.85, 0.85, 0.88, 1.0])
        translate([16.0, -8.0, z_bot + pcb_T])
            cube([21.0, 16.0, 13.5]);

    // Cổng Type-C (Bạc)
    color([0.75, 0.75, 0.78, 1.0])
        translate([-36.5, -4.5, z_bot + pcb_T])
            cube([7.0, 9.0, 3.2]);

    // Chip SoC RV1106 (Đen mờ)
    color([0.15, 0.15, 0.15, 1.0])
        translate([-7.0, -5.0, z_bot + pcb_T])
            cube([10.0, 10.0, 1.2]);

    // 40 Chân GPIO quay xuống dưới (Vàng đồng)
    color([0.9, 0.75, 0.2, 1.0]) {
        for (i = [0:19]) {
            x_pin = -34.5 + i*2.54;
            for (sy = [-1, 1]) {
                translate([x_pin, sy*gpio_Y, z_bot - gpio_H])
                    cylinder(d=0.64, h=gpio_H);
            }
        }
    }
}

// 3. Module ToF VL53L5CX V2
module render_tof_module() {
    // PCB ToF (Tím đậm)
    color([0.35, 0.15, 0.45, 0.95])
        translate([-tof_pcb_L/2, -tof_pcb_T/2, -tof_pcb_H/2])
            cube([tof_pcb_L, tof_pcb_T, tof_pcb_H]);

    // Mắt cảm biến quang học VL53L5CX (Đen bóng có thấu kính)
    color([0.1, 0.1, 0.1, 1.0])
        translate([-tof_sensor_W/2, tof_pcb_T/2, -tof_sensor_H/2])
            cube([tof_sensor_W, 1.6, tof_sensor_H]);

    // 6 Chân header cắm dây Dupont
    color([0.9, 0.75, 0.2, 1.0]) {
        for (p = [0:5]) {
            translate([-6.35 + p*2.54, 0, -tof_pcb_H/2 - 2.5])
                cylinder(d=0.64, h=3.0);
        }
    }
}

// ====================================================================
// TOÀN BỘ CỤM LẮP RÁP PREVIEW - PHIÊN BẢN BACK-MOUNT (TIÊU CHUẨN)
// ====================================================================
module full_assembly_backmount() {
    // 1. Khung Open-Frame BackMount Base (Cam ORC)
    color([0.95, 0.45, 0.1, 0.9])
        part_01B_openframe_backmount();

    // 2. Thanh khóa kép sau lưng 02B (Cam đậm) kèm khe hở kẹp 1.20mm
    color([0.8, 0.35, 0.08, 0.95])
        translate([0, 21.8 + 9.0, 9.8])
            rotate([90, 0, 0])
                part_02B_rod_clamp_backmount();

    // 3. Nẹp trên khóa giữ PCB 03 (Vàng cam)
    //    Lật úp để vấu kẹp đè đúng Z = 17.6mm lên PCB
    color([0.95, 0.65, 0.15, 0.85])
        translate([0, 0, 23.2])
            rotate([180, 0, 0])
                part_03_pcb_top_retainer();

    // 4. Giá gá ToF VL53L5CX V2 (Xanh dương ORC) ở mặt trước
    color([0.15, 0.45, 0.85, 0.9])
        translate([0, -17.3, 0])
            part_04_vl53l5cx_v2_sensor_bracket();

    // 5. Module ToF đặt trên giá gá
    translate([0, -17.3 - (10/2 - 1.0) - 1.2, 3.5 + 9.5])
        rotate([0, 0, 180])
            render_tof_module();

    // 6. Bo mạch Luckfox Pico Max
    render_luckfox_board();

    // 7. 2 Ống Ø8.0mm dựng đứng C-C 56mm
    render_rods_vertical();
}

full_assembly_backmount();
