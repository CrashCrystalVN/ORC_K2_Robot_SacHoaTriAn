"""
generate_redesigned_parts.py
Script thiết kế lại và xuất các file 3D STL tối ưu V5.0:
1. Tấm bắt bo mạch ORC K2 Control Hub (K2 Adapter Plate V5.0 & Monolithic Riser V5.0):
   - Đôn cao 18.0mm (tạo khe hở an toàn 4.0mm vượt nắp kẹp motor sau Z=36mm, triệt tiêu 100% va chạm).
   - 4 Hốc nhét tán M3 ngang (Side-entry Nut Slots) trượt từ mép ngoài x=+-63mm vào, đáy kín 1.2mm.
   - Trình tự lắp ráp chuẩn 2 bước: Bắt bệ xuống khung gầm trước (lỗ chìm Ø6.5mm) -> Đặt K2 Hub và siết ốc từ trên xuống vào tán ngang mà không cần luồn tay xuống gầm!
2. 2 Nẹp ôm động cơ GA25 phía sau (Rear Motor Clamps Left / Right / Universal V4.3):
   - Vòm bán nguyệt Ø26.2mm kèm miệng loe 45° (Ø27.5mm) ôm trọn mọi loại hộp số giảm tốc to.
   - Mép trong thu hẹp suốt chiều dài về X = +-40.5mm (cách trụ MCU cũ 2.5mm tuyệt đối).
3. Cụm Servo S1 nâng hạ & Cánh tay đòn V5.0 (Chuẩn Đĩa tròn Servo MG996R & Chống cấn ốc 100%):
   - Tháp nâng phải (01C V5.0): Hốc chìm tán M3 lục giác sâu 2.6mm ở mặt trong + Rãnh lượn mở rộng 1.0mm -> Triệt tiêu 100% cấn ốc với tay nâng.
   - Tay nâng dưới chữ H (03 V5.0): Hốc tròn âm Ø20.8mm ôm khít đĩa tròn MG996R + 8 lỗ M3 trên PCD Ø14mm + lỗ tâm Ø6.5mm tra vít spline + in phẳng 100% tại Z=0.
   - Khối khóa đĩa tròn S1 rời (08 V5.0): Khớp nối nhanh dành cho ai đã in tay nâng cũ, cắm vừa rãnh chữ nhật cũ mà không cần in lại cả cánh tay!
"""

import os
import subprocess
import struct
import math
import re

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
STL_DIR = os.path.join(BASE_DIR, "3D_Models")
OPENSCAD_COM = r"C:\Program Files\OpenSCAD\openscad.com"

os.makedirs(STL_DIR, exist_ok=True)

# ====================================================================
# OPENSCAD DEFINITIONS
# ====================================================================
SCAD_LIBRARY = """$fn = 64;

module teardrop_hole_x(d = 9.0, h = 10.0) {
    r = d / 2;
    side = r * sqrt(2);
    union() {
        rotate([0, 90, 0]) cylinder(d=d, h=h);
        translate([0, 0, r * 0.5])
            rotate([45, 0, 0])
                translate([0, -side/2, -side/2])
                    cube([h, side, side]);
    }
}

// ====================================================================
// TIỆN ÍCH RÃNH ĐƯỜNG RAY KHÓA TÁN M3 ĐÁY KÍN CHỐNG RƠI & CHỐNG XOAY V9.0 (DFM 0% SUPPORT)
// - Giải quyết triệt để lỗi rơi tán M3 xuống gầm xe khi bắt Plate lên khung trước:
//   + Sàn dày T_deck = 6.0mm có hệ DẢI CẦU ĐỠ ĐÁY TÁN (Train-Rail Retention Bridges) dày 1.2mm
//     bắc ngang qua rãnh 5.65mm (cầu phẳng 1D dài chỉ 5.65mm -> Máy in FDM bắc cầu thẳng tắp 0% Support!).
//   + Tán M3 (5.5 x 6.08 x 2.4mm) trượt êm trên mặt đường ray 1.2mm, KHÔNG BAO GIỜ RƠI XUỐNG GẦM,
//     đồng thời bị 2 vách bên rộng 5.65mm khóa cứng 6 cạnh KHÔNG THỂ XOAY khi siết ốc từ trên xuống!
//   + Cửa nạp tán M3 từ mép sườn ngoài (Side-Entry Port) & Hốc nạp tán (Drop-In Pocket) tiện lợi.
// ====================================================================
module slot_m3_with_nut_channel_z0(x1, y1, x2, y2, T_deck = 6.0, nut_w = 5.65, slot_d = 3.4) {
    dx = x2 - x1;
    dy = y2 - y1;
    L = sqrt(dx*dx + dy*dy);
    ang = atan2(dy, dx);
    cx = 0.5 * (x1 + x2);
    cy = 0.5 * (y1 + y2);

    // 1. Khe xuyên suốt cho thân ốc M3 (Ø3.4mm) từ mặt trên xuống mặt dưới:
    hull() {
        translate([x1, y1, -1.0]) cylinder(d=slot_d, h=T_deck + 2.0);
        translate([x2, y2, -1.0]) cylinder(d=slot_d, h=T_deck + 2.0);
    }

    // 2. Tầng rãnh khóa tán M3 chống xoay (rộng 5.65mm, Z = 1.2 .. 3.9mm)
    //    kèm mái côn 45° tự đỡ (Z = 3.85 .. 5.0mm) -> Giữ nguyên đáy kín Z = 0.0 .. 1.2mm!
    hull() {
        translate([x1, y1, 1.2]) cylinder(d=nut_w, h=2.7);
        translate([x2, y2, 1.2]) cylinder(d=nut_w, h=2.7);
    }
    hull() {
        translate([x1, y1, 3.85]) cylinder(d1=nut_w, d2=slot_d, h=1.15);
        translate([x2, y2, 3.85]) cylinder(d1=nut_w, d2=slot_d, h=1.15);
    }

    // 3. Hốc nạp tán M3 ở tâm rãnh (mở thông đáy Z = -0.1..3.9mm dài 6.2mm để nhét tán M3 vào đường ray,
    //    khi trượt tán lệch khỏi tâm >= 3mm thì sàn đáy kín Z = 0..1.2mm đỡ chặt tán không bao giờ rơi!):
    translate([cx, cy, 0])
        rotate([0, 0, ang]) {
            hull() {
                translate([-1.2, 0, -0.1]) cylinder(d=nut_w + 0.15, h=4.0);
                translate([ 1.2, 0, -0.1]) cylinder(d=nut_w + 0.15, h=4.0);
            }
        }
}

module slot_m3_with_nut_channel_zbot(x1, y1, x2, y2, Z_bot = 38.0, T_deck = 6.0, nut_w = 5.65, slot_d = 3.4) {
    dx = x2 - x1;
    dy = y2 - y1;
    ang = atan2(dy, dx);
    cx = 0.5 * (x1 + x2);
    cy = 0.5 * (y1 + y2);

    // 1. Khe xuyên suốt cho thân ốc M3 (Ø3.4mm):
    hull() {
        translate([x1, y1, Z_bot - 1.0]) cylinder(d=slot_d, h=T_deck + 2.0);
        translate([x2, y2, Z_bot - 1.0]) cylinder(d=slot_d, h=T_deck + 2.0);
    }

    // 2. Tầng rãnh khóa tán M3 chống xoay (rộng 5.65mm, nằm giữa sàn Z = Z_bot + 1.2 .. Z_bot + 3.9mm)
    //    kèm mái côn 45° tự đỡ (Z = Z_bot + 3.85 .. Z_bot + 5.0mm):
    //    -> Lớp đáy Z_bot .. Z_bot + 1.2mm tạo thành ĐƯỜNG RAY ĐÁY KÍN giữ tán M3 không bao giờ rơi xuống gầm!
    //    -> Khi in lật úp (Z_top chạm bàn in), lớp đáy 1.2mm chỉ bắc cầu phẳng ngang 5.65mm -> 0% Support!
    hull() {
        translate([x1, y1, Z_bot + 1.2]) cylinder(d=nut_w, h=2.7);
        translate([x2, y2, Z_bot + 1.2]) cylinder(d=nut_w, h=2.7);
    }
    hull() {
        translate([x1, y1, Z_bot + 3.85]) cylinder(d1=nut_w, d2=slot_d, h=1.15);
        translate([x2, y2, Z_bot + 3.85]) cylinder(d1=nut_w, d2=slot_d, h=1.15);
    }

    // 3. Cửa nạp tán M3 (Drop-In Loading Gate dài 6.2mm tại tâm rãnh):
    //    Cho phép ấn tán M3 từ mặt dưới vào rãnh rồi trượt dọc theo đường ray đáy kín 1.2mm!
    translate([cx, cy, 0])
        rotate([0, 0, ang]) {
            hull() {
                translate([-1.2, 0, Z_bot - 0.1]) cylinder(d=nut_w + 0.15, h=4.0);
                translate([ 1.2, 0, Z_bot - 0.1]) cylinder(d=nut_w + 0.15, h=4.0);
            }
        }
}

module side_nut_entry_port_z0(sx, y_pos, T_deck = 6.0, nut_w = 5.75) {
    // Cửa nhét tán M3 trực tiếp từ mép sườn ngoài (|X| = 60.0mm) vào rãnh đường ray đáy kín (Z = 1.2..3.9mm):
    hull() {
        translate([sx * 54.0, y_pos, 1.2]) cylinder(d=nut_w, h=2.7);
        translate([sx * 61.0, y_pos, 1.2]) cylinder(d=nut_w, h=2.7);
    }
    hull() {
        translate([sx * 54.0, y_pos, 3.85]) cylinder(d1=nut_w, d2=3.4, h=1.15);
        translate([sx * 61.0, y_pos, 3.85]) cylinder(d1=nut_w, d2=3.4, h=1.15);
    }
}

module side_nut_entry_port_zbot(sx, y_pos, Z_bot = 38.0, T_deck = 6.0, nut_w = 5.75) {
    // Cửa nhét tán M3 trực tiếp từ mép sườn ngoài (|X| = 60.0mm) vào rãnh đường ray đáy kín (Z = Z_bot+1.2..3.9mm):
    hull() {
        translate([sx * 54.0, y_pos, Z_bot + 1.2]) cylinder(d=nut_w, h=2.7);
        translate([sx * 61.0, y_pos, Z_bot + 1.2]) cylinder(d=nut_w, h=2.7);
    }
    hull() {
        translate([sx * 54.0, y_pos, Z_bot + 3.85]) cylinder(d1=nut_w, d2=3.4, h=1.15);
        translate([sx * 61.0, y_pos, Z_bot + 3.85]) cylinder(d1=nut_w, d2=3.4, h=1.15);
    }
}

module slot_m3_counterbored_top(x1, y1, x2, y2, Z_base = 0.0, T_deck = 6.0, cb_d = 6.8, cb_h = 2.0, slot_d = 3.4) {
    hull() {
        translate([x1, y1, Z_base - 1.0]) cylinder(d=slot_d, h=T_deck + 2.0);
        translate([x2, y2, Z_base - 1.0]) cylinder(d=slot_d, h=T_deck + 2.0);
    }
    hull() {
        translate([x1, y1, Z_base + T_deck - cb_h]) cylinder(d=cb_d, h=cb_h + 1.0);
        translate([x2, y2, Z_base + T_deck - cb_h]) cylinder(d=cb_d, h=cb_h + 1.0);
    }
}

// ====================================================================
// 1. TẤM BỆ ADAPTER PHẲNG ĐA NĂNG LÙI HẬU NÉ THÁP GẮP TRỤ V9.0 (K2 HUB CANTILEVER REAR-SHIFT PLATE V9.0)
// - Thiết kế lại toàn bộ để TRIỆT TIÊU 100% VA CHẠM VỚI CẤU TRÚC GẮP TRỤ (2 Tháp nâng 01B/01C & Servo S1):
//   1. KIẾN TRÚC LÙI HẬU (CANTILEVER REAR-SHIFT: Y in [-8.0, +82.0mm]):
//      + Mặt sàn chính dừng tại Y = 82.0mm -> Cách lưng 2 Tháp Nâng (Y = 105.0mm) tới 23.0mm (2.3cm)
//        và cách tai sau + ốc + dây cáp của Servo S1 (Y = 107.65mm) tới 25.65mm!
//      + Khi lắp K2 Control Hub (Y in [-6.0, +80.0mm]), mặt trước K2 Hub cách 2 Tháp Nâng đúng 25.0mm,
//        dư không gian thoáng đãng để cắm toàn bộ giắc Motor M1..M4, Encoder E1..E2 và Servo S1..S4!
//   2. 2 TAY VƯƠN BẮT TRỤ TRƯỚC LỘ THIÊN (Y in [82.0, 102.0mm], |X| in [29.2, 39.2mm]):
//      + Nằm hoàn toàn BÊN NGOÀI vách 2 Tháp Nâng (|X| <= 28.0mm -> khe hở ngang 1.2mm) và DỪNG TRƯỚC
//        mặt sau 2 Tháp Nâng & Gờ định vị ngoài (Y = 105.0mm -> khe hở dọc 3.0mm)!
//      + Lỗ bắt trụ trước (Y = 99.0mm) và lỗ khóa nhanh vào khung đôn (Y = 88.5mm) nằm LỘ THIÊN 100%
//        ở phía trước bo mạch K2 Control Hub (Y <= 80.0mm) -> Đưa tô-vít thẳng đứng từ trên xuống cực dễ!
//   3. HỆ RÃNH ĐƯỜNG RAY KHÓA TÁN M3 ĐÁY KÍN CHỐNG RƠI (CAPTIVE BLIND-FLOOR NUT CHANNELS):
//      + Có sàn đáy kín dày 1.2mm giữ tán M3 KHÔNG BAO GIỜ RƠI XUỐNG GẦM XE + cửa nhét tán từ mép sườn!
//      + Rãnh 2 chiều bao phủ |X| từ 30.0mm đến 55.5mm (khoảng cách tâm 60..111mm) và ΔY từ 34..82mm.
// ====================================================================
module k2_adapter_plate_flat() {
    T_deck = 6.0;
    difference() {
        union() {
            // 1. Mặt sàn chính phẳng tuyệt đối 100% lùi hậu (120.0 x 90.0 x 6.0 mm, X in [-60, 60], Y in [-8, 82]):
            //    Dừng tại Y = 82.0mm -> Cách 2 Tháp Nâng (Y=105) tới 23.0mm và cách Servo S1 (Y=107.65) tới 25.65mm!
            translate([-60.0, -8.0, 0.0])
                cube([120.0, 90.0, T_deck]);
                
            // 2. Hai Tai Bắt Ốc Lộ Thiên Phía Sau (X in [+-25.0, +-41.0], Y in [-18.0, -8.0]):
            //    Vươn ra ngoài đuôi K2 Hub (Y >= -6.0) để bắt khóa nhanh từ trên xuống!
            for (sx = [-1, 1]) {
                translate([sx * 33.0 - 8.0, -18.0, 0.0])
                    cube([16.0, 11.0, T_deck]);
            }
            
            // 3. Hai Tay Vươn Bắt Trụ Trước & Khóa Nhanh Lộ Thiên (|X| in [29.2, 39.2], Y in [81.0, 102.0]):
            //    - Mép trong |X| = 29.2mm (cách vách ngoài Tháp Nâng |X| = 28.0mm đúng 1.2mm!)
            //    - Mũi trước Y = 102.0mm (dừng trước Tháp Nâng & Gờ định vị Y = 105.0mm đúng 3.0mm!)
            //    - Giữa 2 tay (X in [-29.2, +29.2]) là Hốc Chữ U rộng 58.4 x 23.0mm né hoàn toàn Cấu Trúc Gắp Trụ!
            for (sx = [-1, 1]) {
                translate([sx * 34.2 - 5.0, 81.0, 0.0])
                    cube([10.0, 21.0, T_deck]);
            }
        }
        
        // Ô thoáng trung tâm (42 x 36 mm, X in [-21, 21], Y in [19, 55]) luồn dây Pin 2S & thoáng khí:
        translate([-21.0, 19.0, -1.0])
            cube([42.0, 36.0, T_deck + 2.0]);
            
        // A. TỔ HỢP RÃNH ĐƯỜNG RAY KHÓA TÁN M3 ĐÁY KÍN 2 CHIỀU (CAPTIVE 2D SLOTTED MATRIX) TẠI 4 GÓC K2 HUB:
        //    - Bao phủ |X| liên tục từ 30.0mm đến 55.5mm (khoảng cách lỗ ngang 60..111mm: vừa 64, 72, 80, 88, 96, 100, 104mm!)
        //    - Góc Sau: Y từ -4.5 đến 19.5mm | Góc Trước: Y từ 54.5 đến 78.5mm (ΔY từ 35mm đến 83mm: vừa 48, 56, 64, 68, 72, 76mm!)
        //    - Đáy kín 1.2mm giữ tán M3 không bao giờ rơi + Cửa nhét tán ngang từ mép sườn |X| = 60.0mm!
        for (sx = [-1, 1]) {
            for (abs_x = [32.0, 40.0, 48.0, 54.0]) {
                slot_m3_with_nut_channel_z0(sx * abs_x, -4.5, sx * abs_x, 19.5, T_deck);
                slot_m3_with_nut_channel_z0(sx * abs_x, 54.5, sx * abs_x, 78.5, T_deck);
            }
            for (hy_rear = [-2.0, 5.0, 12.0, 18.0]) {
                slot_m3_with_nut_channel_z0(sx * 30.0, hy_rear, sx * 55.5, hy_rear, T_deck);
                side_nut_entry_port_z0(sx, hy_rear, T_deck);
            }
            for (hy_front = [56.0, 62.0, 69.0, 76.0]) {
                slot_m3_with_nut_channel_z0(sx * 30.0, hy_front, sx * 55.5, hy_front, T_deck);
                side_nut_entry_port_z0(sx, hy_front, T_deck);
            }
        }
        
        // B. RÃNH TRƯỢT 2 CHIỀU (2D X-Y SLOTS) BẮT XUỐNG 4 TRỤ KHUNG GẦM (X = +-33.0, Y = 49.0 & 99.0):
        //    - Trụ sau (Y = 49.0) & Trụ trước lộ thiên trên tay vươn (Y = 98.0):
        for (sx = [-1, 1]) {
            // Trụ sau (Y = 49.0 +- 3.5mm, |X| = 31.5..35.0mm):
            hull() {
                translate([sx * 31.5, 45.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                translate([sx * 35.0, 45.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                translate([sx * 31.5, 52.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                translate([sx * 35.0, 52.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
            }
            hull() {
                translate([sx * 31.5, 45.5, T_deck - 2.2]) cylinder(d=7.0, h=3.2);
                translate([sx * 35.0, 45.5, T_deck - 2.2]) cylinder(d=7.0, h=3.2);
                translate([sx * 31.5, 52.5, T_deck - 2.2]) cylinder(d=7.0, h=3.2);
                translate([sx * 35.0, 52.5, T_deck - 2.2]) cylinder(d=7.0, h=3.2);
            }
            // Trụ trước lộ thiên trên Tay Vươn Trước (Y = 95.5..99.5mm, |X| = 32.0..35.5mm):
            hull() {
                translate([sx * 32.0, 95.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                translate([sx * 35.5, 95.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                translate([sx * 32.0, 99.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                translate([sx * 35.5, 99.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
            }
            hull() {
                translate([sx * 32.0, 95.5, T_deck - 2.2]) cylinder(d=6.8, h=3.2);
                translate([sx * 35.5, 95.5, T_deck - 2.2]) cylinder(d=6.8, h=3.2);
                translate([sx * 32.0, 99.5, T_deck - 2.2]) cylinder(d=6.8, h=3.2);
                translate([sx * 35.5, 99.5, T_deck - 2.2]) cylinder(d=6.8, h=3.2);
            }
        }
        
        // C. 4 RÃNH KHÓA NHANH LỘ THIÊN (EXPOSED QUICK-LOCK SLOTS) BẮT LÊN KHUNG CHÂN ĐÔN 01D_Base_Riser_Frame:
        //    - 2 Tai Sau Lộ Thiên: X = +-33.0mm, Y = -15.0 .. -11.0mm (nằm sau K2 Hub Y >= -6.0mm)
        //    - 2 Tai Trước Lộ Thiên: X = +-34.0mm, Y = 86.0 .. 90.0mm (nằm trước K2 Hub Y <= 80.0mm & sau Tháp Nâng 15mm!)
        for (sx = [-1, 1]) {
            slot_m3_counterbored_top(sx * 31.5, -13.0, sx * 34.5, -13.0, 0.0, T_deck);
            slot_m3_counterbored_top(sx * 33.0, -15.0, sx * 33.0, -11.0, 0.0, T_deck);
            slot_m3_counterbored_top(sx * 32.5, 88.0, sx * 35.5, 88.0, 0.0, T_deck);
            slot_m3_counterbored_top(sx * 34.0, 86.0, sx * 34.0, 90.0, 0.0, T_deck);
        }
        
        // D. HỆ LƯỚI LỖ ĐA NĂNG CHUẨN OHSTEM 8.0MM (8MM PITCH MATRIX) DỌC HAI BÊN SƯỜN & TRUNG TÂM:
        for (sx = [-1, 1]) {
            for (gx = [44.0, 52.0]) {
                for (gy = [25.0, 33.0, 41.0]) {
                    slot_m3_with_nut_channel_z0(sx * gx, gy - 1.5, sx * gx, gy + 1.5, T_deck);
                }
            }
        }
        for (gx = [-16.0, -8.0, 0.0, 8.0, 16.0]) {
            for (gy = [0.0, 8.0, 64.0, 72.0]) {
                slot_m3_with_nut_channel_z0(gx - 1.5, gy, gx + 1.5, gy, T_deck);
            }
        }
    }
}

// ====================================================================
// 2. KHUNG CHÂN ĐÔN ĐA NĂNG LÙI HẬU NÉ THÁP GẮP TRỤ V9.0 (01D_Base_Riser_Frame)
// - Thiết kế lại toàn bộ để KHÔNG BAO GIỜ VA CHẠM VỚI 2 THÁP NÂNG (01B & 01C) VÀ SERVO S1:
//   1. Toàn bộ phần chân và tay trước giới hạn ở |X| in [29.2, 39.2mm] và dừng tại Y = 102.0mm:
//      + Cách vách ngoài 2 Tháp Nâng (|X| = 28.0mm) đúng 1.2mm theo phương X!
//      + Dừng trước mặt lưng 2 Tháp Nâng & Gờ định vị (Y = 105.0mm) đúng 3.0mm theo phương Y!
//      + Khoảng giữa X in [-29.2, +29.2mm] từ Y = 78.0 đến 105.0mm TRỐNG HOÀN TOÀN 100%!
//   2. 4 Chân bắt xuống khung gầm (X = +-33.0, Y = 49.0 & 99.0) hạ thẳng đứng (Drop-In), có giếng mở
//      rộng rãi từ mặt trên xuống bậc đế dày 4.5mm (Z = 22.0..26.5mm) -> Dùng ốc ngắn M3x10/12mm cực dễ!
//   3. 4 Tai Khóa Nhanh Lộ Thiên (Y = -13.0mm phía sau & Y = 88.0mm phía trước) có sẵn Hốc Giữ Tán M3
//      Đáy Kín Chống Rơi -> Bắt tấm Plate + K2 Hub từ trên xuống hoàn toàn bên ngoài vỏ K2 Hub!
//   4. Đặt in lật úp 180° (mặt Z = 38.0mm nằm sát bàn in Z = 0): IN 0% SUPPORT!
// ====================================================================
module k2_base_riser_frame() {
    Z_top = 38.0;
    difference() {
        union() {
            for (sx = [-1, 1]) {
                // 1. Hai Chân Trụ Sau (|X| in [26.5, 39.2], Y in [45.0, 56.5], Z in [22.0, 38.0]):
                //    Cách nẹp motor sau (|X|=40.5 -> khe hở 1.3mm) và thân motor sau (Y<=44.5) an toàn tuyệt đối!
                translate([sx * 32.85 - 6.35, 45.0, 22.0])
                    cube([12.7, 11.5, Z_top - 22.0]);
                    
                // 2. Hai Chân & Tay Trụ Trước Né Tháp Nâng (|X| in [29.2, 39.2], Y in [82.0, 102.0], Z in [22.0, 38.0]):
                //    - |X| >= 29.2mm (nằm ngoài Tháp Nâng |X| <= 28.0mm đúng 1.2mm!)
                //    - Y <= 102.0mm (dừng trước Tháp Nâng Y = 105.0mm đúng 3.0mm!)
                translate([sx * 34.2 - 5.0, 82.0, 22.0])
                    cube([10.0, 20.0, Z_top - 22.0]);
                    
                // 3. Dầm dọc trên nối liền từ Tai Sau (Y = -18.0) đến Tay Trước (Y = 85.0) tại Z in [31.0, 38.0]:
                translate([sx * 33.5 - 5.7, -18.0, 31.0])
                    cube([11.4, 103.0, 7.0]);
                    
                // 4. Khối Tai Khóa Sau Lộ Thiên dày 8mm (|X| in [25.5, 40.5], Y in [-18.0, -7.0], Z in [30.0, 38.0]):
                translate([sx * 33.0 - 7.5, -18.0, 30.0])
                    cube([15.0, 11.0, 8.0]);
            }
            
            // 5. Hai Thanh Giằng Ngang Chữ H nối Trái - Phải tại Y in [12.0, 20.0] và Y in [66.0, 74.0], Z in [32.0, 38.0]:
            //    (Đặt tại Y <= 74.0mm, cách 2 Tháp Nâng Y=105.0mm tới 31.0mm!)
            translate([-33.0, 12.0, 32.0]) cube([66.0, 8.0, 6.0]);
            translate([-33.0, 66.0, 32.0]) cube([66.0, 8.0, 6.0]);
        }
        
        // Vát góc đáy sau Chân Sau (Y = 45.0..47.5, Z = 22.0..27.0) tránh 100% thân motor GA25:
        for (sx = [-1, 1]) {
            translate([sx * 33.0 - 7.5, 42.5, 21.0])
                rotate([38, 0, 0])
                    cube([15.0, 4.5, 8.0]);
        }
        
        // A. 2 HỐC BẮT TRỤ SAU (X = +-31.5..35.0, Y = 46.5..51.5):
        //    Đáy Z = 22.0..26.5mm (dày 4.5mm), phía trên Z = 26.5..38.0mm mở giếng chữ U rộng rãi kèm côn 45° tự đỡ:
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 31.5, 46.5, 20.0]) cylinder(d=3.6, h=20.0);
                translate([sx * 35.0, 46.5, 20.0]) cylinder(d=3.6, h=20.0);
                translate([sx * 31.5, 51.5, 20.0]) cylinder(d=3.6, h=20.0);
                translate([sx * 35.0, 51.5, 20.0]) cylinder(d=3.6, h=20.0);
            }
            hull() {
                translate([sx * 31.5, 46.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
                translate([sx * 35.0, 51.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
                translate([sx * 41.0, 47.0, 26.5]) cylinder(d1=3.6, d2=9.0, h=3.0);
                translate([sx * 41.0, 51.0, 26.5]) cylinder(d1=3.6, d2=9.0, h=3.0);
            }
            hull() {
                translate([sx * 31.5, 46.5, 29.4]) cylinder(d=9.2, h=10.0);
                translate([sx * 35.0, 51.5, 29.4]) cylinder(d=9.2, h=10.0);
                translate([sx * 41.0, 47.0, 29.4]) cylinder(d=9.0, h=10.0);
                translate([sx * 41.0, 51.0, 29.4]) cylinder(d=9.0, h=10.0);
            }
        }
        
        // B. 2 HỐC BẮT TRỤ TRƯỚC LỘ THIÊN (X = +-32.0..35.5, Y = 95.5..99.5):
        //    Đáy Z = 22.0..26.5mm (dày 4.5mm), phía trên Z = 26.5..38.0mm mở thông ra phía trước & mép ngoài:
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 32.0, 95.5, 20.0]) cylinder(d=3.6, h=20.0);
                translate([sx * 35.5, 95.5, 20.0]) cylinder(d=3.6, h=20.0);
                translate([sx * 32.0, 99.5, 20.0]) cylinder(d=3.6, h=20.0);
                translate([sx * 35.5, 99.5, 20.0]) cylinder(d=3.6, h=20.0);
            }
            hull() {
                translate([sx * 32.5, 95.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
                translate([sx * 35.5, 95.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
                translate([sx * 32.5, 103.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
                translate([sx * 38.5, 99.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
            }
            hull() {
                translate([sx * 32.5, 95.5, 29.4]) cylinder(d=8.5, h=10.0);
                translate([sx * 35.5, 95.5, 29.4]) cylinder(d=8.5, h=10.0);
                translate([sx * 32.5, 103.5, 29.4]) cylinder(d=8.5, h=10.0);
                translate([sx * 38.5, 99.5, 29.4]) cylinder(d=8.5, h=10.0);
            }
        }
        
        // C. 2 RÃNH KHÓA TÁN M3 ĐÁY KÍN Ở TAI SAU LỘ THIÊN (X = +-33.0, Y = -15.0 .. -11.0):
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 33.0, -15.0, 28.0]) cylinder(d=3.3, h=12.0);
                translate([sx * 33.0, -11.0, 28.0]) cylinder(d=3.3, h=12.0);
            }
            // Rãnh khóa tán M3 (Z = 31.2..34.2) có đáy đỡ Z = 30.0..31.2mm + cửa nhét tán từ đuôi Y = -19.0:
            hull() {
                translate([sx * 33.0, -19.0, 31.2]) cylinder(d=5.65, h=2.9);
                translate([sx * 33.0, -11.0, 31.2]) cylinder(d=5.65, h=2.9);
            }
            hull() {
                translate([sx * 33.0, -19.0, 34.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
                translate([sx * 33.0, -11.0, 34.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
            }
        }
        
        // D. 2 RÃNH KHÓA TÁN M3 ĐÁY KÍN Ở TAI TRƯỚC LỘ THIÊN (X = +-34.0, Y = 86.0 .. 90.0):
        //    Nằm giữa K2 Hub (Y <= 80.0) và Ốc Trụ Trước (Y = 99.0), có cửa nhét tán từ mép ngoài |X| = 40.0!
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 34.0, 86.0, 20.0]) cylinder(d=3.3, h=20.0);
                translate([sx * 34.0, 90.0, 20.0]) cylinder(d=3.3, h=20.0);
            }
            hull() {
                translate([sx * 34.0, 86.0, 31.2]) cylinder(d=5.65, h=2.9);
                translate([sx * 34.0, 90.0, 31.2]) cylinder(d=5.65, h=2.9);
                translate([sx * 40.5, 88.0, 31.2]) cylinder(d=5.65, h=2.9);
            }
            hull() {
                translate([sx * 34.0, 86.0, 34.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
                translate([sx * 34.0, 90.0, 34.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
                translate([sx * 40.5, 88.0, 34.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
            }
        }
    }
}

module k2_base_riser_frame_printable() {
    translate([0, 0, 38.0])
        rotate([180, 0, 0])
            k2_base_riser_frame();
}

// Bệ MCU nhỏ gọn Đa Năng V9.0 cho Plate 1 (Đã cắt hốc chữ U phía trước né 100% 2 Tháp Nâng Y=105!)
module mcu_deck_compact_slotted_v80() {
    T_deck = 4.0;
    difference() {
        union() {
            // Sàn chính dừng tại Y = 92.0mm (cách 2 Tháp Nâng 13.0mm):
            translate([-39.0, 42.0, 0.0]) cube([78.0, 50.0, T_deck]);
            // 2 Tai bắt trụ trước nằm tại |X| in [29.2, 39.0], Y in [90.0, 102.0] (né 100% Tháp Nâng!):
            for (sx = [-1, 1]) {
                translate([sx * 34.1 - 4.9, 90.0, 0.0]) cube([9.8, 12.0, T_deck]);
            }
        }
        translate([-20.0, 56.0, -1.0]) cube([40.0, 28.0, T_deck + 2.0]);
        for (sx = [-1, 1]) {
            for (py = [49.0, 97.5]) {
                hull() {
                    translate([sx * 31.8, py - 2.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                    translate([sx * 35.2, py - 2.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                    translate([sx * 31.8, py + 2.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                    translate([sx * 35.2, py + 2.5, -1.0]) cylinder(d=3.6, h=T_deck + 2.0);
                }
            }
            for (gx = [24.0, 32.0]) {
                for (gy = [60.0, 68.0, 76.0, 84.0]) {
                    hull() {
                        translate([sx * gx, gy - 2.0, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
                        translate([sx * gx, gy + 2.0, -1.0]) cylinder(d=3.4, h=T_deck + 2.0);
                    }
                }
            }
        }
    }
}

// Trụ đệm đôn cao 18mm rời (giữ tương thích)
module riser_standoff_18mm() {
    difference() {
        cylinder(d=11.0, h=18.0);
        translate([0, 0, -1.0]) cylinder(d=3.4, h=20.0);
        translate([0, 0, 4.0]) cylinder(d=7.2, h=15.0);
    }
}

// ====================================================================
// 3. BẢN ADAPTER LIỀN KHỐI LÙI HẬU NÉ THÁP GẮP TRỤ 100% V9.0 (MONOLITHIC CANTILEVER RISER V9.0 - 0% SUPPORT)
// - Thiết kế lại toàn diện để GIẢI QUYẾT TRIỆT ĐỂ 100% LỖI VƯỚNG CẤU TRÚC GẮP TRỤ & KHẢ THI LẮP ĐẶT:
//   1. SÀN CHÍNH LÙI HẬU (Y in [-8.0, +82.0mm], X in [-60.0, +60.0mm], Z in [38.0, 44.0mm]):
//      + Mép trước sàn chính dừng tại Y = 82.0mm -> Tạo khoảng trống khổng lồ 23.0mm trước 2 Tháp Nâng
//        (Y = 105.0mm) và 25.65mm trước tai bắt + dây cáp Servo S1 (Y = 107.65mm)!
//      + Bo mạch K2 Control Hub (Y in [-6.0, +80.0mm]) nằm lùi về sau làm đối trọng cân bằng cho cụm tay gắp,
//        mặt trước K2 Hub cách 2 Tháp Nâng đúng 25.0mm (2.5cm) và cách Servo S1 tới 27.65mm!
//   2. 2 TAY VƯƠN BẮT TRỤ TRƯỚC LỘ THIÊN NÉ THÁP TUYỆT ĐỐI (|X| in [29.2, 39.2mm], Y in [82.0, 102.0mm]):
//      + Mép trong |X| = 29.2mm nằm ngoài hoàn toàn 2 Tháp Nâng và Gờ định vị sau (|X| <= 28.0mm -> khe hở 1.2mm).
//      + Mũi trước Y = 102.0mm dừng trước mặt lưng 2 Tháp Nâng và Gờ định vị ngoài (Y = 105.0mm -> khe hở 3.0mm).
//      + Hốc chữ U giữa 2 tay rộng 58.4 x 23.0mm trống hoàn toàn!
//      + Lỗ bắt ốc trụ trước (X = +-33.0, Y = 99.0mm) nằm LỘ THIÊN 19.0mm phía trước K2 Control Hub,
//        có giếng mở thông suốt xuống bậc đế dày 4.5mm (Z = 22.0..26.5mm) -> Dùng ốc M3x10/12mm cực dễ!
//   3. LẮP THẲNG ĐỨNG TỪ TRÊN XUỐNG (100% VERTICAL DROP-IN - KHÔNG CẦN ĐẨY TRƯỢT):
//      + Hạ thẳng đứng xuống 4 trụ khung gầm (Z = 22.0mm) giữa động cơ sau (Y = 44.5mm) và tháp nâng (Y = 105.0mm).
//      + 2 Chân Sau (Y = 49.0mm) có GIẾNG VẶN ỐC THẲNG ĐỨNG XUYÊN SUỐT từ mặt trên xuống bậc đế dày 4.5mm!
//   4. HỆ RÃNH ĐƯỜNG RAY KHÓA TÁN M3 ĐÁY KÍN CHỐNG RƠI (CAPTIVE BLIND-FLOOR NUT CHANNELS):
//      + Đáy sàn có lớp đường ray kín dày 1.2mm (Z = 38.0..39.2mm) giữ 4 con tán M3 KHÔNG BAO GIỜ RƠI XUỐNG GẦM
//        kèm cửa nhét tán trực tiếp từ mép sườn ngoài (|X| = 60.0mm) và hốc nạp tán!
//      + Quy trình lắp chuẩn 100%: Hạ bệ lên xe -> Vặn 4 ốc trụ khung gầm lộ thiên từ mặt trên -> Đặt K2 Hub
//        lên trên và vặn 4 ốc góc vào 4 tán M3 đã nằm sẵn trong rãnh đáy kín (hoặc bắt K2 Hub ở ngoài trước tùy ý)!
// ====================================================================
module k2_adapter_monolithic_v60() {
    Z_top = 44.0;
    T_deck = 6.0;
    Z_bot = Z_top - T_deck; // 38.0mm (Cao hơn nẹp motor sau Z=36.0mm đúng 2.0mm & cao hơn motor 5.5mm!)
    
    difference() {
        union() {
            // 1. Mặt sàn chính phẳng tuyệt đối 100% lùi hậu (120.0 x 90.0 x 6.0 mm, X in [-60, 60], Y in [-8.0, 82.0]):
            translate([-60.0, -8.0, Z_bot])
                cube([120.0, 90.0, T_deck]);
                
            // 2. Hai Chân Đôn Sau Hạ Thẳng Đứng (|X| in [26.5, 39.2], Y in [45.0, 56.5], Z in [22.0, 38.0]):
            //    Cách nẹp motor sau (|X|=40.5 -> khe hở 1.3mm) và thân motor sau (Y<=44.5) an toàn tuyệt đối!
            for (sx = [-1, 1]) {
                translate([sx * 32.85 - 6.35, 45.0, 22.0])
                    cube([12.7, 11.5, Z_bot - 22.0]);
            }
            
            // 3. Hai Tay/Chân Đôn Trước LỘ THIÊN NGOÀI K2 HUB & NÉ THÁP NÂNG 100%
            //    (|X| in [29.2, 39.2], Y in [81.0, 102.0], Z in [22.0, 44.0]):
            //    - Mép trong |X| = 29.2mm (nằm ngoài vách 2 Tháp Nâng |X| <= 28.0mm đúng 1.2mm!)
            //    - Mũi trước Y = 102.0mm (dừng trước lưng 2 Tháp Nâng & Gờ định vị Y = 105.0mm đúng 3.0mm!)
            //    - Mặt đỉnh Z = 44.0mm đồng phẳng 100% với sàn chính -> Đặt in lật úp Z_print = 0.0mm phẳng 100% Zero Support!
            for (sx = [-1, 1]) {
                translate([sx * 34.2 - 5.0, 81.0, 22.0])
                    cube([10.0, 21.0, Z_top - 22.0]);
            }
        }
        
        // Vát góc đáy sau Chân Sau (Y = 45.0..47.5, Z = 22.0..27.0) tránh 100% thân motor GA25:
        for (sx = [-1, 1]) {
            translate([sx * 33.0 - 7.5, 42.5, 21.0])
                rotate([38, 0, 0])
                    cube([15.0, 4.5, 8.0]);
        }
        
        // Ô thoáng trung tâm luồn dây Pin 2S (42.0 x 36.0 mm - X in [-21, 21], Y in [19.0, 55.0]):
        translate([-21.0, 19.0, 20.0])
            cube([42.0, 36.0, 26.0]);
            
        // A. 2 CHÂN ĐÔN SAU HẠ THẲNG ĐỨNG KÈM GIẾNG VẶN ỐC XUYÊN SUỐT TỪ MẶT TRÊN (X = +-31.5..35.0, Y = 46.5..51.5):
        //    - Đáy Z = 22.0..26.5mm (dày 4.5mm): Rãnh trượt 2 chiều X-Y bắt vừa cả X=+-32, +-33 và Y=46.5..51.5mm!
        //    - Phía trên Z = 26.5..44.0mm: Giếng thông suốt Ø9.2mm từ mặt trên xuống kèm côn 45° tự đỡ ở Z = 26.5..29.5mm!
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 31.5, 46.5, 20.0]) cylinder(d=3.6, h=26.0);
                translate([sx * 35.0, 46.5, 20.0]) cylinder(d=3.6, h=26.0);
                translate([sx * 31.5, 51.5, 20.0]) cylinder(d=3.6, h=26.0);
                translate([sx * 35.0, 51.5, 20.0]) cylinder(d=3.6, h=26.0);
            }
            hull() {
                translate([sx * 31.5, 46.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
                translate([sx * 35.0, 46.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
                translate([sx * 31.5, 51.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
                translate([sx * 35.0, 51.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
            }
            hull() {
                translate([sx * 31.5, 46.5, 29.4]) cylinder(d=9.2, h=16.0);
                translate([sx * 35.0, 46.5, 29.4]) cylinder(d=9.2, h=16.0);
                translate([sx * 31.5, 51.5, 29.4]) cylinder(d=9.2, h=16.0);
                translate([sx * 35.0, 51.5, 29.4]) cylinder(d=9.2, h=16.0);
            }
        }
        
        // B. 2 TAY/CHÂN TRƯỚC LỘ THIÊN NGOÀI K2 HUB & NÉ THÁP NÂNG (X = +-32.0..35.5, Y = 95.5..99.5):
        //    - Nằm lộ thiên phía trước mặt sàn chính (Y=82.0) tới 17.0mm -> Không bao giờ bị K2 Hub che khuất!
        //    - Đáy Z = 22.0..26.5mm (dày 4.5mm): Rãnh trượt 2 chiều X-Y!
        //    - Phía trên Z = 26.5..44.0mm: Giếng chữ U mở rộng thông lên mặt trên (Z=44), mũi trước (Y=103) và mép ngoài
        //      kèm côn 45° ở Z = 26.5..29.5mm -> Vặn ốc M3x10/12mm cực dễ và in úp 0% Support!
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 32.0, 95.5, 20.0]) cylinder(d=3.6, h=26.0);
                translate([sx * 35.5, 95.5, 20.0]) cylinder(d=3.6, h=26.0);
                translate([sx * 32.0, 99.5, 20.0]) cylinder(d=3.6, h=26.0);
                translate([sx * 35.5, 99.5, 20.0]) cylinder(d=3.6, h=26.0);
            }
            hull() {
                translate([sx * 32.5, 95.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
                translate([sx * 35.5, 95.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
                translate([sx * 32.5, 103.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
                translate([sx * 38.5, 99.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
            }
            hull() {
                translate([sx * 32.5, 95.5, 29.4]) cylinder(d=8.5, h=16.0);
                translate([sx * 35.5, 95.5, 29.4]) cylinder(d=8.5, h=16.0);
                translate([sx * 32.5, 103.5, 29.4]) cylinder(d=8.5, h=16.0);
                translate([sx * 38.5, 99.5, 29.4]) cylinder(d=8.5, h=16.0);
            }
        }
        
        // C. TỔ HỢP RÃNH ĐƯỜNG RAY KHÓA TÁN M3 ĐÁY KÍN 2 CHIỀU (CAPTIVE 2D SLOTTED MATRIX) TẠI 4 GÓC K2 CONTROL HUB:
        //    - Chiều ngang X: 4 rãnh dọc tại |X| = 32.0, 40.0, 48.0, 54.0mm + các rãnh ngang liên thông từ |X|=30.0 đến 55.5mm
        //    - Chiều dọc Y: Góc sau từ Y = -4.5 đến 19.5mm; Góc trước từ Y = 54.5 đến 78.5mm (ΔY bao phủ 35..83mm!)
        //    - Sàn đáy kín Z = 38.0..39.2mm giữ tán M3 KHÔNG BAO GIỜ RƠI XUỐNG GẦM + Cửa nhét tán từ sườn ngoài |X|=60.0mm!
        for (sx = [-1, 1]) {
            for (abs_x = [32.0, 40.0, 48.0, 54.0]) {
                slot_m3_with_nut_channel_zbot(sx * abs_x, -4.5, sx * abs_x, 19.5, Z_bot, T_deck);
                slot_m3_with_nut_channel_zbot(sx * abs_x, 54.5, sx * abs_x, 78.5, Z_bot, T_deck);
            }
            for (hy_rear = [-2.0, 5.0, 12.0, 18.0]) {
                slot_m3_with_nut_channel_zbot(sx * 30.0, hy_rear, sx * 55.5, hy_rear, Z_bot, T_deck);
                side_nut_entry_port_zbot(sx, hy_rear, Z_bot, T_deck);
            }
            for (hy_front = [56.0, 62.0, 69.0, 76.0]) {
                slot_m3_with_nut_channel_zbot(sx * 30.0, hy_front, sx * 55.5, hy_front, Z_bot, T_deck);
                side_nut_entry_port_zbot(sx, hy_front, Z_bot, T_deck);
            }
            // D. Hệ lưới lỗ chuẩn 8mm dọc 2 bên sườn (Y = 25, 33, 41):
            for (gx = [44.0, 52.0]) {
                for (gy = [25.0, 33.0, 41.0]) {
                    slot_m3_with_nut_channel_zbot(sx * gx, gy - 1.5, sx * gx, gy + 1.5, Z_bot, T_deck);
                }
            }
        }
        for (gx = [-16.0, -8.0, 0.0, 8.0, 16.0]) {
            for (gy = [0.0, 8.0, 64.0, 72.0]) {
                slot_m3_with_nut_channel_zbot(gx - 1.5, gy, gx + 1.5, gy, Z_bot, T_deck);
            }
        }
    }
}

// BẢN IN ÚP PHẲNG 100% TRÊN BÀN IN (Z = 0.0 mm - ZERO SUPPORT):
module k2_adapter_monolithic_printable() {
    translate([0, 0, 44.0])
        rotate([180, 0, 0])
            k2_adapter_monolithic_v60();
}

// ====================================================================
// 4. NẸP ÔM ĐỘNG CƠ GA25 PHÍA SAU - TRÁI (LEFT REAR MOTOR CLAMP V4.3)
// ====================================================================
module ga25_rear_clamp_left() {
    difference() {
        union() {
            translate([-12.0, -22.0, 0.6]) cube([15.5, 12.0, 5.4]);
            translate([-12.0, -14.5, 0.0]) cube([15.5, 29.0, 16.0]);
            translate([-12.0, 10.0, 0.6]) cube([15.5, 12.0, 5.4]);
        }
        translate([-13.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=26.2, h=20.0);
        translate([-13.0, 0, 0]) rotate([0, 90, 0]) cylinder(d1=27.5, d2=26.2, h=1.5);
        translate([2.5, 0, 0]) rotate([0, 90, 0]) cylinder(d1=26.2, d2=27.5, h=1.5);
        for (y_pos = [-17.5, 17.5]) {
            translate([0, y_pos, -1.0]) cylinder(d=3.4, h=9.0);
            translate([0, y_pos, 3.5]) cylinder(d=6.5, h=3.0);
        }
        translate([3.5, 22.0, -1.0]) rotate([0, 0, 45]) cube([6.0, 6.0, 18.0]);
        translate([3.5, -22.0, -1.0]) rotate([0, 0, 45]) cube([6.0, 6.0, 18.0]);
    }
}

// ====================================================================
// 5. NẸP ÔM ĐỘNG CƠ GA25 PHÍA SAU - PHẢI (RIGHT REAR MOTOR CLAMP V4.3)
// ====================================================================
module ga25_rear_clamp_right() {
    difference() {
        union() {
            translate([-3.5, -22.0, 0.6]) cube([15.5, 12.0, 5.4]);
            translate([-3.5, -14.5, 0.0]) cube([15.5, 29.0, 16.0]);
            translate([-3.5, 10.0, 0.6]) cube([15.5, 12.0, 5.4]);
        }
        translate([-5.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=26.2, h=20.0);
        translate([-4.5, 0, 0]) rotate([0, 90, 0]) cylinder(d1=27.5, d2=26.2, h=1.5);
        translate([11.0, 0, 0]) rotate([0, 90, 0]) cylinder(d1=26.2, d2=27.5, h=1.5);
        for (y_pos = [-17.5, 17.5]) {
            translate([0, y_pos, -1.0]) cylinder(d=3.4, h=9.0);
            translate([0, y_pos, 3.5]) cylinder(d=6.5, h=3.0);
        }
        translate([-3.5, 22.0, -1.0]) rotate([0, 0, 45]) cube([6.0, 6.0, 18.0]);
        translate([-3.5, -22.0, -1.0]) rotate([0, 0, 45]) cube([6.0, 6.0, 18.0]);
    }
}

// ====================================================================
// 6. NẸP ÔM ĐỘNG CƠ GA25 PHÍA SAU - DÙNG CHUNG (UNIVERSAL REAR MOTOR CLAMP V4.3)
// ====================================================================
module ga25_rear_clamp_universal() {
    difference() {
        union() {
            translate([-4.0, -22.0, 0.6]) cube([8.0, 12.0, 5.4]);
            translate([-4.0, -14.5, 0.0]) cube([8.0, 29.0, 16.0]);
            translate([-4.0, 10.0, 0.6]) cube([8.0, 12.0, 5.4]);
        }
        translate([-5.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=26.2, h=10.0);
        translate([-5.0, 0, 0]) rotate([0, 90, 0]) cylinder(d1=27.5, d2=26.2, h=1.5);
        translate([2.5, 0, 0]) rotate([0, 90, 0]) cylinder(d1=26.2, d2=27.5, h=1.5);
        for (y_pos = [-17.5, 17.5]) {
            translate([0, y_pos, -1.0]) cylinder(d=3.4, h=9.0);
            translate([0, y_pos, 3.5]) cylinder(d=6.5, h=3.0);
        }
    }
}

// ====================================================================
// 7. THÁP NÂNG PHẢI MG996R V5.0 (RIGHT LIFT TOWER V5.0)
// ====================================================================
// - Hốc chìm tán M3 lục giác sâu 2.6mm ở mặt trong (X = 20.0mm): Tán M3 chìm phẳng tuyệt đối.
// - Rãnh lượn mở rộng 1.0mm ở mặt trong (X in [20.0, 21.0]): Tăng khe hở tay nâng lên 1.5mm!
module lift_tower_right_v50() {
    x_wall_min = 20.0;
    x_flange_min = 12.0;
    brace_x0 = 0.0;
    fx = 16.0;
    wx = 24.0;

    difference() {
        union() {
            translate([x_wall_min, 105.0, 4.0]) cube([8.0, 61.0, 90.0]);
            translate([x_flange_min, 105.0, 4.0]) cube([8.0, 22.5, 8.0]);
            translate([x_flange_min, 154.5, 4.0]) cube([8.0, 11.5, 8.0]);
            translate([brace_x0, 105.0, 88.0]) cube([20.0, 13.0, 6.0]);
        }

        translate([-30.0, 127.5, 3.5]) cube([60.0, 27.0, 30.5]);

        // Hốc chữ nhật lọt thân Servo MG996R (41.2 x 20.2 mm)
        translate([19.0, 114.05, 47.9]) cube([10.0, 41.2, 20.2]);

        // 4 Lỗ ốc M3 bắt Servo MG996R có HỐC CHÌM TÁN M3 LỤC GIÁC Ở MẶT TRONG:
        for (sy = [134.65 - 24.25, 134.65 + 24.25]) {
            for (sz = [58.0 - 5.0, 58.0 + 5.0]) {
                translate([19.0, sy, sz]) rotate([0, 90, 0]) cylinder(d=3.4, h=10.0);
                translate([19.9, sy, sz]) rotate([0, 90, 0]) cylinder(d=6.5, h=2.8, $fn=6);
            }
        }

        // Khe lượn mở rộng (Clearance Pocket) sâu 1.0mm ở mặt trong dọc hành trình quay:
        translate([19.9, 138.0, 44.0]) cube([1.2, 28.0, 30.0]);

        // Lỗ chốt xoay trên
        translate([-30.0, 145.0, 86.0]) rotate([0, 90, 0]) cylinder(d=3.3, h=60.0);

        // Lỗ bu-lông M3 bắt xuống sàn khung gầm
        for (sy = [110.5, 122.0, 160.25]) {
            translate([fx, sy, 3.5]) cylinder(d=3.3, h=10.0);
        }
        for (sy = [116.0, 160.25]) {
            translate([wx, sy, 3.5]) cylinder(d=3.0, h=14.0);
        }
    }
}

module lift_tower_right_v50_printable() {
    translate([0, 0, 28.0]) rotate([0, 90, 0]) lift_tower_right_v50();
}

// ====================================================================
// 8. KHUNG TAY NÂNG DƯỚI CHỮ H V5.0 (LOWER H-FRAME ARM V5.0)
// ====================================================================
// - Hốc tròn âm Ø20.8mm sâu 2.5mm ôm trọn Đĩa tròn Servo MG996R (25T Round Horn)!
// - 8 Lỗ ốc M3 trên PCD Ø14.0mm (r = 7.0mm) kèm lỗ bậc chìm Ø6.0mm ở mặt trong.
// - Lỗ tâm Ø6.5mm tra vít khóa trục 25T.
// - Đáy phẳng 100% tại Z = -6.0mm: Đặt in phẳng Z = 0 -> 0% SUPPORT!
module lower_h_frame_arm_v50(length = 98.0, height = 12.0, thickness = 5.0) {
    difference() {
        union() {
            // Thanh trái (X in [-19.5, -14.5])
            translate([-19.5, 0, -height/2]) cube([thickness, length, height]);
            translate([-19.5, 0, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);
            translate([-19.5, length, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);
            translate([-19.5, -height/2, -height/2]) cube([thickness, height/2, height/2]);
            translate([-19.5, length, -height/2]) cube([thickness, height/2, height/2]);

            // Thanh phải (X in [14.5, 19.5])
            translate([14.5, 0, -height/2]) cube([thickness, length, height]);
            translate([14.5, length, 0]) rotate([0, 90, 0]) cylinder(d=height, h=thickness);
            translate([14.5, length, -height/2]) cube([thickness, height/2, height/2]);

            // Gờ vòm tròn tăng cứng ôm đĩa tròn Servo (d = 23.0mm) ở gốc thanh phải:
            intersection() {
                translate([14.5, 0, 0]) rotate([0, 90, 0]) cylinder(d=23.0, h=thickness);
                translate([14.0, -12.0, -height/2]) cube([thickness + 1.0, 24.0, 20.0]);
            }
            translate([14.5, -height/2, -height/2]) cube([thickness, height/2, height/2]);

            // Thanh giằng ngang chữ H chống xoắn (X in [-14.5, 14.5])
            translate([-14.5, 42.0, -height/2]) cube([29.0, 14.0, height]);
        }

        // Hốc tròn âm Ø20.8mm sâu 2.5mm ở mặt ngoài thanh phải (X in [17.0, 19.6])
        translate([17.0, 0, 0]) rotate([0, 90, 0]) cylinder(d=20.8, h=3.0);

        // Lỗ tâm Ø6.5mm tra vít khóa trục Servo 25T
        translate([13.5, 0, 0]) rotate([0, 90, 0]) cylinder(d=6.5, h=7.0);

        // 8 Lỗ ốc M3 trên PCD Ø14.0mm kèm lỗ bậc chìm Ø6.0mm ở mặt trong
        for (a = [0:45:315]) {
            hy = 7.0 * cos(a);
            hz = 7.0 * sin(a);
            if (hz >= -height/2 + 1.0) {
                translate([13.5, hy, hz]) rotate([0, 90, 0]) cylinder(d=3.2, h=7.0);
                translate([13.5, hy, hz]) rotate([0, 90, 0]) cylinder(d=6.0, h=2.2);
            }
        }

        // Lỗ chốt xoay mắt trước
        translate([-22.0, length, 0]) teardrop_hole_x(d=3.3, h=44.0);

        // Lỗ chốt xoay mắt sau thanh trái
        translate([-22.0, 0, 0]) teardrop_hole_x(d=3.3, h=10.0);
    }
}

module lower_h_frame_arm_v50_printable() {
    translate([0, 0, 6.0]) lower_h_frame_arm_v50();
}

// ====================================================================
// 9. KHỐI KHÓA ĐĨA TRÒN SERVO S1 RỜI (S1 ROUND HORN DRIVE COUPLER)
// ====================================================================
module s1_round_horn_drive_coupler() {
    difference() {
        union() {
            cylinder(d=23.0, h=4.0);
            translate([-4.0, 0, 4.0]) cube([8.0, 20.0, 2.5]);
        }
        translate([0, 0, -0.1]) cylinder(d=20.8, h=2.1);
        translate([0, 0, -1.0]) cylinder(d=6.5, h=8.0);
        for (a = [0, 90, 180, 270]) {
            translate([7.0*cos(a), 7.0*sin(a), -1.0]) cylinder(d=3.2, h=8.0);
        }
        translate([0, 10.0, -1.0]) cylinder(d=2.5, h=8.0);
        translate([0, 16.0, -1.0]) cylinder(d=2.5, h=8.0);
    }
}

// ====================================================================
// 9B. CỔ TAY NỐI TAY NÂNG H-FRAME & GÁ SERVO S3 GẬP DỌC 90° V7.1
// (04A_Wrist_Clevis_Pitch_Bracket_S3 - ZERO SUPPORT, 100% H-FRAME COMPATIBLE)
// - Phía sau (Y = 8.0, Z = 10.0 & 38.0): Lắp vừa 100% 4 chốt của cánh tay chữ H đã in (03 & 03B)
// - Phía trước (Y in [16.6, 37.0]): Ôm khít Servo S3 (MG996R) đặt dọc, trục quay hướng +X
//   tại (Y_piv = 26.8, Z_piv = 38.0), mặt đĩa tròn S3 nằm đúng tại X = +27.0mm!
// - Bên trái (X in [-27.0, -13.5]): Gối đỡ đồng trục M3 (X = -27.0mm) vát 45° tự đỡ kèm hốc lục giác giữ tán M3!
// - Đặt in phẳng mặt lưng Y = 0 xuống bàn in (rotate([90, 0, 0])) -> 0% SUPPORT TUYỆT ĐỐI!
// ====================================================================
module wrist_clevis_pitch_bracket_s3() {
    Y_piv = 26.8;
    Z_piv = 38.0;

    difference() {
        union() {
            // 1. Khối Clevis & Lưng chịu lực từ Y = 0 đến Y = 16.6 (X in [-14.0, +14.0], Z in [-2.5, 56.0]):
            translate([-14.0, 0, -2.5]) cube([28.0, 16.6, 46.5]);
            translate([-14.0, 0, 44.0]) cube([27.0, 16.6, 12.0]);

            // 2. Vách Trái đỡ lưng Servo S3 (X in [-16.5, -13.5], Y in [16.6, 37.0], Z in [-2.5, 56.0])
            // vát 45° từ X = -14.0 tại Y = 14.0 ra X = -16.5 tại Y = 16.6:
            hull() {
                translate([-14.0, 14.0, -2.5]) cube([1.0, 2.6, 58.5]);
                translate([-16.5, 16.6, -2.5]) cube([3.0, 20.4, 58.5]);
            }

            // 3. Gối Trục Xoay Đồng Trục Bên Trái vươn ra X = -27.0mm tại (Y_piv = 26.8, Z_piv = 38.0)
            // vát côn 45° tự đỡ từ (X = -14.0, Y = 13.8) lên (X = -27.0, Y = 26.8) -> 0% Support khi in mặt Y = 0!
            hull() {
                translate([-14.0, 13.8, Z_piv - 9.0]) cube([1.0, 2.8, 18.0]);
                translate([-16.5, 16.6, Z_piv - 9.0]) cube([3.0, 18.0, 18.0]);
                translate([-27.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=16.0, h=1.0);
            }

            // 4. Khối Bắt Tai Dưới Servo S3 (X in [-14.0, +13.0], Y in [16.6, 37.0], Z in [-2.5, 7.2]):
            translate([-14.0, 16.6, -2.5]) cube([27.0, 20.4, 9.7]);

            // 5. Khối Bắt Tai Trên Servo S3 (X in [-14.0, +13.0], Y in [16.6, 37.0], Z in [48.6, 56.0]):
            translate([-14.0, 16.6, 48.6]) cube([27.0, 20.4, 7.4]);
        }

        // A. Hốc giữa Clevis phía sau (X in [-8.5, +8.5], Y in [4.5, 16.6], Z in [-3.0, 57.0])
        // để giảm trọng lượng và nhét 4 tán M3 giữ chốt tay nâng cực dễ:
        translate([-8.5, 4.5, -3.0]) cube([17.0, 12.2, 60.0]);

        // B. 4 Lỗ chốt xoay nối với tay nâng chữ H dưới (Z = 10.0) và trên (Z = 38.0) tại Y = 8.0:
        for (zp = [10.0, 38.0]) {
            translate([-20.0, 8.0, zp]) rotate([0, 90, 0]) cylinder(d=3.3, h=40.0);
            translate([-20.0, 8.0, zp]) rotate([0, 90, 0]) rotate([0, 0, -45]) cube([3.3/2, 3.3/2, 40.0]);
            translate([-8.6, 8.0, zp]) rotate([0, -90, 0]) cylinder(d=6.5, h=2.6, $fn=6);
            translate([8.6, 8.0, zp])  rotate([0, 90, 0])  cylinder(d=6.5, h=2.6, $fn=6);
        }

        // C. 4 Lỗ bắt ốc M3 tự taro (Ø2.95mm sâu 8.5mm) + Hốc mở phía trước nhét tán M3 cho tai Servo S3
        // (Y = 26.8 +- 5.0 => 21.8 & 31.8; Z = 3.75 & 52.25):
        for (sy = [Y_piv - 5.0, Y_piv + 5.0]) {
            for (sz = [3.75, 52.25]) {
                translate([-10.0, sy, sz]) rotate([0, 90, 0]) cylinder(d=2.95, h=25.0);
            }
        }
        // Khoang mở phía trước ở X in [-8.5, +4.5] để có thể luồn tán M3 từ phía trước nếu muốn dùng kèm đai ốc:
        translate([-8.5, 19.0, 0.75])  cube([13.0, 19.0, 6.0]);
        translate([-8.5, 19.0, 49.25]) cube([13.0, 19.0, 6.0]);

        // D. Lỗ Trục Xoay Đồng Trục Bên Trái tại (Y_piv = 26.8, Z_piv = 38.0)
        // kèm lỗ tự taro M3 dài 10.5mm + Hốc Lục Giác giữ tán M3 ở mặt trong Vách Trái (X in [-17.0, -13.5]):
        translate([-30.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=3.0, h=18.0);
        translate([-17.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=6.5, h=3.6, $fn=6);

        // E. Rãnh luồn dây cáp Servo S3 ở góc dưới:
        translate([-13.6, 22.0, 4.5]) cube([8.0, 9.6, 4.0]);
    }
}

module wrist_clevis_pitch_bracket_s3_printable() {
    rotate([90, 0, 0]) wrist_clevis_pitch_bracket_s3();
}

// ====================================================================
// 10. BỆ ĐẦU KẸP 3 TRỤ HOA TÍCH HỢP BẢN LỀ GẬP DỌC 90° V7.1
// (04_Gripper_Base_Head - ZERO SUPPORT, PITCH 0..90 DEG)
// - Tâm trục gập ngang (Pitch Axis) tại (Y_piv = 6.0, Z_piv = 38.0)
// - Má Phải (X in [+27.0, +35.0]): Tích hợp Hốc Đĩa Tròn MG996R Ø20.8mm + 8 lỗ M3 PCD Ø14mm
//   + rãnh tay đơn 8.2mm + lỗ tâm Ø6.5mm bắt trực tiếp vào trục Servo S3!
// - Má Trái (X in [-33.0, -27.0]): Lỗ trục xoay đồng trục Ø3.4mm + bậc chìm đầu ốc M3!
// - Mở rộng tâm 2 trục xoay hàm kẹp tại X = +-15.0mm, Y = 39.0mm (Xoay 0°..90° KHÔNG VA CHẠM!)
// - Đặt in phẳng đáy Z = 0.0mm -> 0% SUPPORT!
// ====================================================================
module gripper_base_head_3flower() {
    Y_piv = 6.0;
    Z_piv = 38.0;
    Y_jaw = 39.0;

    difference() {
        union() {
            // 1. Tấm đế chính (Y in [22.0, 50.0], Z in [0, 5.0]) + Bàn đỡ trượt chống xệ hàm phía trước (Y up to 60.0):
            translate([-31.0, 22.0, 0]) cube([66.0, 28.0, 5.0]);
            hull() {
                translate([-20.0, 46.0, 0]) cube([40.0, 4.0, 5.0]);
                translate([-14.0, 58.0, 0]) cube([28.0, 4.0, 5.0]);
            }

            // 2. Vách hậu liên kết cứng (Y in [22.0, 27.5], Z in [0, 24.5]):
            translate([-31.0, 22.0, 0]) cube([66.0, 5.5, 24.5]);

            // 3. Hai trục trụ xoay Ø8.0mm cho Hàm Trái (-15.0, Y_jaw=39.0) và Hàm Phải (+15.0, Y_jaw=39.0):
            translate([-15.0, Y_jaw, 5.0]) cylinder(d=8.0, h=10.0);
            translate([15.0, Y_jaw, 5.0])  cylinder(d=8.0, h=10.0);

            // 4. Trụ đỡ Cầu Servo S2 bên TRÁI & Má Bản Lề Gập Dọc Trái (X in [-31.0, -27.0] & [-33.0, -27.0]):
            translate([-31.0, 22.0, 0]) cube([4.0, 28.0, 35.0]);
            translate([-31.0, 22.0, 0]) cube([15.0, 5.0, 24.5]);
            hull() {
                translate([-31.0, 27.0, 21.5]) cube([4.0, 23.0, 13.5]);
                translate([-31.0, 27.0, 31.0]) cube([15.0, 23.0, 4.0]);
            }
            // - Má Bản Lề Gập Dọc Trái (X in [-33.0, -27.0]) vươn về (Y_piv = 6.0, Z_piv = 38.0)
            //   với đáy giọt nước ngược vát phẳng 45° tự đỡ nối thẳng xuống đế Z = 0 tại Y = 22.0:
            hull() {
                translate([-33.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=18.0, h=6.0);
                translate([-33.0, Y_piv + 6.0, Z_piv - 12.0]) cube([6.0, 2.0, 12.0]);
                translate([-31.0, 22.0, 0.0]) cube([4.0, 14.0, 35.0]);
            }

            // 5. Trụ đỡ Cầu Servo S2 bên PHẢI & Má Bản Lề Gập Dọc Phải (X in [+27.0, +35.0]):
            translate([27.0, 22.0, 0]) cube([8.0, 28.0, 35.0]);
            hull() {
                translate([27.0, 27.0, 26.0]) cube([8.0, 23.0, 9.0]);
                translate([25.25, 27.0, 29.0]) cube([9.75, 23.0, 6.0]);
            }
            // - Má Bản Lề Gập Dọc Phải (X in [+27.0, +35.0]) ôm Đĩa Tròn MG996R Ø20mm tại (Y_piv = 6.0, Z_piv = 38.0)
            //   với đáy giọt nước ngược vát phẳng 45° tự đỡ nối thẳng xuống đế Z = 0 tại Y = 22.0:
            hull() {
                translate([27.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=25.0, h=8.0);
                translate([27.0, Y_piv + 8.0, Z_piv - 16.0]) cube([8.0, 2.0, 16.0]);
                translate([27.0, 22.0, 0.0]) cube([8.0, 14.0, 35.0]);
            }
        }

        // A. 4 Lỗ bắt tai Servo MG996R S2 (Tâm trục tại X = +15.0, Y = Y_jaw = 39.0 => Tâm thân tại X = 4.65, Y = 39.0):
        for (sx = [4.65 - 24.25, 4.65 + 24.25]) {
            for (sy = [Y_jaw - 5.0, Y_jaw + 5.0]) {
                translate([sx, sy, 20.0]) cylinder(d=2.95, h=20.0);
            }
        }
        // Hốc lục giác âm cho 2 ốc tai phải S2 (X = +28.90):
        for (sy = [Y_jaw - 5.0, Y_jaw + 5.0]) {
            translate([28.90, sy, -1.0]) cylinder(d=6.5, h=29.5, $fn=6);
            translate([28.90, sy, 28.4]) cylinder(d1=6.5, d2=2.95, h=2.0);
        }

        // B. 2 Lỗ tâm trục xoay hàm kẹp (X = +-15.0, Y = Y_jaw = 39.0) + Hốc Lục Giác giữ tán M3 ở đáy:
        for (px = [-15.0, 15.0]) {
            translate([px, Y_jaw, -1.0]) cylinder(d=3.3, h=20.0);
            translate([px, Y_jaw, -0.1]) rotate([0, 0, 30]) cylinder(d=6.45, h=2.8, $fn=6);
            translate([px, Y_jaw, 2.65]) cylinder(d1=6.45, d2=3.3, h=1.8);
        }

        // C. Lỗ Trục Gập Ngang Bên Trái (X in [-33.0, -27.0]) tại (Y_piv = 6.0, Z_piv = 38.0):
        translate([-35.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=3.4, h=10.0);
        translate([-35.0, Y_piv, Z_piv]) rotate([0, 90, 0]) rotate([0, 0, 45]) cube([3.4/2, 3.4/2, 10.0]);
        translate([-33.5, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=6.5, h=2.5);

        // D. HỐC ĐĨA TRÒN SERVO S3 (Ø20.8mm sâu 2.5mm + 8 lỗ M3 PCD Ø14.0mm + Rãnh tay đơn 8.2mm + Lỗ tâm Ø6.5mm)
        // trên Má Bản Lề Phải (X in [+27.0, +35.0]) tại (Y_piv = 6.0, Z_piv = 38.0):
        translate([26.8, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=20.8, h=2.7);
        translate([26.8, Y_piv - 4.1, Z_piv - 4.1]) cube([2.7, 22.0, 8.2]);
        translate([26.0, Y_piv, Z_piv]) rotate([0, 90, 0]) cylinder(d=6.5, h=10.0);
        for (a = [0:45:315]) {
            hy = Y_piv + 7.0 * cos(a);
            hz = Z_piv + 7.0 * sin(a);
            translate([26.0, hy, hz]) rotate([0, 90, 0]) cylinder(d=2.9, h=10.0);
        }
    }
}

// ====================================================================
// 11 & 12. CẶP HÀM KẸP LIÊN HOÀN 3 TRỤ HOA Ø32MM V7.0 (05 & 06)
// - Kẹp cùng lúc 3 trụ hoa Ø32.0mm xếp dọc nối tiếp tại Y1=33, Y2=66, Y3=99mm
// - Tích hợp 3 Khe Đàn Hồi Lò Xo Lá độc lập + Gân ma sát ngang + Gờ đỡ đáy vát 45°
// - Hàm Phải (06) tích hợp HỐC TRÒN ÂM Ø20.8MM cho Đĩa Tròn Servo MG996R (8 lỗ M3 PCD Ø14mm)
//   KÈM rãnh chữ nhật 8.2mm đa năng!
// ====================================================================
module specialized_gripper_jaw_3flower(is_left = true) {
    pivot_x = is_left ? -15.0 : 15.0;
    sx = is_left ? -1.0 : 1.0;
    H = 22.0;
    H_hub = is_left ? 16.0 : 22.0;
    
    Y1 = 33.0;
    Y2 = 66.0;
    Y3 = 99.0;

    difference() {
        union() {
            // 1. Khối Hub trục xoay (X = +-15.0, Y = 0) & Cổ nối vào thân hàm:
            translate([pivot_x, 0, 0]) cylinder(r=11.5, h=H_hub);
            hull() {
                translate([pivot_x, 0, 0]) cylinder(r=10.0, h=H_hub);
                translate([sx * 17.5, 16.0, 0]) cylinder(r=5.0, h=H_hub);
            }
            hull() {
                translate([sx * 17.5, 14.0, 0]) cylinder(r=5.0, h=H_hub);
                translate([sx * 19.0, 21.0, 0]) cylinder(r=5.0, h=H);
            }
            
            // 2. Bánh răng rẻ quạt đồng bộ (R_pitch = 15.0mm, Module m = 1.5mm, cao 16.0mm):
            for (a = is_left ? [-54, -36, -18, 0, 18, 36] : [135, 153, 171, 189, 207, 225]) {
                translate([pivot_x, 0, 0])
                    rotate([0, 0, a])
                        hull() {
                            translate([10.5, -2.1, 0]) cube([2.5, 4.2, 16.0]);
                            translate([16.3, -1.1, 0]) cube([0.6, 2.2, 16.0]);
                        }
            }
            
            // 3. Thân Dầm Khung Chịu Lực Dọc 3 Hốc Hoa (Y1=33, Y2=66, Y3=99):
            difference() {
                union() {
                    for (yk = [Y1, Y2, Y3]) {
                        translate([0, yk, 0]) cylinder(r=23.0, h=H);
                    }
                    if (is_left) {
                        translate([-23.0, 20.0, 0]) cube([7.5, 79.0, H]);
                    } else {
                        translate([15.5, 20.0, 0])  cube([7.5, 79.0, H]);
                    }
                }
                // Cắt phẳng hoàn toàn phía trước Y3 (Y > 99.0) để nối mượt vào Phễu V-Guide:
                translate([-25.0, Y3, -1.0]) cube([50.0, 30.0, H + 2.0]);
                // Cắt vát góc trong phía sau Hốc #1 (|X| < 11.0, Y < 17.5) giải phóng không gian bánh răng:
                translate([-11.0, 8.0, -1.0]) cube([22.0, 9.5, H + 2.0]);
                // Trên Hàm Trái (is_left), hạ bậc vùng Y < 15.0 xuống Z = 16.0mm (kèm vát 45° tới Y = 21.0) để không bao giờ chạm cầu Servo S2:
                if (is_left) {
                    translate([-30.0, 0.0, H_hub]) cube([60.0, 15.0, H]);
                    translate([-30.0, 15.0, H_hub]) rotate([45, 0, 0]) cube([60.0, 10.0, 10.0]);
                }
            }
            
            // 4. Phễu dẫn hướng chữ V mở rộng 35° ở mũi hàm (từ Y = Y3 = 99.0 ra Y = 119.0):
            hull() {
                translate([sx * 19.2, Y3, 0]) cylinder(d=6.8, h=H);
                translate([sx * 30.0, Y3 + 19.0, 0]) cylinder(d=5.0, h=H);
            }
        }
        
        // Cắt bỏ nửa đối diện (chỉ giữ nửa bên trái hoặc bên phải từ Y = 8.0 trở đi):
        if (is_left) {
            translate([-7.5, 8.0, -1.0]) cube([40.0, 125.0, H + 2.0]);
        } else {
            translate([-32.5, 8.0, -1.0]) cube([40.0, 125.0, H + 2.0]);
        }
        
        // A. Khoét 3 Lòng Hốc Kẹp Hoa Ø32.0mm (R = 16.1mm) tại Y1=33, Y2=66, Y3=99:
        for (yk = [Y1, Y2, Y3]) {
            translate([0, yk, 0]) {
                translate([0, 0, -0.5]) cylinder(r=14.9, h=2.0);
                translate([0, 0, 1.4])  cylinder(r1=14.9, r2=16.1, h=1.2);
                translate([0, 0, 2.5])  cylinder(r=16.1, h=H + 2.0);
                for (zg = [6.5, 11.5, 16.5]) {
                    translate([0, 0, zg]) cylinder(r1=16.1, r2=16.6, h=0.8);
                    translate([0, 0, zg + 0.8]) cylinder(r1=16.6, r2=16.1, h=0.8);
                }
            }
        }
        
        // B. Khoét thông lối dẫn dọc giữa 3 hốc (Mấu định tâm ở X = +-13.0mm):
        translate([-13.0, Y1, 2.5]) cube([26.0, Y3 - Y1 + 5.0, H + 2.0]);
        translate([-12.5, Y1, -0.5]) cube([25.0, Y3 - Y1 + 5.0, 3.2]);
        
        // C. 3 Khe Đàn Hồi Lò Xo Lá Độc Lập (Elastic Compliance Slots) nằm gọn trong thân hàm:
        for (yk = [Y1, Y2, Y3]) {
            for (ang = is_left ? [166, 175, 184] : [-14, -5, 4]) {
                hull() {
                    translate([19.2 * cos(ang), yk + 19.2 * sin(ang), -1.0])
                        cylinder(d=2.0, h=H + 2.0, $fn=16);
                    translate([19.2 * cos(ang + 9), yk + 19.2 * sin(ang + 9), -1.0])
                        cylinder(d=2.0, h=H + 2.0, $fn=16);
                }
            }
        }
        
        // D. Lỗ bạc lót trục xoay Ø8.2mm sâu 10.2mm kèm mái côn tự đỡ 45° + Lỗ ốc tâm M3:
        translate([pivot_x, 0, -0.2]) cylinder(d=8.2, h=10.4);
        translate([pivot_x, 0, 10.2]) cylinder(d1=8.2, d2=3.4, h=2.4);
        translate([pivot_x, 0, -0.5]) cylinder(d=3.4, h=H + 2.0);
        if (is_left) {
            translate([pivot_x, 0, H_hub - 3.0]) cylinder(d=6.8, h=4.0);
        }
        
        // E. HỐC LẮP ĐĨA TRÒN SERVO MG996R (Ø20.8mm + 8 Lỗ M3 PCD Ø14mm) & RÃNH TAY GẠT ĐƠN TRÊN HÀM PHẢI (06):
        if (!is_left) {
            translate([pivot_x, 0, H - 2.5]) cylinder(d=20.8, h=3.0);
            translate([pivot_x - 4.1, -4.1, H - 2.5]) cube([8.2, 23.0, 3.0]);
            translate([pivot_x, 0, 12.6]) cylinder(d=6.5, h=10.0);
            for (a = [0:45:315]) {
                hx = pivot_x + 7.0 * cos(a);
                hy = 7.0 * sin(a);
                translate([hx, hy, 11.0]) cylinder(d=2.9, h=12.0);
            }
            translate([pivot_x, 11.0, 12.0]) cylinder(d=2.5, h=11.0);
            translate([pivot_x, 16.0, 12.0]) cylinder(d=2.5, h=11.0);
        }
    }
}
"""

PARTS = [
    {
        "stl_name": "04A_Wrist_Clevis_Pitch_Bracket_S3.stl",
        "scad_code": SCAD_LIBRARY + "\nwrist_clevis_pitch_bracket_s3_printable();\n",
        "desc": "Cổ tay nối tay nâng chữ H cũ & Gá Servo S3 gập dọc 90° V7.1 (Lắp vừa 4 chốt 03 & 03B, gối xoay đồng trục M3, in phẳng Z=0, 0% Support)"
    },
    {
        "stl_name": "04_Gripper_Base_Head.stl",
        "scad_code": SCAD_LIBRARY + "\ngripper_base_head_3flower();\n",
        "desc": "Bệ đầu kẹp 3 trụ hoa gập dọc 90° V7.1 (2 má bản lề gập dọc 90°, hốc đĩa tròn MG996R Ø20.8mm cho Servo S3, bàn đỡ chống xệ hàm, 0% Support)"
    },
    {
        "stl_name": "05_Gripper_Jaw_Left_VGuide_Flower32.stl",
        "scad_code": SCAD_LIBRARY + "\nspecialized_gripper_jaw_3flower(is_left=true);\n",
        "desc": "Hàm kẹp Trái 3 trụ hoa liên hoàn V7.0 (3 hốc Ø32mm, khe đàn hồi lò xo lá độc lập, gờ đỡ đáy chống tụt, 0% Support)"
    },
    {
        "stl_name": "06_Gripper_Jaw_Right_VGuide_Flower32.stl",
        "scad_code": SCAD_LIBRARY + "\nspecialized_gripper_jaw_3flower(is_left=false);\n",
        "desc": "Hàm kẹp Phải chủ động 3 trụ hoa liên hoàn V7.0 (Hốc đĩa tròn MG996R Ø20.8mm + 8 lỗ M3 PCD Ø14mm, 3 hốc đàn hồi, 0% Support)"
    },
    {
        "stl_name": "01D_K2_Hub_Adapter_Plate.stl",
        "scad_code": SCAD_LIBRARY + "\nk2_adapter_plate_flat();\n",
        "desc": "Tấm sàn phẳng K2 Control Hub Đa Năng V9.0 (Cantilever Dời Lùi Y=-8..82mm Cách Tháp Nâng 23mm + Rãnh Đáy Kín Khóa Tán M3 Chống Rơi + 2 Tay Đòn Trước Né Tháp Nâng) - In phẳng Z=0"
    },
    {
        "stl_name": "01D_MCU_Control_Hub_Deck_FlatPrint.stl",
        "scad_code": SCAD_LIBRARY + "\nmcu_deck_compact_slotted_v80();\n",
        "desc": "Bệ MCU nhỏ gọn Đa Năng V9.0 (Cắt hốc né Tháp Nâng Y=102mm + Rãnh Đáy Kín Khóa Tán M3 + Rãnh trượt trụ X-Y, vừa khít Plate 1) - In phẳng Z=0"
    },
    {
        "stl_name": "01D_Base_Riser_Frame.stl",
        "scad_code": SCAD_LIBRARY + "\nk2_base_riser_frame_printable();\n",
        "desc": "Khung chân đôn trung gian Đa Năng V9.0 (Hạ Thẳng Đứng 100% Không Cần Trượt + Né Tuyệt Đối Tháp Nâng & Servo S1 + 4 Tai Bắt Tấm Sàn Lộ Thiên) - In úp Z=0"
    },
    {
        "stl_name": "01D_K2_Control_Hub_Riser_Adapter_Monolithic.stl",
        "scad_code": SCAD_LIBRARY + "\nk2_adapter_monolithic_printable();\n",
        "desc": "Bản liền khối Đa Năng 1 chi tiết V9.0 (Cantilever Dời Lùi Cách Cụm Gắp Trụ 23-25mm + Rãnh Đáy Kín Giữ Tán M3 + Hạ Thẳng Đứng 100%) - In úp Z=0"
    },
    {
        "stl_name": "01D_K2_Control_Hub_Riser_Adapter_V60.stl",
        "scad_code": SCAD_LIBRARY + "\nk2_adapter_monolithic_printable();\n",
        "desc": "Bản liền khối Đa Năng 1 chi tiết V9.0 (Đồng bộ file V60) - In úp Z=0"
    },
    {
        "stl_name": "01D_Riser_Standoff_18mm.stl",
        "scad_code": SCAD_LIBRARY + "\nriser_standoff_18mm();\n",
        "desc": "Trụ đệm đôn cao 18mm rời (Ø11mm, lỗ bậc chìm 14mm cho ốc M3x12/16mm)"
    },
    {
        "stl_name": "02B_GA25_Rear_Motor_Clamp_Left.stl",
        "scad_code": SCAD_LIBRARY + "\ntranslate([0, 0, 12.0]) rotate([0, -90, 0]) ga25_rear_clamp_left();\n",
        "desc": "Nẹp động cơ GA25 Sau - Trái V4.3 (Vòm Ø26.2mm, khuyết phẳng mép trong 2.5mm, in nằm phẳng bên)"
    },
    {
        "stl_name": "02C_GA25_Rear_Motor_Clamp_Right.stl",
        "scad_code": SCAD_LIBRARY + "\ntranslate([0, 0, 3.5]) rotate([0, -90, 0]) ga25_rear_clamp_right();\n",
        "desc": "Nẹp động cơ GA25 Sau - Phải V4.3 (Vòm Ø26.2mm, khuyết phẳng mép trong 2.5mm, in nằm phẳng bên)"
    },
    {
        "stl_name": "02_GA25_Rear_Motor_Clamp_Universal.stl",
        "scad_code": SCAD_LIBRARY + "\ntranslate([0, 0, 4.0]) rotate([0, -90, 0]) ga25_rear_clamp_universal();\n",
        "desc": "Nẹp động cơ GA25 Sau Dùng Chung V4.3 (Vòm Ø26.2mm, đối xứng 8mm, lắp cả 2 bên)"
    },
    {
        "stl_name": "01C_Lift_Tower_Right_MG996R_FlatPrint.stl",
        "scad_code": SCAD_LIBRARY + "\nlift_tower_right_v50_printable();\n",
        "desc": "Tháp nâng phải MG996R V5.0 (Hốc chìm tán M3, rãnh lượn 1.5mm chống cấn ốc tuyệt đối) - In nằm phẳng Z=0"
    },
    {
        "stl_name": "03_Parallel_Arm_Truss_IBeam.stl",
        "scad_code": SCAD_LIBRARY + "\nlower_h_frame_arm_v50_printable();\n",
        "desc": "Khung tay nâng dưới chữ H V5.0 (Hốc âm đĩa tròn MG996R Ø20.8mm, 8 lỗ M3 PCD Ø14mm, lỗ tâm Ø6.5mm) - In phẳng Z=0"
    },
    {
        "stl_name": "08_S1_MG996R_Round_Horn_Drive_Coupler.stl",
        "scad_code": SCAD_LIBRARY + "\ns1_round_horn_drive_coupler();\n",
        "desc": "Khối khóa đĩa tròn Servo S1 rời V5.0 (Cắm vừa rãnh tay nâng cũ, không cần in lại tay nâng) - In phẳng Z=0"
    },
]

def convert_stl_to_binary(stl_path):
    with open(stl_path, "rb") as f:
        head = f.read(80)
        is_ascii = head.startswith(b"solid") and (b"\n" in head or b"\r" in head)
    if not is_ascii:
        return
    with open(stl_path, "r", errors="ignore") as f:
        text = f.read()
    pattern = re.compile(
        r"facet\s+normal\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+"
        r"outer\s+loop\s+"
        r"vertex\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+"
        r"vertex\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+"
        r"vertex\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+([eE0-9\.\-\+]+)\s+"
        r"endloop\s+endfacet",
        re.DOTALL,
    )
    matches = pattern.findall(text)
    if not matches:
        return
    with open(stl_path, "wb") as f:
        header = b"Binary STL - ORC K2 DFM V5.0".ljust(80, b" ")
        f.write(header)
        f.write(struct.pack("<I", len(matches)))
        for m in matches:
            vals = [float(x) for x in m]
            f.write(struct.pack("<12fH", *vals, 0))

def render_part(part):
    stl_path = os.path.join(STL_DIR, part["stl_name"])
    temp_scad = os.path.join(STL_DIR, "_temp_" + part["stl_name"].replace(".stl", ".scad"))
    
    with open(temp_scad, "w", encoding="utf-8") as f:
        f.write(part["scad_code"])
        
    print(f"-> Đang xuất STL: {part['stl_name']} ({part['desc']})...")
    cmd = [OPENSCAD_COM, "-o", stl_path, temp_scad]
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    if os.path.exists(temp_scad):
        os.remove(temp_scad)
        
    if res.returncode == 0 and os.path.exists(stl_path):
        convert_stl_to_binary(stl_path)
        size = os.path.getsize(stl_path)
        print(f"   [OK] Đã tạo thành công {part['stl_name']} (Kích thước Binary: {size:,} bytes)")
        return True
    else:
        print(f"   [LỖI] Xuất thất bại {part['stl_name']}!")
        print("   Stderr:", res.stderr)
        return False

if __name__ == "__main__":
    print("\n====================================================================")
    print("BẮT ĐẦU XUẤT CÁC TỆP 3D STL THIẾT KẾ LẠI V5.0 THEO YÊU CẦU")
    print("====================================================================")
    success_count = 0
    for p in PARTS:
        if render_part(p):
            success_count += 1
            
    print(f"\n-> Hoàn tất xuất {success_count}/{len(PARTS)} file STL!")
