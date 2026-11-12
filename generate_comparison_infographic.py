"""
Generate Side-by-Side Visual Comparison Infographic:
Zigzag Base V9.1 vs Balanced Omni Base V10.0
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
MODELS_DIR = os.path.join(BASE_DIR, "3D_Models")

# Source images
img_zigzag_path = os.path.join(MODELS_DIR, "preview_full_assembly_zigzag_top.png")
img_balanced_path = os.path.join(MODELS_DIR, "preview_full_assembly_balanced_top.png")

if not os.path.exists(img_zigzag_path):
    # render it if not existing
    import subprocess
    cmd = [
        r"C:\Program Files\OpenSCAD\openscad.exe",
        "-o", img_zigzag_path,
        "--camera=0,85,60,0,0,0,380",
        "--imgsize=1024,768",
        "--colorscheme=Tomorrow Night",
        os.path.join(MODELS_DIR, "full_assembly_zigzag_omni.scad")
    ]
    subprocess.run(cmd)

im_zz = Image.open(img_zigzag_path).resize((800, 600), Image.Resampling.LANCZOS)
im_bal = Image.open(img_balanced_path).resize((800, 600), Image.Resampling.LANCZOS)

# Create a canvas: 1650 x 850
canvas = Image.new("RGB", (1650, 920), (20, 24, 30))
draw = ImageDraw.Draw(canvas)

# Paste the two images
canvas.paste(im_zz, (20, 160))
canvas.paste(im_bal, (830, 160))

# Try loading standard font or default
try:
    font_title = ImageFont.truetype("arialbd.ttf", 32)
    font_subtitle = ImageFont.truetype("arial.ttf", 20)
    font_header = ImageFont.truetype("arialbd.ttf", 24)
    font_body = ImageFont.truetype("arial.ttf", 18)
    font_badge = ImageFont.truetype("arialbd.ttf", 18)
except:
    font_title = ImageFont.load_default()
    font_subtitle = font_title
    font_header = font_title
    font_body = font_title
    font_badge = font_title

# Header
draw.text((825, 30), "SO SÁNH CƠ HỌC & ĐỘNG HỌC ĐA GIÁC ĐỠ TIẾP ĐẤT", fill=(255, 255, 255), font=font_title, anchor="mt")
draw.text((825, 75), "ZIGZAG BASE V9.1 (BỊ NGHIÊNG/CHÚI ĐẦU) vs BALANCED OMNI BASE V10.0 (CÂN BẰNG ĐỐI XỨNG)", fill=(200, 215, 230), font=font_subtitle, anchor="mt")

# Panels
# Left Panel: Zigzag
draw.rectangle([(20, 115), (820, 155)], fill=(180, 40, 40))
draw.text((420, 135), "BẢN CŨ: ZIGZAG SO LE (BÁNH LỆCH 56MM - BỊ NGHIÊNG/CHÚI)", fill=(255, 255, 255), font=font_header, anchor="mm")

# Annotations on Left
draw.rectangle([(30, 770), (810, 900)], fill=(35, 40, 50), outline=(220, 60, 60), width=2)
lines_zz = [
    "[!] Đa giác tiếp đất bị xiên 23.3 độ (Đường nối Bánh Trước-Phải Y=142 sang Giữa-Trái Y=86mm)",
    "[!] Góc Trước-Bên Trái hổng hoàn toàn 82.5mm không có bánh đỡ (Dưới tháp nâng & tay gắp!)",
    "[!] Khi vươn kẹp hoa hoặc phanh gấp: Trọng tâm dồn ra ngoài đường đỡ -> XE BỊ CHÚI NGHIÊNG!",
    "[!] Động học 4 bánh không đối xứng -> Xe bị nhao lái lệch tâm (Yaw drift) khi chạy thẳng"
]
for idx, l in enumerate(lines_zz):
    draw.text((45, 780 + idx * 28), l, fill=(255, 130, 130) if "[!]" in l else (220, 220, 220), font=font_body)

# Right Panel: Balanced Omni
draw.rectangle([(830, 115), (1630, 155)], fill=(30, 140, 60))
draw.text((1230, 135), "BẢN MỚI: BALANCED OMNI BASE (ĐỐI XỨNG 2 TRƯỚC - 2 SAU)", fill=(255, 255, 255), font=font_header, anchor="mm")

# Annotations on Right
draw.rectangle([(840, 770), (1620, 900)], fill=(35, 40, 50), outline=(50, 200, 80), width=2)
lines_bal = [
    "[✓] Đa giác tiếp đất HÌNH CHỮ NHẬT HOÀN HẢO 158 x 118mm (2 bánh trước Y=142, 2 bánh sau Y=24mm)",
    "[✓] Chống chúi đầu / nghiêng lật 100%: 2 bánh trước đỡ trọn vẹn cả 2 tháp nâng 01B và 01C!",
    "[✓] Động học đối xứng tuyệt đối: Chạy thẳng tắp, quay tròn tại chỗ không lệch tâm, bám line cực chuẩn",
    "[✓] Phủ bì toàn xe: 174 x 176 mm <= 185 mm! Lọt thỏm trong hộp thi đấu, in 3D vừa Bambu A1 Mini"
]
for idx, l in enumerate(lines_bal):
    draw.text((855, 780 + idx * 28), l, fill=(130, 255, 160) if "[✓]" in l else (220, 220, 220), font=font_body)

out_comp = os.path.join(MODELS_DIR, "compare_zigzag_vs_balanced_omni.png")
canvas.save(out_comp)
print(f"Comparison image generated: {out_comp} ({os.path.getsize(out_comp):,} bytes)")
