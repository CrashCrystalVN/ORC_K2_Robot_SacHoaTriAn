"""
Generate Isometric Side-by-Side Comparison:
compare_zigzag_vs_balanced_omni_iso.png
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
MODELS_DIR = os.path.join(BASE_DIR, "3D_Models")

img_zz_iso = os.path.join(MODELS_DIR, "preview_full_assembly_zigzag_iso.png")
img_bal_iso = os.path.join(MODELS_DIR, "preview_full_assembly_balanced_iso.png")

im_zz = Image.open(img_zz_iso).resize((800, 600), Image.Resampling.LANCZOS)
im_bal = Image.open(img_bal_iso).resize((800, 600), Image.Resampling.LANCZOS)

canvas = Image.new("RGB", (1650, 920), (20, 24, 30))
draw = ImageDraw.Draw(canvas)

canvas.paste(im_zz, (20, 160))
canvas.paste(im_bal, (830, 160))

try:
    font_title = ImageFont.truetype("arialbd.ttf", 32)
    font_subtitle = ImageFont.truetype("arial.ttf", 20)
    font_header = ImageFont.truetype("arialbd.ttf", 24)
    font_body = ImageFont.truetype("arial.ttf", 18)
except:
    font_title = ImageFont.load_default()
    font_subtitle = font_title
    font_header = font_title
    font_body = font_title

draw.text((825, 30), "PHỐI CẢNH 3D LẮP RÁP TOÀN XE ROBOT SẮC HOA TRI ÂN", fill=(255, 255, 255), font=font_title, anchor="mt")
draw.text((825, 75), "ZIGZAG V9.1 (GÓC TRƯỚC-TRÁI HỔNG) vs BALANCED OMNI V10.0 (4 BÁNH ĐỐI XỨNG CHỐNG LẬT 100%)", fill=(200, 215, 230), font=font_subtitle, anchor="mt")

draw.rectangle([(20, 115), (820, 155)], fill=(180, 40, 40))
draw.text((420, 135), "BẢN CŨ: ZIGZAG SO LE (THIẾU ĐIỂM TỰA GÓC TRƯỚC)", fill=(255, 255, 255), font=font_header, anchor="mm")

draw.rectangle([(30, 770), (810, 900)], fill=(35, 40, 50), outline=(220, 60, 60), width=2)
lines_zz = [
    "- Bánh Trước-Trái nằm sâu ở Y=86mm, trong khi Tháp nâng 01B vươn tới Y=160mm",
    "- Khi tay gắp mang hoa: Robot bị bập bênh và đổ dồn về góc trước-trái",
    "- 4 Bánh xe không tạo thành hình chữ nhật cân xứng làm lệch hướng di chuyển"
]
for idx, l in enumerate(lines_zz):
    draw.text((45, 785 + idx * 32), l, fill=(255, 160, 160), font=font_body)

draw.rectangle([(830, 115), (1630, 155)], fill=(30, 140, 60))
draw.text((1230, 135), "BẢN MỚI: BALANCED OMNI BASE (CÂN BẰNG ĐỐI XỨNG HOÀN HẢO)", fill=(255, 255, 255), font=font_header, anchor="mm")

draw.rectangle([(840, 770), (1620, 900)], fill=(35, 40, 50), outline=(50, 200, 80), width=2)
lines_bal = [
    "- 2 Bánh trước nằm tại Y=142mm: Đỡ trực tiếp dưới vòm cả 2 tháp nâng 01B & 01C",
    "- 2 Bánh sau nằm tại Y=24mm: Đỡ trọn vẹn phần đuôi xe, chống bập bênh 100%",
    "- Phủ bì toàn xe 174 x 176mm: Lọt gọn trong hộp 185x185mm, in phẳng trên Bambu A1 Mini"
]
for idx, l in enumerate(lines_bal):
    draw.text((855, 785 + idx * 32), l, fill=(160, 255, 180), font=font_body)

out_comp = os.path.join(MODELS_DIR, "compare_zigzag_vs_balanced_omni_iso.png")
canvas.save(out_comp)
print(f"Isometric comparison generated: {out_comp} ({os.path.getsize(out_comp):,} bytes)")
