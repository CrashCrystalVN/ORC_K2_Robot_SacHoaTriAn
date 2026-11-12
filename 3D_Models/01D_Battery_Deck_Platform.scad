// ====================================================================
// DỰ ÁN: ROBOT THI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & 20/11
// CHI TIẾT: SÀN ĐỠ PIN TẦNG 1 TẬN DỤNG TRỤC Z (BATTERY DECK PLATFORM)
// FILE: 01D_Battery_Deck_Platform.scad
// PHIÊN BẢN V2.0: ĐỒNG BỘ TOÀN DIỆN 100% VỚI KHUNG GẦM ZIGZAG 76MM & K2 HUB
// ĐẶT TRÊN 4 TRỤ KHUNG GẦM ZIGZAG TẠI Z = 34.0 MM - ZERO ERROR ALIGNMENT
// ====================================================================

$fn = 36;

DECK_W = 76.0;  // Bề rộng bằng đúng thân xe Zigzag (mm)
DECK_L = 78.0;  // Chiều dài sàn đỡ pin (mm)
DECK_T = 3.5;   // Độ dày sàn in FDM (mm)

// TỌA ĐỘ TÂM ĐỐI XỨNG CỦA CÁC LỖ BẮT VÍT:
// 1. 4 Lỗ bắt ốc xuống 4 trụ chassis Zigzag (Khớp 100% với X=±35, Y=38 & 100mm):
// Khi sàn đặt tại tâm Y = 69.0mm trên chassis:
// Y_local = 38.0 - 69.0 = -31.0mm và 100.0 - 69.0 = +31.0mm
BASE_HOLE_X = 35.0;
BASE_HOLE_Y = 31.0;

// 2. 4 Lỗ cọc Standoff M3 nâng bo mạch K2 Hub (Khớp 100% với full_assembly X=±28, Y=45 & 95mm):
// Y_local = 45.0 - 69.0 = -24.0mm và 95.0 - 69.0 = +26.0mm
HUB_HOLE_X  = 28.0;
HUB_HOLE_Y1 = -24.0;
HUB_HOLE_Y2 =  26.0;

// ====================================================================
// MODULE SÀN ĐỠ PIN TẦNG 1 (GỐC TỌA ĐỘ TẠI TÂM HÌNH HỌC X=0, Y=0)
// ====================================================================
module battery_deck_platform() {
    difference() {
        union() {
            // 1. Tấm sàn chính phẳng 100% tại Z = 0
            translate([-DECK_W/2.0, -DECK_L/2.0, 0])
                cube([DECK_W, DECK_L, DECK_T]);

            // 2. Gờ định vị 4 góc chống xô lệch pin 2S2P (Lòng gờ rộng 40.0mm x dài 72.0mm)
            for (sx = [-20.0, 18.0]) {
                for (sy = [-DECK_L/2.0 + 4.0, DECK_L/2.0 - 14.0]) {
                    translate([sx, sy, DECK_T])
                        cube([2.0, 10.0, 3.0]);
                }
            }
        }

        // ================= KHOÉT LỖ BẮT ỐC & KHE ĐAI VELCRO =================

        // 1. 4 Lỗ ốc M3 bắt xuống 4 trụ khung gầm Zigzag (Ø3.4mm xuyên + vát chìm Ø6.2mm)
        for (bx = [-BASE_HOLE_X, BASE_HOLE_X]) {
            for (by = [-BASE_HOLE_Y, BASE_HOLE_Y]) {
                translate([bx, by, -1.0]) cylinder(d=3.4, h=DECK_T + 2.0);
                translate([bx, by, DECK_T - 1.5]) cylinder(d=6.2, h=2.0);
            }
        }

        // 2. 4 Khe luồn đai Velcro bản 20mm (3.5 x 22.0 mm) ôm sát thành pin 2S2P (X = ±21.5mm)
        // Cách xa cọc Standoff K2 Hub > 4.5mm -> Loại bỏ 100% va chạm, giữ trọn vẹn lỗ cọc!
        for (vx = [-21.5, 21.5]) {
            for (vy = [-12.0, 12.0]) {
                translate([vx - 1.75, vy - 11.0, -1.0])
                    cube([3.5, 22.0, DECK_T + 2.0]);
            }
        }

        // 3. 4 Lỗ cọc Standoff M3 nâng bo mạch K2 Control Hub (Ø3.2mm xuyên + vát chìm đáy Ø6.0mm)
        for (hx = [-HUB_HOLE_X, HUB_HOLE_X]) {
            for (hy = [HUB_HOLE_Y1, HUB_HOLE_Y2]) {
                translate([hx, hy, -1.0]) cylinder(d=3.2, h=DECK_T + 2.0);
                translate([hx, hy, -1.0]) cylinder(d=6.0, h=1.5);
            }
        }

        // 4. Lỗ thông dây điện luồn jack nguồn XT30 / XH2.54 từ pin xuống driver
        translate([-10.0, -6.0, -1.0])
            cube([20.0, 12.0, DECK_T + 2.0]);
    }
}

// Render chính (Xuất part chuẩn in FDM tại tâm Z=0)
battery_deck_platform();
