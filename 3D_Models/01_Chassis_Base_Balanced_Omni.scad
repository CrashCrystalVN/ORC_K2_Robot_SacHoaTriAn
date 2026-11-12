// ====================================================================
// DỰ ÁN: ROBOT THI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & 20/11
// THIẾT KẾ: KHUNG GẦM CÂN BẰNG ĐỐI XỨNG BÁNH ĐA HƯỚNG (BALANCED OMNI BASE)
// FILE: 01_Chassis_Base_Balanced_Omni.scad
// PHIÊN BẢN V10.0: ĐỐI XỨNG TUYỆT ĐỐI 2 TRƯỚC - 2 SAU, TRIỆT TIÊU 100% NGHIÊNG/CHÚI
// TẬN DỤNG TRỤC Z: KHOANG PIN ĐẶT TẦNG 1 (01D), GIẢI PHÓNG TOÀN DIỆN LÒNG XE
// KÍCH THƯỚC: CHI TIẾT IN 136x160.5MM (BAMBU A1 MINI), PHỦ BÌ XE 174x176MM <= 185MM!
// DFM: 100% SOLID GA25 MOUNTS, ĐỦ 6 LỖ M3 PCD 17MM GIỌT NƯỚC 45°, 0% SUPPORT!
// ====================================================================

DISPLAY_MODE = "part"; // "part", "assembly_omni_58"
$fn = (DISPLAY_MODE == "part") ? 36 : 24;

// ====================================================================
// 1. THÔNG SỐ HÌNH HỌC CỐT LÕI (BALANCED OMNI BASE)
// ====================================================================
CHASSIS_W     = 136.0;   // Bề rộng phủ bì thân xe tại bệ motor (mm)
Y_START       = 8.0;     // Tọa độ Y bắt đầu sàn sau (mm)
Y_END         = 168.5;   // Tọa độ Y kết thúc cản trước ToF (mm)
CHASSIS_L_EFF = Y_END - Y_START; // 160.5 mm

FLOOR_T       = 4.0;     // Độ dày sàn chịu lực (mm)
WALL_T        = 4.0;     // Độ dày vách sườn chịu lực (mm)
WALL_H        = 30.0;    // Chiều cao vách sườn chính (mm)

// KHOẢNG LỌT LÒNG GIỮA 2 MẶT BÍCH MOTOR ĐỐI DIỆN:
// 2 Motor GA25 dài 63mm x 2 = 126mm.
// Lòng trong thân xe: 136.0 - 2 * 4.0 = 128.0 mm!
// Khe hở an toàn đuôi Encoder = 128.0 - 126.0 = 2.0 mm (ZERO COLLISION 100%)!
INNER_SPAN    = CHASSIS_W - 2.0 * WALL_T; // 128.0 mm

// THÔNG SỐ Ụ BỆ MOTOR GA25 (SOLID ROBUST MOUNT):
BOSS_D        = 32.0;    // Đường kính ụ bệ motor (mm) -> vách dày >= 3.3mm quanh motor 25.4mm
FLANGE_T      = 4.0;     // Độ dày mặt bích bắt motor (mm)
Z_SHAFT       = 20.0;    // Cao độ tâm trục bánh xe so với đáy sàn Z=0 (mm)
CRADLE_W      = 30.0;    // Chiều sâu ổ đỡ nửa dưới GA25 từ vách vào lòng xe (mm)

// ====================================================================
// 2. TỌA ĐỘ 4 ĐỘNG CƠ CÂN BẰNG ĐỐI XỨNG (SYMMETRIC BALANCED AXES)
// ====================================================================
// Cặp bánh sau: Đối xứng hoàn hảo, chống bập bênh đuôi xe 100%
Y_RL          = 24.0;    // Rear-Left motor  (Thành Trái X = -68mm, lòng X = -64mm)
Y_RR          = 24.0;    // Rear-Right motor (Thành Phải X = +68mm, lòng X = +64mm)

// Cặp bánh trước: Đối xứng hoàn hảo, chống chúi đầu / nghiêng lật 100%
Y_FL          = 142.0;   // Front-Left motor (Thành Trái X = -68mm, dưới vòm tháp nâng 01B)
Y_FR          = 142.0;   // Front-Right motor(Thành Phải X = +68mm, dưới vòm tháp nâng 01C)

WHEELBASE     = Y_FL - Y_RL; // 118.0 mm (Trọng tâm dồn chuẩn 4 bánh, đầm chắc tuyệt đối)

// ====================================================================
// 3. TRỤ ĐỠ TẦNG 1 (BATTERY DECK STANDOFFS - KHỚP 100% 01D_Battery_Deck_Platform)
// ====================================================================
PILLAR_Z_TOP  = 34.0;    // Cao độ đỉnh trụ đỡ tầng pin (mm)
PILLAR_W      = 8.0;     // Bề rộng trụ (mm)
PILLAR_L      = 8.0;     // Chiều dài trụ (mm)
PILLAR_HOLE_D = 2.8;     // Lỗ vít M3 tự taro in FDM (Ø2.8mm)
PILLAR_HOLE_H = 10.0;    // Chiều sâu lỗ bắt vít (mm)

// Tọa độ 4 lỗ bắt vít sàn pin 01D (Khớp 100% với X = ±35.0mm, Y = 38.0 & 100.0mm):
PILLAR_X      = 35.0;
PILLAR_Y_REAR = 38.0;
PILLAR_Y_FRNT = 100.0;

// ====================================================================
// TIỆN ÍCH LỖ GIỌT NƯỚC 45° TỰ ĐỠ IN FDM (TEARDROP HOLES CHO TRỤC X)
// ====================================================================
module teardrop_hole_x(d = 7.0, h = 10.0) {
    r = d / 2.0;
    side = r * sqrt(2.0);
    union() {
        rotate([0, 90, 0]) cylinder(d=d, h=h);
        translate([0, 0, r * 0.5])
            rotate([45, 0, 0])
                translate([0, -side/2.0, -side/2.0])
                    cube([h, side, side]);
    }
}

// ====================================================================
// MODULE Ụ ĐỘNG CƠ GA25 NGUYÊN KHỐI SOLID (ADDITIVE UNION)
// ====================================================================
module motor_mount_solid(is_right = false, my = 24.0, cradle_len = 32.0) {
    sx = is_right ? 1 : -1;
    x_wall_outer = sx * CHASSIS_W / 2.0;
    x_wall_inner = is_right ? (x_wall_outer - WALL_T) : (x_wall_outer + WALL_T);

    // 1. Ụ nhô Boss mặt bích tích hợp vách ngoài + bệ dốc hình chóp xuống sàn
    hull() {
        if (is_right) {
            translate([x_wall_inner, my, Z_SHAFT])
                rotate([0, 90, 0]) cylinder(d=BOSS_D, h=WALL_T);
            translate([x_wall_inner, my - 16.0, 0])
                cube([WALL_T, 32.0, FLOOR_T]);
        } else {
            translate([x_wall_outer, my, Z_SHAFT])
                rotate([0, 90, 0]) cylinder(d=BOSS_D, h=WALL_T);
            translate([x_wall_outer, my - 16.0, 0])
                cube([WALL_T, 32.0, FLOOR_T]);
        }
    }

    // 2. Vách chịu lực cục bộ nâng cao Z=36mm bảo vệ ụ động cơ
    if (is_right) {
        translate([x_wall_inner, my - cradle_len/2.0, 0])
            cube([WALL_T, cradle_len, Z_SHAFT + BOSS_D/2.0]);
    } else {
        translate([x_wall_outer, my - cradle_len/2.0, 0])
            cube([WALL_T, cradle_len, Z_SHAFT + BOSS_D/2.0]);
    }

    // 3. Khối ổ đỡ Saddle Cradle đỡ nửa dưới thân động cơ GA25 (từ vách vào lòng 30mm)
    if (is_right) {
        translate([x_wall_inner - CRADLE_W, my - cradle_len/2.0, 0])
            cube([CRADLE_W, cradle_len, 20.0]);
    } else {
        translate([x_wall_inner, my - cradle_len/2.0, 0])
            cube([CRADLE_W, cradle_len, 20.0]);
    }
}

// ====================================================================
// MODULE KHOÉT RỖNG ĐỘNG CƠ GA25 & 6 LỖ M3 PCD 17MM (SUBTRACTIVE CUTS)
// ====================================================================
module motor_mount_cuts(is_right = false, my = 24.0) {
    sx = is_right ? 1 : -1;
    x_wall_outer = sx * CHASSIS_W / 2.0;
    x_wall_inner = is_right ? (x_wall_outer - WALL_T) : (x_wall_outer + WALL_T);

    // 1. Khoét hốc lắp động cơ GA25 d=25.4mm trong lòng ổ đỡ Saddle Cradle
    if (is_right) {
        translate([x_wall_inner - CRADLE_W - 0.1, my, Z_SHAFT])
            rotate([0, 90, 0])
                cylinder(d=25.4, h=CRADLE_W + 0.1);
    } else {
        translate([x_wall_inner, my, Z_SHAFT])
            rotate([0, 90, 0])
                cylinder(d=25.4, h=CRADLE_W + 0.1);
    }

    // 2. Lỗ trục 7mm dạng giọt nước Teardrop 45° in FDM (d=7.2mm kèm dung sai co ngót)
    if (is_right) {
        translate([x_wall_inner - 1.0, my, Z_SHAFT])
            teardrop_hole_x(d=7.2, h=WALL_T + 2.0);
    } else {
        translate([x_wall_outer - 1.0, my, Z_SHAFT])
            teardrop_hole_x(d=7.2, h=WALL_T + 2.0);
    }

    // 3. Đủ 6 lỗ ốc M3 PCD 17mm (bán kính 8.5mm, chia đều 60 độ: 0, 60, 120, 180, 240, 300)
    for (a = [0:60:300]) {
        hy = my + 8.5 * cos(a);
        hz = Z_SHAFT + 8.5 * sin(a);
        if (is_right) {
            translate([x_wall_inner - 1.0, hy, hz])
                teardrop_hole_x(d=3.4, h=WALL_T + 2.0);
        } else {
            translate([x_wall_outer - 1.0, hy, hz])
                teardrop_hole_x(d=3.4, h=WALL_T + 2.0);
        }
    }
}

// ====================================================================
// MODULE KHUNG GẦM CHÍNH CÂN BẰNG ĐỐI XỨNG (chassis_base_balanced_omni)
// ====================================================================
module chassis_base_balanced_omni() {
    difference() {
        union() {
            // 1. SÀN ĐÁY PHẲNG CHÍNH TẠI Z = 0.0 mm
            translate([-CHASSIS_W/2.0, Y_START, 0])
                cube([CHASSIS_W, CHASSIS_L_EFF, FLOOR_T]);

            // 2. HAI VÁCH SƯỜN CHỊU LỰC CHÍNH (Z = 0..30mm, từ Y_START đến Y=164.5mm)
            translate([-CHASSIS_W/2.0, Y_START, 0])
                cube([WALL_T, 164.5 - Y_START, WALL_H]);
            translate([CHASSIS_W/2.0 - WALL_T, Y_START, 0])
                cube([WALL_T, 164.5 - Y_START, WALL_H]);

            // Vát chuyển tiếp êm từ vách sườn cao 30mm xuống cản trước cao 14mm
            hull() {
                translate([-CHASSIS_W/2.0, 160.0, 0])
                    cube([WALL_T, 4.5, WALL_H]);
                translate([-CHASSIS_W/2.0, 164.5, 0])
                    cube([WALL_T, 1.0, 14.0]);
            }
            hull() {
                translate([CHASSIS_W/2.0 - WALL_T, 160.0, 0])
                    cube([WALL_T, 4.5, WALL_H]);
                translate([CHASSIS_W/2.0 - WALL_T, 164.5, 0])
                    cube([WALL_T, 1.0, 14.0]);
            }

            // 3. 4 CỤM BỆ MOTOR GA25 CÂN BẰNG ĐỐI XỨNG NGUYÊN KHỐI
            // Cặp bánh sau tại Y = 24.0mm (Cân bằng tuyệt đối, đối xứng trái - phải)
            motor_mount_solid(is_right = false, my = Y_RL, cradle_len = 32.0);
            motor_mount_solid(is_right = true,  my = Y_RR, cradle_len = 32.0);

            // Cặp bánh trước tại Y = 142.0mm (Dưới vòm tháp nâng 01B và 01C, đối xứng trái - phải)
            motor_mount_solid(is_right = false, my = Y_FL, cradle_len = 30.0);
            motor_mount_solid(is_right = true,  my = Y_FR, cradle_len = 30.0);

            // 4. 4 TRỤ ĐỠ TẦNG 1 (BATTERY DECK PILLARS) - KHỚP 100% HOLE_X=±35, HOLE_Y=38 & 100
            for (sx = [-1, 1]) {
                // Trụ sau Y=38.0mm: Kết nối vững chắc vào sàn và liên kết ụ motor sau
                translate([sx * PILLAR_X - PILLAR_W/2.0, PILLAR_Y_REAR - PILLAR_L/2.0, 0])
                    cube([PILLAR_W, PILLAR_L, PILLAR_Z_TOP]);

                // Gân tăng cứng trụ sau xuống sàn
                hull() {
                    translate([sx * PILLAR_X - PILLAR_W/2.0, PILLAR_Y_REAR - PILLAR_L/2.0, 0])
                        cube([PILLAR_W, PILLAR_L, 16.0]);
                    translate([sx * PILLAR_X - PILLAR_W/2.0, PILLAR_Y_REAR + 4.0, 0])
                        cube([PILLAR_W, 8.0, FLOOR_T]);
                }

                // Trụ trước Y=100.0mm: Đứng vững trên sàn với gân tam giác
                translate([sx * PILLAR_X - PILLAR_W/2.0, PILLAR_Y_FRNT - PILLAR_L/2.0, 0])
                    cube([PILLAR_W, PILLAR_L, PILLAR_Z_TOP]);

                // Gân tăng cứng trụ trước xuống sàn
                hull() {
                    translate([sx * PILLAR_X - PILLAR_W/2.0, PILLAR_Y_FRNT - 10.0, 0])
                        cube([PILLAR_W, 4.0, FLOOR_T]);
                    translate([sx * PILLAR_X - PILLAR_W/2.0, PILLAR_Y_FRNT - PILLAR_L/2.0, 0])
                        cube([PILLAR_W, PILLAR_L, 16.0]);
                    translate([sx * PILLAR_X - PILLAR_W/2.0, PILLAR_Y_FRNT + PILLAR_L/2.0, 0])
                        cube([PILLAR_W, 8.0, FLOOR_T]);
                }
            }

            // 5. CẢN TRƯỚC TÍCH HỢP HỐC ToF VL53L0X - NGUYÊN KHỐI KHÔNG KHE HỞ
            hull() {
                translate([-CHASSIS_W/2.0, 164.5, 0])
                    cube([CHASSIS_W, 1.5, 14.0]);
                translate([-28.0, Y_END - 2.0, 0])
                    cube([56.0, 2.0, 14.0]);
            }

            // 6. GỜ ĐỊNH VỊ CHÂN THÁP NÂNG (01B & 01C)
            translate([-28.5, 126.0, FLOOR_T]) cube([2.0, 26.0, 3.0]);
            translate([ 26.5, 126.0, FLOOR_T]) cube([2.0, 26.0, 3.0]);
        }

        // ================= KHOÉT RỖNG CSG & LỖ GIỌT NƯỚC 45° =================

        // 1. KHOÉT 4 VỊ TRÍ ĐỘNG CƠ GA25, LỖ TRỤC 7.2MM & 6 LỖ M3 PCD 17MM
        motor_mount_cuts(is_right = false, my = Y_RL);
        motor_mount_cuts(is_right = true,  my = Y_RR);
        motor_mount_cuts(is_right = false, my = Y_FL);
        motor_mount_cuts(is_right = true,  my = Y_FR);

        // 2. 4 LỖ ỐC M3 TRÊN ĐỈNH 4 TRỤ ĐỠ TẦNG PIN (Z = 34.0mm, X = ±35.0, Y = 38.0 & 100.0)
        for (sx = [-1, 1]) {
            for (py = [PILLAR_Y_REAR, PILLAR_Y_FRNT]) {
                translate([sx * PILLAR_X, py, PILLAR_Z_TOP - PILLAR_HOLE_H])
                    cylinder(d=PILLAR_HOLE_D, h=PILLAR_HOLE_H + 1.0);
            }
        }

        // 3. 10 LỖ BU-LÔNG M3 CHÂN THÁP NÂNG 01B & 01C (CHÍNH XÁC TUYỆT ĐỐI)
        for (sx = [-16.0, 16.0]) {
            for (sy = [110.5, 122.0, 160.25]) {
                translate([sx, sy, -1.0]) cylinder(d=3.4, h=30.0);
            }
        }
        for (sx = [-24.0, 24.0]) {
            for (sy = [116.0, 160.25]) {
                translate([sx, sy, -1.0]) cylinder(d=3.4, h=30.0);
            }
        }

        // 4. LỖ BẮT ĐẾ CẢM BIẾN DÒ LINE (01E) DƯỚI GẦM TRƯỚC
        for (lx = [-12.0, -8.0, 8.0, 12.0]) {
            translate([lx, CHASSIS_L_EFF + Y_START - 12.0, -0.5])
                cylinder(d=3.2, h=FLOOR_T + 1.0);
        }
        // Khe luồn cáp cảm biến dò line
        translate([-8.0, 148.0, -0.5])
            cube([16.0, 6.0, FLOOR_T + 1.0]);

        // 5. CỬA SỔ QUANG HỌC ToF VL53L0X Ở MŨI CẢN TRƯỚC
        translate([0, Y_END - 6.0, 7.0]) {
            rotate([-90, 0, 0]) cylinder(d=7.0, h=8.0);
            translate([0, 3.0, 0])
                rotate([-90, 0, 0])
                    cylinder(d1=7.0, d2=12.0, h=4.0);
            for (tx = [-10.0, 10.0]) {
                translate([tx, -1.0, 0])
                    rotate([-90, 0, 0])
                        cylinder(d=3.2, h=8.0);
            }
        }

        // 6. ĐUÔI XE TRÒN MƯỢT TỰ NHIÊN:
        // Hai ụ động cơ sau BOSS_D=32mm tại Y=24mm bo tròn tự nhiên với bán kính R=16mm,
        // không cần vát góc nhân tạo, bảo toàn 100% vách dày chịu lực và 6 lỗ M3 PCD 17mm.

        // 7. RÃNH THOÁT NHIỆT & GIẢM TRỌNG LƯỢNG SÀN XE (LIGHTWEIGHT VENT SLOTS)
        for (vy = [54.0, 76.0]) {
            translate([-18.0, vy, -0.5])
                cube([36.0, 12.0, FLOOR_T + 1.0]);
        }
    }
}

// Render ở chế độ part mặc định
if (DISPLAY_MODE == "part") {
    chassis_base_balanced_omni();
}
