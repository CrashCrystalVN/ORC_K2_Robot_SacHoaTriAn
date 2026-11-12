
$fn = 40;

// ====================================================================
// 1. KHUNG CHAN DON K2 HUB CHO PIN 2S2P (01D_Base_Riser_Frame_2S2P)
// ====================================================================
// - Nang tam bat K2 Hub len Z_top = 46.0mm (hoac 48.0mm):
//   + Mat day san xe Z = 4.0mm -> Khoang sang gam lot long: H_clear = 46.0 - 4.0 = 42.0mm!
//   + Dat vua khit khoi pin 2S2P 38 x 38 x 70mm + day dai Velcro 2mm + khe ho an toan 2mm!
// - 4 Chan don ha thang dung xuong 4 tru khung gam (Z = 22.0mm) tai X = +-33.0, Y = 49.0 & 99.0
//   + Day chan day 4.5mm (Z = 22.0..26.5mm) bat oc M3x10/12mm cuc de
//   + Gieng mo thong suot tu Z = 26.5 len Z_top giup van oc thang dung tu tren xuong
// - 2 Thanh giang ngang duoc bo tri NÉ PIN 2S2P 100%:
//   + Giang sau tai Y in [-18.0, -10.0mm] (phia sau pin)
//   + Giang truoc tai Y in [84.0, 92.0mm] (phia truoc pin)
//   + Toan bo khoang giua X in [-26.5, +26.5mm], Y in [0, 84mm] THONG SUOT 100% khong vuong giang!
// - 4 Tai khoa nhanh lo thien co san hoc giu tan M3 day kin chong roi
// - In lat up 180° (mat Z_top nam sat ban in): IN 0% SUPPORT!
// ====================================================================
module k2_base_riser_frame_2s2p(Z_top = 46.0) {
    difference() {
        union() {
            for (sx = [-1, 1]) {
                // 1. Hai Chan Tru Sau (|X| in [26.5, 39.2], Y in [45.0, 56.5], Z in [22.0, Z_top]):
                translate([sx * 32.85 - 6.35, 45.0, 22.0])
                    cube([12.7, 11.5, Z_top - 22.0]);
                    
                // 2. Hai Chan & Tay Tru Truoc Ne Thap Nang (|X| in [29.2, 39.2], Y in [82.0, 102.0], Z in [22.0, Z_top]):
                translate([sx * 34.2 - 5.0, 82.0, 22.0])
                    cube([10.0, 20.0, Z_top - 22.0]);
                    
                // 3. Dam doc tren noi lien tu Tai Sau (Y = -18.0) den Tay Truoc (Y = 85.0) tai Z in [Z_top - 7.0, Z_top]:
                translate([sx * 33.5 - 5.7, -18.0, Z_top - 7.0])
                    cube([11.4, 103.0, 7.0]);
                    
                // 4. Khoi Tai Khoa Sau Lo Thien day 8mm (|X| in [25.5, 40.5], Y in [-18.0, -7.0], Z in [Z_top - 8.0, Z_top]):
                translate([sx * 33.0 - 7.5, -18.0, Z_top - 8.0])
                    cube([15.0, 11.0, 8.0]);
            }
            
            // 5. Hai Thanh Giang Ngang Chu H NE HOAN TOAN PIN 2S2P:
            //    - Giang Sau: Tai Y in [-18.0, -10.0mm], Z in [Z_top - 6.0, Z_top] (Noi lien 2 tai sau)
            //    - Giang Truoc: Tai Y in [84.0, 92.0mm], Z in [Z_top - 6.0, Z_top] (Noi lien 2 tay truoc)
            //    -> Toan bo khoang tu Y = -10.0 den Y = 84.0mm (dai 94mm, rong 53mm) TRONG 100% cho Pin 2S2P 38x70mm!
            translate([-33.0, -17.0, Z_top - 6.0]) cube([66.0, 8.0, 6.0]);
            translate([-33.0, 84.0, Z_top - 6.0])  cube([66.0, 8.0, 6.0]);
        }
        
        // Vát goc day sau Chan Sau (Y = 45.0..47.5, Z = 22.0..27.0) tranh 100% than motor GA25:
        for (sx = [-1, 1]) {
            translate([sx * 33.0 - 7.5, 42.5, 21.0])
                rotate([38, 0, 0])
                    cube([15.0, 4.5, 8.0]);
        }
        
        // A. 2 HOC BAT TRU SAU (X = +-33.0, Y = 47.5..50.5):
        //    Day Z = 22.0..26.5mm (day 4.5mm), phia tren Z = 26.5..Z_top mo gieng thang dung O7.6mm
        for (sx = [-1, 1]) {
            // Lo truot oc M3 qua day day 4.5mm (Z = 22.0..26.5mm):
            hull() {
                translate([sx * 33.0, 47.5, 20.0]) cylinder(d=3.6, h=20.0);
                translate([sx * 33.0, 50.5, 20.0]) cylinder(d=3.6, h=20.0);
            }
            // Non chuyen tiep tu do 45° tu lo M3 len gieng dau oc:
            hull() {
                translate([sx * 33.0, 47.5, 26.5]) cylinder(d1=3.6, d2=7.6, h=2.5);
                translate([sx * 33.0, 50.5, 26.5]) cylinder(d1=3.6, d2=7.6, h=2.5);
            }
            // Gieng dung tha oc M3 & luc giac van thang dung tu tren xuong (Z = 28.9..Z_top+1):
            hull() {
                translate([sx * 33.0, 47.5, 28.9]) cylinder(d=7.6, h=Z_top - 27.9);
                translate([sx * 33.0, 50.5, 28.9]) cylinder(d=7.6, h=Z_top - 27.9);
            }
        }
        
        // B. 2 HOC BAT TRU TRUOC LO THIEN (X = +-32.0..35.5, Y = 95.5..99.5):
        //    Day Z = 22.0..26.5mm (day 4.5mm), phia tren Z = 26.5..Z_top mo thong ra phia truoc & mep ngoai:
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
                translate([sx * 32.5, 95.5, 29.4]) cylinder(d=8.5, h=Z_top - 28.4);
                translate([sx * 35.5, 95.5, 29.4]) cylinder(d=8.5, h=Z_top - 28.4);
                translate([sx * 32.5, 103.5, 29.4]) cylinder(d=8.5, h=Z_top - 28.4);
                translate([sx * 38.5, 99.5, 29.4]) cylinder(d=8.5, h=Z_top - 28.4);
            }
        }
        
        // C. 2 RANH KHOA TAN M3 DAY KIN O TAI SAU LO THIEN (X = +-33.0, Y = -15.0 .. -11.0):
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 33.0, -15.0, Z_top - 10.0]) cylinder(d=3.3, h=12.0);
                translate([sx * 33.0, -11.0, Z_top - 10.0]) cylinder(d=3.3, h=12.0);
            }
            // Ranh khoa tan M3 co day do 1.2mm + cua nhet tan tu duoi Y = -19.0:
            hull() {
                translate([sx * 33.0, -19.0, Z_top - 6.8]) cylinder(d=5.65, h=2.9);
                translate([sx * 33.0, -11.0, Z_top - 6.8]) cylinder(d=5.65, h=2.9);
            }
            hull() {
                translate([sx * 33.0, -19.0, Z_top - 4.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
                translate([sx * 33.0, -11.0, Z_top - 4.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
            }
        }
        
        // D. 2 RANH KHOA TAN M3 DAY KIN O TAI TRUOC LO THIEN (X = +-34.0, Y = 86.0 .. 90.0):
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 34.0, 86.0, Z_top - 12.0]) cylinder(d=3.3, h=14.0);
                translate([sx * 34.0, 90.0, Z_top - 12.0]) cylinder(d=3.3, h=14.0);
            }
            hull() {
                translate([sx * 34.0, 86.0, Z_top - 6.8]) cylinder(d=5.65, h=2.9);
                translate([sx * 34.0, 90.0, Z_top - 6.8]) cylinder(d=5.65, h=2.9);
                translate([sx * 40.5, 88.0, Z_top - 6.8]) cylinder(d=5.65, h=2.9);
            }
            hull() {
                translate([sx * 34.0, 86.0, Z_top - 4.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
                translate([sx * 34.0, 90.0, Z_top - 4.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
                translate([sx * 40.5, 88.0, Z_top - 4.0]) cylinder(d1=5.65, d2=3.3, h=1.6);
            }
        }
    }
}

module k2_base_riser_frame_2s2p_printable(Z_top = 46.0) {
    translate([0, 0, Z_top])
        rotate([180, 0, 0])
            k2_base_riser_frame_2s2p(Z_top = Z_top);
}

// ====================================================================
// 2. TRU DON ROII MODULE CHO PIN 2S2P (01D_Riser_Standoff_24mm_2S2P)
// ====================================================================
// - Don cao them 24mm (Z = 22.0 + 24.0 = 46.0mm -> H_clear = 42.0mm)
// - Duong kinh O11.0mm, lo xuyen O3.4mm, gieng am M3 sau 19mm
module riser_standoff_24mm_2s2p(h = 24.0) {
    difference() {
        cylinder(d=11.0, h=h);
        translate([0, 0, -1.0]) cylinder(d=3.4, h=h + 2.0);
        translate([0, 0, 5.0]) cylinder(d=7.2, h=h);
    }
}

// ====================================================================
// 3. BAN ADAPTER LIEN KHOI DON CAO CHO PIN 2S2P (01D_K2_Control_Hub_Riser_Adapter_Monolithic_2S2P)
// ====================================================================
// - Tich hop toan bo chan don + san do K2 Hub + 2 canh ga ToF VL53L0X
// - Z_bot = 46.0mm -> H_clear = 46.0 - 4.0 = 42.0mm!
// - T_deck = 5.0mm -> Z_top = 51.0mm (Dinh K2 Hub Z = 51.0 + 26.0 = 77.0mm < 78.0mm)
// - In lat up 180°: 100% Zero Support!
module vl53l0x_pod_half(T_deck = 5.0, Z_base = 0.0) {
    difference() {
        union() {
            hull() {
                translate([56.0, 66.0, Z_base]) cube([4.0, 16.5, T_deck]);
                translate([68.2, 67.5, Z_base]) cylinder(r=2.2, h=T_deck + 6.0);
                translate([68.2, 81.0, Z_base]) cylinder(r=2.2, h=T_deck + 6.0);
                translate([56.0, 82.5, Z_base]) cube([4.0, 0.1, T_deck]);
            }
            for (py = [70.0, 78.5]) {
                translate([68.6, py - 2.2, Z_base]) cube([1.8, 4.4, T_deck + 6.0]);
                translate([68.6, py - 2.2, Z_base + T_deck + 4.5])
                    hull() {
                        cube([1.8, 4.4, 1.5]);
                        translate([-1.0, 0, 0]) cube([0.1, 4.4, 1.0]);
                    }
            }
            translate([66.2, 68.0, Z_base]) cube([1.4, 13.0, T_deck + 5.5]);
        }
        translate([67.6, 67.5, Z_base + 1.5]) cube([2.1, 14.0, 15.0]);
        translate([64.5, 68.5, Z_base + 2.8]) cube([8.0, 11.0, 6.5]);
        hull() {
            translate([66.0, 68.5, Z_base + 2.8]) cube([0.1, 11.0, 6.5]);
            translate([70.0, 67.5, Z_base + 1.5]) cube([0.1, 13.0, 9.2]);
        }
        translate([63.5, 67.5, Z_base - 1.0]) cylinder(d=3.3, h=T_deck + 10.0);
        translate([63.5, 81.5, Z_base - 1.0]) cylinder(d=3.3, h=T_deck + 10.0);
        translate([56.0, 74.0, Z_base + 2.5]) cube([12.0, 5.0, T_deck + 2.0]);
    }
}

module vl53l0x_maze_sensor_pod(is_left = true, T_deck = 5.0, Z_base = 0.0) {
    if (is_left) {
        mirror([1, 0, 0]) vl53l0x_pod_half(T_deck = T_deck, Z_base = Z_base);
    } else {
        vl53l0x_pod_half(T_deck = T_deck, Z_base = Z_base);
    }
}

module k2_adapter_monolithic_2s2p(Z_bot = 46.0, T_deck = 5.0) {
    Z_top = Z_bot + T_deck; // 51.0mm
    
    difference() {
        union() {
            // 1. Mat san chinh (120.0 x 90.0 x 5.0 mm, X in [-60, 60], Y in [-8.0, 82.0]):
            translate([-60.0, -8.0, Z_bot])
                cube([120.0, 90.0, T_deck]);
                
            // 2. Hai Chan Don Sau Ha Thang Dung (|X| in [26.5, 39.2], Y in [45.0, 56.5], Z in [22.0, Z_bot]):
            for (sx = [-1, 1]) {
                translate([sx * 32.85 - 6.35, 45.0, 22.0])
                    cube([12.7, 11.5, Z_bot - 22.0]);
            }
            
            // 3. Hai Tay/Chan Don Truoc LO THIEN NGOAI K2 HUB & NE THAP NANG 100%
            //    (|X| in [29.2, 39.2], Y in [81.0, 102.0], Z in [22.0, Z_top]):
            for (sx = [-1, 1]) {
                translate([sx * 34.2 - 5.0, 81.0, 22.0])
                    cube([10.0, 21.0, Z_top - 22.0]);
            }
            
            // 4. Hai Cum Ga Laser ToF VL53L0X
            vl53l0x_maze_sensor_pod(is_left=true, T_deck=T_deck, Z_base=Z_top - 12.0);
            vl53l0x_maze_sensor_pod(is_left=false, T_deck=T_deck, Z_base=Z_top - 12.0);
        }
        
        // Vat goc day sau Chan Sau tranh than motor:
        for (sx = [-1, 1]) {
            translate([sx * 33.0 - 7.5, 42.5, 21.0])
                rotate([38, 0, 0])
                    cube([15.0, 4.5, 8.0]);
        }
        
        // O thoang trung tam rong rai cho cap nguon Pin 2S2P & thoat nhiet (44.0 x 44.0 mm, Y in [18.0, 62.0]):
        translate([-22.0, 18.0, 20.0])
            cube([44.0, 44.0, Z_top + 2.0]);
            
        // A. 2 CHIEU BAT TRU SAU KEM GIENG VAN OC XUYEN SUOT (X = +-31.5..35.0, Y = 46.5..51.5):
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 31.5, 46.5, 20.0]) cylinder(d=3.6, h=Z_top - 18.0);
                translate([sx * 35.0, 46.5, 20.0]) cylinder(d=3.6, h=Z_top - 18.0);
                translate([sx * 31.5, 51.5, 20.0]) cylinder(d=3.6, h=Z_top - 18.0);
                translate([sx * 35.0, 51.5, 20.0]) cylinder(d=3.6, h=Z_top - 18.0);
            }
            hull() {
                translate([sx * 31.5, 46.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
                translate([sx * 35.0, 46.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
                translate([sx * 31.5, 51.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
                translate([sx * 35.0, 51.5, 26.5]) cylinder(d1=3.6, d2=9.2, h=3.0);
            }
            hull() {
                translate([sx * 31.5, 46.5, 29.4]) cylinder(d=9.2, h=Z_top - 28.0);
                translate([sx * 35.0, 46.5, 29.4]) cylinder(d=9.2, h=Z_top - 28.0);
                translate([sx * 31.5, 51.5, 29.4]) cylinder(d=9.2, h=Z_top - 28.0);
                translate([sx * 35.0, 51.5, 29.4]) cylinder(d=9.2, h=Z_top - 28.0);
            }
        }
        
        // B. 2 TAY/CHAN TRUOC LO THIEN NGOAI K2 HUB (X = +-32.0..35.5, Y = 95.5..99.5):
        for (sx = [-1, 1]) {
            hull() {
                translate([sx * 32.0, 95.5, 20.0]) cylinder(d=3.6, h=Z_top - 18.0);
                translate([sx * 35.5, 95.5, 20.0]) cylinder(d=3.6, h=Z_top - 18.0);
                translate([sx * 32.0, 99.5, 20.0]) cylinder(d=3.6, h=Z_top - 18.0);
                translate([sx * 35.5, 99.5, 20.0]) cylinder(d=3.6, h=Z_top - 18.0);
            }
            hull() {
                translate([sx * 32.5, 95.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
                translate([sx * 35.5, 95.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
                translate([sx * 32.5, 103.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
                translate([sx * 38.5, 99.5, 26.5]) cylinder(d1=3.6, d2=8.5, h=3.0);
            }
            hull() {
                translate([sx * 32.5, 95.5, 29.4]) cylinder(d=8.5, h=Z_top - 28.0);
                translate([sx * 35.5, 95.5, 29.4]) cylinder(d=8.5, h=Z_top - 28.0);
                translate([sx * 32.5, 103.5, 29.4]) cylinder(d=8.5, h=Z_top - 28.0);
                translate([sx * 38.5, 99.5, 29.4]) cylinder(d=8.5, h=Z_top - 28.0);
            }
        }
        
        // C. 4 RANH TRUOT DON GON GANG TAI 4 GOC K2 CONTROL HUB:
        for (sx = [-1, 1]) {
            for (sy = [6.0, 68.0]) {
                hull() {
                    translate([sx * 44.0, sy, Z_bot - 1.0]) cylinder(d=3.4, h=T_deck + 2.0);
                    translate([sx * 53.0, sy, Z_bot - 1.0]) cylinder(d=3.4, h=T_deck + 2.0);
                }
                hull() {
                    translate([sx * 44.0, sy, Z_top - 2.5]) cylinder(d=6.5, h=3.0);
                    translate([sx * 53.0, sy, Z_top - 2.5]) cylinder(d=6.5, h=3.0);
                }
            }
        }
    }
}

module k2_adapter_monolithic_2s2p_printable(Z_bot = 46.0, T_deck = 5.0) {
    translate([0, 0, Z_bot + T_deck])
        rotate([180, 0, 0])
            k2_adapter_monolithic_2s2p(Z_bot = Z_bot, T_deck = T_deck);
}


k2_adapter_monolithic_2s2p_printable(Z_bot=46.0, T_deck=5.0);
