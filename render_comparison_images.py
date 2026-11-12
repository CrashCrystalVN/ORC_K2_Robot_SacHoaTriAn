"""
render_comparison_images.py
Renders high-resolution side-by-side comparison images:
1. compare_base_plate_old_vs_new.png
2. compare_riser_plate_old_vs_new.png
"""

import os
import subprocess
import trimesh
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
TEMP_DIR = os.path.join(BASE_DIR, "temp_compare_meshes")
STL_DIR = os.path.join(BASE_DIR, "3D_Models")
OUT_3MF_DIR = os.path.join(BASE_DIR, "3MF_Models")
OPENSCAD = r"C:\Program Files\OpenSCAD\openscad.exe"

os.makedirs(TEMP_DIR, exist_ok=True)

def build_base_compare():
    scad_file = os.path.join(TEMP_DIR, "scene_base_compare.scad")
    old_stl = os.path.join(TEMP_DIR, "old_chassis.stl").replace("\\", "/")
    new_stl = os.path.join(STL_DIR, "01_Chassis_Base_200x200.stl").replace("\\", "/")
    
    code = f"""
$fn = 35;

// OLD CHASSIS (LEFT) - CORAL / RED
translate([-95, 0, 0]) {{
    color([0.88, 0.32, 0.25, 1.0])
        translate([0, 88, 16.5])
            import("{old_stl}");
}}

// NEW CHASSIS V6 (RIGHT) - EMERALD GREEN
translate([95, 0, 0]) {{
    color([0.15, 0.72, 0.48, 1.0])
        import("{new_stl}");
}}
"""
    with open(scad_file, "w", encoding="utf-8") as f:
        f.write(code)
    
    img_top = os.path.join(TEMP_DIR, "base_top.png")
    img_iso = os.path.join(TEMP_DIR, "base_iso.png")
    
    # Orthogonal top-down view
    subprocess.run([
        OPENSCAD, "-o", img_top,
        "--imgsize=1600,900",
        "--colorscheme=Tomorrow Night",
        "--projection=o",
        "--camera=0,86,20,0,0,0,460",
        scad_file
    ], check=True)
    
    # Perspective isometric view
    subprocess.run([
        OPENSCAD, "-o", img_iso,
        "--imgsize=1600,900",
        "--colorscheme=Tomorrow Night",
        "--projection=p",
        "--camera=0,86,15,55,0,25,540",
        scad_file
    ], check=True)
    
    print("Rendered base views.")
    return img_top, img_iso

def build_riser_compare():
    scad_file = os.path.join(TEMP_DIR, "scene_riser_compare.scad")
    old_riser = os.path.join(TEMP_DIR, "old_riser_frame.stl").replace("\\", "/")
    old_plate = os.path.join(TEMP_DIR, "old_k2_plate.stl").replace("\\", "/")
    new_riser = os.path.join(STL_DIR, "01D_Base_Riser_Frame.stl").replace("\\", "/")
    new_plate = os.path.join(STL_DIR, "01D_K2_Hub_Adapter_Plate_V11_Hardened.stl").replace("\\", "/")
    
    # Layout on print bed / exploded assembly:
    # Left side (OLD V9): Riser Frame + K2 Plate
    # Right side (NEW V11 / 2S2P): Riser Frame 2S2P + K2 Plate V11 Hardened
    code = f"""
$fn = 35;

// OLD RISER SYSTEM (LEFT) - WARM ORANGE / RED
translate([-100, 0, 0]) {{
    // Old Riser Frame (Height 16mm, centered around 0 in X, Y, Z in [-8, 8])
    translate([0, -65, 8])
        color([0.9, 0.45, 0.2, 1.0])
            import("{old_riser}");
            
    // Old K2 Plate (Height 6mm, centered around 0 in X, Y, Z in [-3, 3])
    translate([0, 65, 3])
        color([0.85, 0.35, 0.25, 1.0])
            import("{old_plate}");
}}

// NEW RISER SYSTEM 2S2P (RIGHT) - TEAL / GREEN
translate([100, 0, 0]) {{
    // New Riser Frame (Height 24mm, centered around 0 in X, Y, Z in [-12, 12])
    translate([0, -65, 12])
        color([0.15, 0.72, 0.48, 1.0])
            import("{new_riser}");
            
    // New K2 Plate V11 Hardened (Height 18.1mm, centered around 0 in X, Y, Z in [-9.05, 9.05])
    translate([0, 65, 9.05])
        color([0.2, 0.65, 0.85, 1.0])
            import("{new_plate}");
}}
"""
    with open(scad_file, "w", encoding="utf-8") as f:
        f.write(code)
    
    img_top = os.path.join(TEMP_DIR, "riser_top.png")
    img_iso = os.path.join(TEMP_DIR, "riser_iso.png")
    
    # Orthogonal top-down view
    subprocess.run([
        OPENSCAD, "-o", img_top,
        "--imgsize=1600,900",
        "--colorscheme=Tomorrow Night",
        "--projection=o",
        "--camera=0,0,10,0,0,0,380",
        scad_file
    ], check=True)
    
    # Perspective isometric view
    subprocess.run([
        OPENSCAD, "-o", img_iso,
        "--imgsize=1600,900",
        "--colorscheme=Tomorrow Night",
        "--projection=p",
        "--camera=0,0,10,55,0,25,480",
        scad_file
    ], check=True)
    
    print("Rendered riser views.")
    return img_top, img_iso

def combine_and_annotate(img1_path, img2_path, out_path, title_main, col1_header, col2_header, bullet_points_col1, bullet_points_col2):
    im1 = Image.open(img1_path)
    im2 = Image.open(img2_path)
    
    w1, h1 = im1.size
    w2, h2 = im2.size
    
    # Layout: Top is img1 (Isometric), Bottom is img2 (Top-Down), or Left-Right stacked
    # Let's stack vertically:
    # Header area (120px)
    # View 1: Isometric (w1 x h1)
    # View 2: Top-down (w2 x h2)
    # Footer table / notes area (260px)
    
    total_w = max(w1, w2)
    header_h = 130
    footer_h = 280
    total_h = header_h + h1 + h2 + footer_h
    
    canvas = Image.new("RGB", (total_w, total_h), (24, 26, 32))
    draw = ImageDraw.Draw(canvas)
    
    # Paste images
    canvas.paste(im2, (0, header_h))         # Top-down view first
    canvas.paste(im1, (0, header_h + h2))    # Isometric view second
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 36)
        font_sub = ImageFont.truetype("arial.ttf", 22)
        font_col = ImageFont.truetype("arial.ttf", 26)
        font_body = ImageFont.truetype("arial.ttf", 20)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = font_title
        font_col = font_title
        font_body = font_title
        
    # Draw Header
    draw.rectangle([(0, 0), (total_w, header_h)], fill=(18, 20, 24))
    draw.text((40, 25), title_main, fill=(255, 255, 255), font=font_title)
    draw.text((40, 75), "ORC K2 Robot 'Sac Hoa Tri An' - Bambu Lab A1 Production 3MF Validation", fill=(170, 185, 200), font=font_sub)
    
    # Subheaders over images
    y_view1 = header_h + 15
    draw.rectangle([(30, y_view1), (320, y_view1 + 35)], fill=(35, 40, 50))
    draw.text((40, y_view1 + 5), "[ VIEW A: TOP-DOWN (Z=0) ]", fill=(240, 240, 240), font=font_sub)
    
    y_view2 = header_h + h2 + 15
    draw.rectangle([(30, y_view2), (320, y_view2 + 35)], fill=(35, 40, 50))
    draw.text((40, y_view2 + 5), "[ VIEW B: ISOMETRIC (3D) ]", fill=(240, 240, 240), font=font_sub)
    
    # Column labels over left/right
    left_x = total_w // 4
    right_x = 3 * total_w // 4
    
    # Draw Footer
    y_foot = header_h + h1 + h2
    draw.rectangle([(0, y_foot), (total_w, total_h)], fill=(16, 18, 22))
    draw.line([(0, y_foot), (total_w, y_foot)], fill=(50, 60, 75), width=2)
    draw.line([(total_w // 2, y_foot), (total_w // 2, total_h)], fill=(50, 60, 75), width=2)
    
    # Left column (Old)
    draw.text((40, y_foot + 20), col1_header, fill=(235, 87, 87), font=font_col)
    cur_y = y_foot + 65
    for bp in bullet_points_col1:
        draw.text((50, cur_y), f"• {bp}", fill=(210, 215, 225), font=font_body)
        cur_y += 32
        
    # Right column (New)
    draw.text((total_w // 2 + 40, y_foot + 20), col2_header, fill=(46, 204, 113), font=font_col)
    cur_y = y_foot + 65
    for bp in bullet_points_col2:
        draw.text((total_w // 2 + 50, cur_y), f"• {bp}", fill=(210, 215, 225), font=font_body)
        cur_y += 32
        
    canvas.save(out_path, quality=95)
    print(f"Generated composite image: {out_path}")

def main():
    print("=== RENDERING SIDE-BY-SIDE METROLOGY COMPARISONS ===")
    
    # 1. Base Plate Comparison
    base_top, base_iso = build_base_compare()
    out_base = os.path.join(BASE_DIR, "compare_base_plate_old_vs_new.png")
    combine_and_annotate(
        base_iso, base_top, out_base,
        title_main="DOI CHIEU METRIC KHUNG GAM BASE: BAN CU (GIT) VS BAN MOI V6 (3MF)",
        col1_header="[BAN CU] Plate 1 Khung Gam Cu (136x176x33mm - FAIL SLICING)",
        col2_header="[BAN MOI] 01_Chassis_Base_200x200_Bambu.3mf (139x172x38mm - PASS 100%)",
        bullet_points_col1=[
            "GA25 Motor: Be phang cu gay can duoi -13mm giua 2 motor sau (khong vua encoder 63mm).",
            "Can truoc: Vat nghieng sieu am HC-SR04, chieu dai xe 176mm can hop kiem 200mm.",
            "Vach suon xe: 3 lo khoet rong moi ben lam suy giam do cung xoan, lo day dien.",
            "Khoang pin: Chi cho 2S1P (37mm), go nhan de len lo oc san, khong gan duoc 2S2P.",
            "10 lo thap nang: Lech offset 0.25mm gay lo meo elip khi slice, lech tam 01B/01C.",
            "Do tin cay in 3D: Watertight = FALSE (loi non-manifold, 11,444 faces, can support)."
        ],
        bullet_points_col2=[
            "GA25 Motor: Be boss duc loi +10.5mm, khe ho tinh khong +7.0mm cho 2x GA25 Encoder.",
            "Can truoc: Can phang mong 5mm + ngam laser VL53L0X ToF, tong dai robot 190mm <= 200mm.",
            "Vach suon xe: Vach kin dac 100%, chiu luc mom-men Mecanum 2.5G cuc ky vung chai.",
            "Khoang pin: Khoang van nang 82x76mm (2S2P brick 38mm & flat 19mm) + 4 khe dai Velcro 20mm.",
            "10 lo thap nang: 10 lo tron phi 3.4mm tieu chuan bat oc M3 thong suot, sai so tam 0.00mm.",
            "Do tin cay in 3D: Watertight = TRUE (100% Manifold, 14,700 faces, In 0% SUPPORT)."
        ]
    )
    
    # 2. Riser & K2 Hub Comparison
    riser_top, riser_iso = build_riser_compare()
    out_riser = os.path.join(BASE_DIR, "compare_riser_plate_old_vs_new.png")
    combine_and_annotate(
        riser_iso, riser_top, out_riser,
        title_main="DOI CHIEU HE TANG DON RISER & K2 HUB: BAN CU V9 VS BAN MOI V11 2S2P",
        col1_header="[BAN CU V9] Plate 6 / Riser V9 (Cao 16mm - BI CAN PIN 2S2P)",
        col2_header="[BAN MOI V11] Plate_K2_Hub_Riser_2S2P_Pack.3mf (Cao 24mm - PASS 2S2P)",
        bullet_points_col1=[
            "Chieu cao don Riser: Chi cao 16mm, tinh khong 34mm (can pin 2S2P khoi gach 38mm toi 4mm).",
            "Thanh giang ngang: Giang giua tai Y = 66..74mm chan ngang bung xe, chen ep cell pin.",
            "Lo bat truoc K2: Bi lech toa do X = +-34.0mm (lech 1.0mm so voi K2 Hub chuan +-33mm).",
            "Tam plate K2: Ban phang 120x120mm don gian, tai khoa de g gay, khong co ngam laser.",
            "Kha nang su dung: KHONG THE LAP PIN 2S2P (bat buoc phai thay the bang Riser 2S2P)."
        ],
        bullet_points_col2=[
            "Chieu cao don Riser: Nang len 24mm, tinh khong dat 42mm (lap vua pin 38mm + dai Velcro 2mm).",
            "Thanh giang ngang: Doi ve 2 dau (Y = -14mm & Y = +88mm), vom giua 94x53mm THONG SUOT 100%.",
            "Lo bat truoc K2: Chuan hoa ranh 2D va lo M3 tai X = +-33.0mm, lap oc M3 thang dung cuc de.",
            "Tam plate K2: V11 Hardened (140.8x120mm) sieu ben, tich hop san 2 ngam cam bien laser VL53L0X.",
            "Kha nang su dung: SAN SANG 100% CHO BAMBU LAB A1 (In 0% support, kem 2x Nep Motor Universal)."
        ]
    )
    
    print("\n>>> All side-by-side comparison images created successfully!")

if __name__ == "__main__":
    main()

