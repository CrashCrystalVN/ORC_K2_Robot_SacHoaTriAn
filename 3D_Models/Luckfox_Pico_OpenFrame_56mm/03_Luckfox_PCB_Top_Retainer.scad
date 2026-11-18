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

// Các hàm bổ trợ hình học chuẩn FDM
module rounded_box_z(lx, ly, lz, r=2.4) {
    hull() {
        for (sx = [-1, 1])
            for (sy = [-1, 1])
                translate([sx*(lx/2 - r), sy*(ly/2 - r), 0])
                    cylinder(r=r, h=lz);
    }
}

// ====================================================================
// CHI TIẾT 03: NẸP TRÊN KHÓA GIỮ PCB LUCKFOX PICO MAX / PRO
// - Đặt phẳng Z = 0 (mặt lưng phẳng áp bàn in PEI), 0% Support!
// - CÁC GÂN NẸP ĐÈ PCB (CLERANCE LUGS): Gồm 6 vấu đè cao 2.0mm
//   chĩa xuống mặt bo mạch tại Z = 17.6mm, ép chặt PCB không cho rung lắc.
// - CÁC VÁCH NGĂN ĐƯỢC GIA CỐ >= 1.8mm (loại bỏ hoàn toàn các vách mỏng <1.5mm):
//   + Vách Cam MIPI <-> RJ45: 1.8mm (trước đây 0.5mm)
//   + Vách RV1106 <-> Cam MIPI: 2.2mm (trước đây 1.0mm)
//   + Vách BOOT/RESET <-> RV1106: 2.0mm
//   + Vách Type-C <-> BOOT/RESET: 2.0mm (trước đây chồng lấn 0mm)
// - Hốc chìm đầu ốc M3 d=6.6mm vát 45° in cực sạch.
// ====================================================================

module part_03_pcb_top_retainer() {
    ret_L   = 79.0;
    ret_W   = 27.6;
    plate_H = 3.6;          // Độ dày tấm nẹp chính
    lug_H   = 2.0;          // Chiều cao vấu ép đè PCB (tổng chiều cao = 5.6mm)

    difference() {
        union() {
            // 1. Tấm nẹp chính (đặt phẳng Z = 0 .. plate_H)
            rounded_box_z(ret_L, ret_W, plate_H, r=2.5);

            // 2. 2 Tai bắt ốc M3 hai bên sườn (X = 0, Y = ±17.0mm)
            for (sy = [-1, 1]) {
                hull() {
                    translate([0, sy*(ret_W/2 + 3.2), 0])
                        cylinder(d=8.6, h=plate_H);
                    translate([-5.0, sy*(ret_W/2 - 1.5), 0])
                        cube([10.0, 3.0, plate_H]);
                }
            }

            // 3. CÁC VẤU KẸP ĐÈ PCB (Clamping Lugs) nhô lên từ Z = plate_H lên plate_H + lug_H
            //    (khi lắp ráp úp ngược xuống, các vấu này đè chuẩn Z = 17.6mm lên PCB)
            // A. Vấu đè đầu trái (flanking Type-C, X = -36.0 .. -32.5mm)
            translate([-36.0, -10.5, plate_H])
                cube([3.5, 3.5, lug_H]);
            translate([-36.0, 7.0, plate_H])
                cube([3.5, 3.5, lug_H]);

            // B. Vấu đè đầu phải (flanking RJ45, X = +33.0 .. +36.5mm)
            translate([33.0, -10.5, plate_H])
                cube([3.5, 2.0, lug_H]);
            translate([33.0, 8.5, plate_H])
                cube([3.5, 2.0, lug_H]);

            // C. Vấu đè giữa sườn (X = -3.0 .. +3.0mm, Y = ±(8.5 .. 10.5))
            translate([-3.0, -10.5, plate_H])
                cube([6.0, 2.0, lug_H]);
            translate([-3.0, 8.5, plate_H])
                cube([6.0, 2.0, lug_H]);
        }

        // ------------------------------------------------------------
        // CÁC HỐC THOÁNG TRÊN NẸP (ĐƯỢC ĐỊNH TUYẾN CHÍNH XÁC RIBS >= 1.8MM)
        // ------------------------------------------------------------

        // 1. Cổng RJ45 (X = +16.0 .. +40.0, rộng 17.0mm)
        translate([16.0, -8.5, -0.5])
            cube([24.0, 17.0, plate_H + lug_H + 1.0]);

        // 2. Cáp Camera MIPI CSI (X = +6.2 .. +14.2, rộng 16.5mm)
        //    -> Gân giữa Cam và RJ45 = 16.0 - 14.2 = 1.8mm (>= 1.5mm chuẩn!)
        translate([6.2, -8.25, -0.5])
            cube([8.0, 16.5, plate_H + lug_H + 1.0]);

        // 3. Khe tản nhiệt Chip RV1106 (X = -7.5 .. +4.0, rộng 14.0mm)
        //    -> Gân giữa RV1106 và Cam = 6.2 - 4.0 = 2.2mm (>= 1.5mm chuẩn!)
        translate([-7.5, -7.0, -0.5])
            cube([11.5, 14.0, plate_H + lug_H + 1.0]);

        // 4. Khe bấm nút BOOT / RESET & Thẻ nhớ MicroSD (X = -28.0 .. -9.5)
        //    -> Gân giữa BOOT/RESET và RV1106 = -7.5 - (-9.5) = 2.0mm (>= 1.5mm chuẩn!)
        translate([-28.0, -7.0, -0.5])
            cube([18.5, 14.0, plate_H + lug_H + 1.0]);

        // 5. Cổng Type-C (X = -40.5 .. -30.0, rộng 13.0mm)
        //    -> Gân giữa Type-C và BOOT/RESET = -28.0 - (-30.0) = 2.0mm (>= 1.5mm chuẩn!)
        translate([-40.5, -6.5, -0.5])
            cube([10.5, 13.0, plate_H + lug_H + 1.0]);

        // 6. 2 Lỗ ốc M3 ở 2 tai (X = 0, Y = ±17.0mm)
        for (sy = [-1, 1]) {
            translate([0, sy*(ret_W/2 + 3.2), -0.5])
                cylinder(d=3.4, h=plate_H + lug_H + 1.0);
            // Hốc chìm đầu ốc M3 d=6.6mm kèm vát mép 45°
            translate([0, sy*(ret_W/2 + 3.2), -0.1])
                cylinder(d=6.6, h=2.0);
            translate([0, sy*(ret_W/2 + 3.2), 1.9])
                cylinder(d1=6.6, d2=3.4, h=1.6);
        }
    }
}

part_03_pcb_top_retainer();
