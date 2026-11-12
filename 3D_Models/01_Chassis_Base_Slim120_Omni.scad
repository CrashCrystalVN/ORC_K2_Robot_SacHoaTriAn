// ====================================================================
// DỰ ÁN: ROBOT THI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & 20/11
// THIẾT KẾ: KHUNG GẦM SIÊU HẸP ULTRA-SLIM 120 (ORC-K2 SLIM120 OMNI BASE)
// FILE: 01_Chassis_Base_Slim120_Omni.scad
// PHIÊN BẢN V11.0: ĐỘT PHÁ GIẢI QUYẾT BÀI TOÁN "TỔNG TRỤC X < 120MM"
// 1. BỀ RỘNG THÂN XE CHỈ 72.0MM (BẢO ĐẢM TỔNG PHỦ BÌ XE CẢ BÁNH <= 116.0MM < 120.0MM)
// 2. BỐ TRÍ 4 ĐỘNG CƠ GA25 ZIGZAG ĐAN CHÉO ĐUÔI - ZERO COLLISION 100%
// 3. TÍCH HỢP 4 ĐIỂM TỰA TRỢ LỰC CHỐNG CHÚI / BẬP BÊNH (CASTER BALL Ø12MM / SKID PADS)
// 4. TƯƠNG THÍCH 100% THÁP NÂNG 01B/01C, CẢM BIẾN ToF, DÒ LINE & SÀN PIN 01D TẦNG 1
// ====================================================================

DISPLAY_MODE = "part"; // "part", "assembly_omni_58", "assembly_omni_48"
$fn = (DISPLAY_MODE == "part") ? 36 : 24;

// ====================================================================
// 1. THÔNG SỐ HÌNH HỌC CỐT LÕI (ULTRA-SLIM 120MM SPECIFICATIONS)
// ====================================================================
CHASSIS_W     = 72.0;    // Bề rộng khung xe chính siêu hẹp (mm)
Y_START       = 8.0;     // Tọa độ Y bắt đầu sàn sau (mm)
Y_END         = 168.5;   // Tọa độ Y kết thúc cản trước ToF (mm)
CHASSIS_L_EFF = Y_END - Y_START; // 160.5 mm

FLOOR_T       = 4.0;     // Độ dày sàn chịu lực (mm)
WALL_T        = 4.0;     // Độ dày vách sườn chịu lực (mm)
WALL_H        = 30.0;    // Chiều cao vách sườn chính (mm)

// THÔNG SỐ Ụ BỆ MOTOR GA25 (SLIM SOLID GA25 MOUNT):
BOSS_OUT      = 3.0;     // Độ nhô ra ngoài của mặt bích (mm)
BOSS_D        = 32.0;    // Đường kính ngoài bệ motor (mm) -> Vách dày >= 3.3mm quanh motor 25.4mm
FLANGE_T      = 3.5;     // Độ dày mặt bích bắt motor (mm) >= 3.0mm
Z_SHAFT       = 20.0;    // Cao độ tâm trục bánh xe so với đáy sàn Z=0 (mm)
CRADLE_W      = 16.0;    // Chiều sâu ổ đỡ nửa dưới GA25 từ vách vào lòng xe (mm)

// TỌA ĐỘ 4 ĐỘNG CƠ GA25 ZIGZAG SO LE TỐI ƯU KHOẢNG CÁCH:
Y_RL          = 24.0;    // Rear-Left motor  (Thành Trái X = -36mm)
Y_RR          = 50.0;    // Rear-Right motor (Thành Phải X = +36mm, Stagger +26mm > 24.4mm)
Y_FL          = 90.0;    // Front-Left motor (Thành Trái X = -36mm, Vươn xa tối đa sát chân tháp)
Y_FR          = 142.0;   // Front-Right motor(Thành Phải X = +36mm, Dưới vòm tháp nâng 01C)

// TRỤ ĐỠ TẦNG 1 (BATTERY DECK STANDOFFS - KHỚP 100% 01D_Battery_Deck_Platform):
PILLAR_Z_TOP  = 34.0;    // Cao độ đỉnh trụ đỡ tầng pin (mm)
PILLAR_W      = 7.0;     // Bề rộng trụ theo trục X (mm)
PILLAR_L      = 8.0;     // Chiều dài trụ theo trục Y (mm)
PILLAR_HOLE_D = 2.8;     // Đường kính lỗ vít M3 tự taro / ren nhựa FDM (chuẩn Ø2.8mm)
PILLAR_HOLE_H = 10.0;    // Chiều sâu lỗ bắt vít (mm)

// Tọa độ 4 lỗ bắt vít sàn pin 01D (Khớp 100% X = ±35.0, Y = 38.0 & 100.0):
PILLAR_X      = 35.0;
PILLAR_Y_REAR = 38.0;
PILLAR_Y_FRNT = 100.0;

// ĐIỂM TỰA TRỢ LỰC CHỐNG CHÚI / BẬP BÊNH (ANTI-TIP CASTER BALL / SKID PADS):
CASTER_X      = 26.0;    // Tọa độ X tâm gá bi mắt trâu (±26.0mm)
CASTER_Y_FRNT = 156.0;   // Tọa độ Y điểm tựa trước (ngay sau cản ToF, đỡ mũi góc trái & phải)
CASTER_Y_REAR = 16.0;    // Tọa độ Y điểm tựa sau (đỡ đuôi góc phải & trái)
CASTER_REC_D  = 14.0;    // Đường kính hốc bi mắt trâu Ø12-14mm
CASTER_REC_H  = 1.5;     // Độ lõm hốc bi (mm)
CASTER_HOLE_SP= 16.0;    // Khoảng cách 2 lỗ vít M3 gá bi (mm)

// TIỆN ÍCH LỖ GIỌT NƯỚC 45° TỰ ĐỠ IN FDM (TEARDROP HOLES CHO TRỤC X)
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

// MODULE Ụ ĐỘNG CƠ NGUYÊN KHỐI SOLID (ADDITIVE UNION)
module motor_mount_solid(is_right = false, my = 24.0, cradle_len = 32.0, cradle_y_offset = 0) {
    sx = is_right ? 1 : -1;
    x_wall_outer = sx * CHASSIS_W / 2.0;
    
    // 1. Ụ nhô Boss mặt bích ngoài + bệ dốc xuống sàn
    hull() {
        if (is_right) {
            translate([x_wall_outer, my, Z_SHAFT])
                rotate([0, 90, 0]) cylinder(d=BOSS_D, h=BOSS_OUT);
            translate([x_wall_outer, my - 14.0, 0])
                cube([BOSS_OUT, 28.0, FLOOR_T]);
        } else {
            translate([x_wall_outer - BOSS_OUT, my, Z_SHAFT])
                rotate([0, 90, 0]) cylinder(d=BOSS_D, h=BOSS_OUT);
            translate([x_wall_outer - BOSS_OUT, my - 14.0, 0])
                cube([BOSS_OUT, 28.0, FLOOR_T]);
        }
    }
    
    // 2. Vách chịu lực cục bộ nâng cao Z=34mm (bảo vệ ụ động cơ và đỡ trụ)
    if (is_right) {
        translate([x_wall_outer - WALL_T, my - cradle_len/2.0 + cradle_y_offset, 0])
            cube([WALL_T, cradle_len, PILLAR_Z_TOP]);
    } else {
        translate([x_wall_outer, my - cradle_len/2.0 + cradle_y_offset, 0])
            cube([WALL_T, cradle_len, PILLAR_Z_TOP]);
    }
    
    // 3. Khối ổ đỡ Saddle Cradle đỡ nửa dưới thân động cơ GA25
    if (is_right) {
        translate([x_wall_outer - CRADLE_W, my - cradle_len/2.0 + cradle_y_offset, 0])
            cube([CRADLE_W, cradle_len, 18.0]);
    } else {
        translate([x_wall_outer, my - cradle_len/2.0 + cradle_y_offset, 0])
            cube([CRADLE_W, cradle_len, 18.0]);
    }
}

// MODULE KHOÉT RỖNG ĐỘNG CƠ GA25 & 6 LỖ M3 PCD 17MM (SUBTRACTIVE CUTS)
module motor_mount_cuts(is_right = false, my = 24.0, max_cut_y = 999.0) {
    sx = is_right ? 1 : -1;
    x_wall_outer = sx * CHASSIS_W / 2.0;
    
    // 1. Khoét hốc lắp động cơ d=25.4mm
    if (is_right) {
        translate([x_wall_outer - CRADLE_W - 0.1, my, Z_SHAFT])
            rotate([0, 90, 0])
                cylinder(d=25.4, h=CRADLE_W + BOSS_OUT - FLANGE_T + 0.1);
    } else {
        intersection() {
            translate([x_wall_outer - BOSS_OUT + FLANGE_T, my, Z_SHAFT])
                rotate([0, 90, 0])
                    cylinder(d=25.4, h=CRADLE_W + BOSS_OUT - FLANGE_T + 0.1);
            if (max_cut_y < 500.0) {
                translate([-CHASSIS_W/2.0 - 10.0, -50.0, -10.0])
                    cube([CHASSIS_W, max_cut_y + 50.0, 100.0]);
            }
        }
    }
    
    // 2. Lỗ trục 7mm dạng giọt nước Teardrop in FDM (d=7.2mm kèm dung sai co ngót)
    if (is_right) {
        translate([x_wall_outer + BOSS_OUT - FLANGE_T - 1.0, my, Z_SHAFT])
            teardrop_hole_x(d=7.2, h=FLANGE_T + 2.0);
    } else {
        translate([x_wall_outer - BOSS_OUT - 1.0, my, Z_SHAFT])
            teardrop_hole_x(d=7.2, h=FLANGE_T + 2.0);
    }
    
    // 3. Đủ 6 lỗ ốc M3 PCD 17mm (bán kính 8.5mm, chia đều 60 độ)
    for (a = [0:60:300]) {
        hy = my + 8.5 * cos(a);
        hz = Z_SHAFT + 8.5 * sin(a);
        if (is_right) {
            translate([x_wall_outer + BOSS_OUT - FLANGE_T - 1.0, hy, hz])
                teardrop_hole_x(d=3.4, h=FLANGE_T + 2.0);
        } else {
            translate([x_wall_outer - BOSS_OUT - 1.0, hy, hz])
                teardrop_hole_x(d=3.4, h=FLANGE_T + 2.0);
        }
    }
}

// ====================================================================
// MODULE KHUNG GẦM SLIM 120 HOÀN CHỈNH (chassis_base_slim120_omni)
// ====================================================================
module chassis_base_slim120_omni() {
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

            // 3. 4 CỤM BỆ MOTOR GA25 ZIGZAG SO LE NGUYÊN KHỐI
            // Motor 1: Rear-Left (RL) - Y = 24.0mm
            motor_mount_solid(is_right = false, my = Y_RL, cradle_len = 32.0, cradle_y_offset = 0);

            // Motor 2: Rear-Right (RR) - Y = 50.0mm (Khoảng lệch Y=26mm > 24.4mm đường kính motor)
            motor_mount_solid(is_right = true,  my = Y_RR, cradle_len = 32.0, cradle_y_offset = 0);

            // Motor 3: Front-Left (FL) - Y = 90.0mm (Vươn tối đa đỡ đầu xe trái, cách ly trụ pin Y=100)
            motor_mount_solid(is_right = false, my = Y_FL, cradle_len = 26.0, cradle_y_offset = -2.0);

            // Motor 4: Front-Right (FR) - Y = 142.0mm (Dưới vòm tháp nâng 01C)
            motor_mount_solid(is_right = true,  my = Y_FR, cradle_len = 32.0, cradle_y_offset = 0);

            // 4. 4 TRỤ ĐỠ TẦNG 1 (BATTERY DECK PILLARS) - KHỚP 100% HOLE_X=±35, HOLE_Y=38 & 100
            for (sx = [-1, 1]) {
                for (py = [PILLAR_Y_REAR, PILLAR_Y_FRNT]) {
                    x_pos = (sx < 0) ? -CHASSIS_W/2.0 - 0.5 : CHASSIS_W/2.0 - PILLAR_W + 0.5;
                    translate([x_pos, py - PILLAR_L/2.0, 0])
                        cube([PILLAR_W, PILLAR_L, PILLAR_Z_TOP]);
                }
            }

            // 5. CẢN TRƯỚC TÍCH HỢP HỘC ToF VL53L0X - NGUYÊN KHỐI KHÔNG KHE HỞ
            hull() {
                translate([-CHASSIS_W/2.0, 164.5, 0])
                    cube([CHASSIS_W, 1.5, 14.0]);
                translate([-28.0, Y_END - 2.0, 0])
                    cube([56.0, 2.0, 14.0]);
            }

            // 6. GỜ ĐỊNH VỊ CHÂN THÁP NÂNG (01B & 01C)
            translate([-28.5, 126.0, FLOOR_T]) cube([2.0, 26.0, 3.0]);
            translate([ 26.5, 126.0, FLOOR_T]) cube([2.0, 26.0, 3.0]);

            // 7. GỜ GIA CƯỜNG ĐIỂM TỰA CHỐNG BẬP BÊNH / CHỐNG CHÚI (REINFORCED CASTER BOSSES)
            // 4 Cụm bệ gá bi mắt trâu / vấu trượt gầm xe
            for (cx = [-CASTER_X, CASTER_X]) {
                for (cy = [CASTER_Y_REAR, CASTER_Y_FRNT]) {
                    translate([cx - 9.0, cy - 10.0, FLOOR_T])
                        cube([18.0, 20.0, 3.0]);
                }
            }
        }

        // ================= KHOÉT RỖNG CSG & LỖ GIỌT NƯỚC 45° =================

        // 1. KHOÉT 4 VỊ TRÍ ĐỘNG CƠ GA25, LỖ TRỤC 7.2MM & 6 LỖ M3 PCD 17MM
        motor_mount_cuts(is_right = false, my = Y_RL);
        motor_mount_cuts(is_right = true,  my = Y_RR);
        motor_mount_cuts(is_right = false, my = Y_FL, max_cut_y = 97.0);
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
        translate([-8.0, CHASSIS_L_EFF + Y_START - 26.0, -0.5])
            cube([16.0, 8.0, FLOOR_T + 1.0]);

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

        // 6. 4 CỤM ĐIỂM TỰA TRỢ LỰC CHỐNG CHÚI / BẬP BÊNH (CASTER BALL Ø12MM & M3 SCREW MOUNTS)
        // Khoét hốc định vị bi Ø14mm sâu 1.5mm từ mặt đáy Z=0 lên
        // Khoét 2 lỗ vít M3 (khoảng cách 16mm) bắt cứng bệ bi mắt trâu hoặc vấu trượt Teflon
        for (cx = [-CASTER_X, CASTER_X]) {
            for (cy = [CASTER_Y_REAR, CASTER_Y_FRNT]) {
                // Hốc lõm định vị bi lăn / chén đỡ
                translate([cx, cy, -0.5])
                    cylinder(d=CASTER_REC_D, h=CASTER_REC_H + 0.5);
                // 2 lỗ bắt vít M3 xuyên sàn
                translate([cx, cy - CASTER_HOLE_SP/2.0, -1.0])
                    cylinder(d=3.4, h=FLOOR_T + 5.0);
                translate([cx, cy + CASTER_HOLE_SP/2.0, -1.0])
                    cylinder(d=3.4, h=FLOOR_T + 5.0);
            }
        }

        // 7. RÃNH THOÁT NHIỆT & GIẢM TRỌNG LƯỢNG SÀN XE (LIGHTWEIGHT VENT SLOTS)
        for (vy = [38.0, 68.0]) {
            translate([-12.0, vy, -0.5])
                cube([24.0, 10.0, FLOOR_T + 1.0]);
        }

        // 8. VÁT GÓC 45° ĐUÔI XE & MŨI XE (TỐI ƯU XOAY TRÒN KHÔNG VƯỚNG)
        translate([-CHASSIS_W/2.0 - 5.0, Y_START - 5.0, -1.0])
            rotate([0, 0, 45])
                cube([14.0, 14.0, WALL_H + 5.0]);
        translate([CHASSIS_W/2.0 + 5.0, Y_START - 5.0, -1.0])
            rotate([0, 0, 45])
                cube([14.0, 14.0, WALL_H + 5.0]);
    }
}

// Render ở chế độ part mặc định
if (DISPLAY_MODE == "part") {
    chassis_base_slim120_omni();
}
