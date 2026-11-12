"""
Generate Comprehensive Presentation Infographic for Ultra-Slim 120 Omni Chassis Base
File: presentation_chassis_slim120_omni.png
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
MODELS_DIR = os.path.join(BASE_DIR, "3D_Models")

img_iso_path = os.path.join(MODELS_DIR, "preview_full_assembly_slim120_iso.png")
img_top_path = os.path.join(MODELS_DIR, "preview_full_assembly_slim120_top.png")
img_bot_path = os.path.join(MODELS_DIR, "preview_chassis_slim120_bottom.png")

im_iso = Image.open(img_iso_path).resize((900, 675), Image.Resampling.LANCZOS)
im_top = Image.open(img_top_path).resize((700, 330), Image.Resampling.LANCZOS)
im_bot = Image.open(img_bot_path).resize((700, 330), Image.Resampling.LANCZOS)

# Canvas: 1650 x 920
canvas = Image.new("RGB", (1650, 920), (16, 20, 26))
draw = ImageDraw.Draw(canvas)

# Paste panels
canvas.paste(im_iso, (25, 180))
canvas.paste(im_top, (935, 180))
canvas.paste(im_bot, (935, 525))

# Fonts
try:
    font_title = ImageFont.truetype("arialbd.ttf", 30)
    font_sub = ImageFont.truetype("arial.ttf", 18)
    font_header = ImageFont.truetype("arialbd.ttf", 20)
    font_body = ImageFont.truetype("arial.ttf", 15)
    font_badge = ImageFont.truetype("arialbd.ttf", 14)
except Exception:
    font_title = ImageFont.load_default()
    font_sub = font_title
    font_header = font_title
    font_body = font_title
    font_badge = font_title

# Title Banner
draw.rectangle([(0, 0), (1650, 140)], fill=(24, 30, 40))
draw.line([(0, 140), (1650, 140)], fill=(0, 200, 255), width=3)

draw.text((825, 35), "ORC-K2 PRO: KHUNG GẦM ULTRA-SLIM 120 (TỔNG TRỤC X < 120MM)", fill=(255, 255, 255), font=font_title, anchor="mt")
draw.text((825, 80), "BỐ TRÍ ĐỘNG CƠ ZIGZAG ĐAN CHÉO ĐUÔI + TÍCH HỢP 4 ĐIỂM TỰA TRỢ LỰC CHỐNG CHÚI / BẬP BÊNH", fill=(0, 210, 255), font=font_sub, anchor="mt")
draw.text((825, 110), "TỔNG PHỦ BÌ XE CẢ BÁNH: 116.0 MM <= 118.0 MM < 120.0 MM (PASS 100% QUI ĐỊNH)", fill=(120, 255, 160), font=font_badge, anchor="mt")

# Left Panel Box (Full Assembly)
draw.rectangle([(20, 155), (930, 890)], outline=(60, 75, 95), width=2)
draw.rectangle([(25, 160), (925, 195)], fill=(30, 40, 55))
draw.text((475, 178), "PHỐI CẢNH 3D LẮP RÁP TỔNG THỂ (FULL PACKAGING ISO)", fill=(255, 255, 255), font=font_header, anchor="mm")

# Top Right Box (Top View & X < 120 Dimensioning)
draw.rectangle([(930, 155), (1640, 515)], outline=(60, 75, 95), width=2)
draw.rectangle([(935, 160), (1635, 195)], fill=(30, 40, 55))
draw.text((1285, 178), "TOP VIEW: KIỂM CHỨNG TỔNG TRỤC X = 116.0MM < 120.0MM", fill=(120, 255, 160), font=font_header, anchor="mm")

# Bottom Right Box (Underbody & Anti-Tip Caster Balls)
draw.rectangle([(930, 520), (1640, 890)], outline=(60, 75, 95), width=2)
draw.rectangle([(935, 525), (1635, 560)], fill=(30, 40, 55))
draw.text((1285, 543), "MẶT GẦM: 4 CỤM ĐIỂM TỰA TRỢ LỰC CHỐNG BẬP BÊNH / CHỐNG CHÚI", fill=(255, 200, 80), font=font_header, anchor="mm")

# Overlay Badges and Metric Callouts
# Left panel badges:
draw.rectangle([(40, 210), (320, 280)], fill=(20, 26, 36, 220), outline=(0, 200, 255), width=2)
draw.text((50, 222), "• 4x Động cơ GA25 Zigzag", fill=(255, 255, 255), font=font_body)
draw.text((50, 242), "• Tầng 1: Sàn pin 01D 2S2P", fill=(200, 220, 255), font=font_body)
draw.text((50, 262), "• Tầng 2: Bo mạch K2 Hub", fill=(120, 255, 160), font=font_body)

draw.rectangle([(640, 210), (910, 280)], fill=(20, 26, 36, 220), outline=(255, 180, 50), width=2)
draw.text((650, 222), "• Bi trợ lực Caster Ball Ø12", fill=(255, 215, 100), font=font_body)
draw.text((650, 242), "• Triệt tiêu chúi góc trước trái", fill=(255, 255, 255), font=font_body)
draw.text((650, 262), "• Triệt tiêu bập bênh sau phải", fill=(255, 255, 255), font=font_body)

# Top Right metric callouts:
draw.rectangle([(950, 210), (1240, 275)], fill=(20, 30, 45), outline=(0, 255, 180), width=2)
draw.text((960, 220), "Bề rộng thân: 72.0 mm", fill=(255, 255, 255), font=font_body)
draw.text((960, 238), "Bề rộng phủ bì xe: 116.0 mm", fill=(120, 255, 160), font=font_header)
draw.text((960, 258), "Khoảng dư an toàn: 4.0 mm", fill=(200, 220, 255), font=font_body)

# Bottom Right metric callouts:
draw.rectangle([(950, 575), (1330, 640)], fill=(20, 30, 45), outline=(255, 180, 50), width=2)
draw.text((960, 585), "• Gá bi mắt trâu CY-12A / Vấu trượt", fill=(255, 215, 100), font=font_body)
draw.text((960, 603), "• Hốc định vị Ø14mm + 2 lỗ M3 (16mm)", fill=(255, 255, 255), font=font_body)
draw.text((960, 621), "• Đáy phẳng Z=0, FDM 0% Support", fill=(120, 255, 160), font=font_body)

# Footer bar
draw.rectangle([(0, 895), (1650, 920)], fill=(20, 24, 32))
draw.text((825, 907), "ORC K2 STEM Robot Design System • Verified with Trimesh & OpenSCAD • 100% Bambu Lab A1 Mini Compatible", fill=(130, 145, 165), font=font_badge, anchor="mm")

out_infographic = os.path.join(MODELS_DIR, "presentation_chassis_slim120_omni.png")
canvas.save(out_infographic)
print(f"Generated Presentation Infographic: {out_infographic} ({os.path.getsize(out_infographic):,} bytes)")
