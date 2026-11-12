import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn"
IMG_PATH = os.path.join(BASE_DIR, "preview_standoff_26mm_44mm_dualnut.png")

def annotate_image():
    im = Image.open(IMG_PATH).convert("RGBA")
    w, h = im.size

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Load system font if available, else default
    font_title = None
    font_sec = None
    font_body = None
    font_callout = None

    for fn in ["arial.ttf", "segoeui.ttf", "calibri.ttf"]:
        try:
            font_title = ImageFont.truetype(fn, 34)
            font_sec = ImageFont.truetype(fn, 22)
            font_body = ImageFont.truetype(fn, 18)
            font_callout = ImageFont.truetype(fn, 16)
            break
        except Exception:
            continue

    if font_title is None:
        font_title = font_sec = font_body = font_callout = ImageFont.load_default()

    # 1. Header Banner (Top-Left)
    draw.rounded_rectangle([40, 30, 480, 220], radius=12, fill=(20, 24, 30, 220), outline=(0, 200, 255, 200), width=2)
    draw.text((60, 45), "ORC K2 DUAL-NUT STANDOFF M3", font=font_title, fill=(0, 220, 255, 255))
    draw.text((60, 92), "KIỂU CÀI 2 TÁN LỤC GIÁC M3 TỪ BÊN HÔNG", font=font_sec, fill=(255, 175, 40, 255))
    
    spec_lines = [
        "• Tiết diện: Ø11.6mm kèm vát phẳng D-flat (R_-Y = 5.3mm <= 5.5mm)",
        "• Hốc tán M3: 5.80 x 2.75mm, khoét quá tâm 3.25mm (DIN 934)",
        "• Bệ chịu lực: 3.50mm mỗi đầu | Lỗ trục xuyên suốt: Ø3.50mm",
        "• Bắt 2 ốc M3 ngắn độc lập từ 2 đầu | DFM In đứng 0% Support"
    ]
    y_text = 125
    for l in spec_lines:
        draw.text((60, y_text), l, font=font_callout, fill=(220, 230, 240, 240))
        y_text += 22

    # 2. Specs Badge (Lower-Left)
    draw.rounded_rectangle([40, 240, 480, 410], radius=12, fill=(20, 24, 30, 220), outline=(255, 140, 0, 180), width=2)
    draw.text((60, 255), "THÔNG SỐ & KHÔNG GIAN BỐ TRÍ", font=font_sec, fill=(255, 160, 30, 255))
    info_lines = [
        "• 26mm Standoff (01D_Riser_Standoff_26mm_2S2P):",
        "  - Ghép chồng hoặc đôn khung, dùng mọi ốc M3x10/12/16mm",
        "• 44mm Standoff (01D_Riser_Standoff_44mm_2S2P):",
        "  - Nâng thẳng K2 Hub từ sàn Z=4mm lên Z=48mm (H_clear=44mm)",
        "  - Chứa vừa khít Pin gạch 2S2P (38mm) chỉ với 1 bộ 4 cọc duy nhất!",
        "• Khe hở nẹp motor sau GA25: >= 0.493mm (Tuyệt đối không cấn!)"
    ]
    y_info = 285
    for l in info_lines:
        draw.text((60, y_info), l, font=font_callout, fill=(210, 225, 235, 230))
        y_info += 19

    # 3. Model Column Labels at Bottom
    # Model 1: ~X=620, Model 2: ~X=930, Model 3: ~X=1280, Model 4: ~X=1600
    cols = [
        (560, 970, 740, 1045, "Standoff 26mm (Ngoại quan)", "2 Khe cài tán M3 ngang hông", (255, 150, 0)),
        (830, 970, 1070, 1045, "Mặt cắt 26mm + 2 Tán + 2 Ốc", "Bắt 2 ốc M3 ngắn liên tiếp 2 đầu", (0, 210, 255)),
        (1170, 970, 1370, 1045, "Standoff 44mm Nguyên khối", "Nâng thẳng K2 Hub lên Z=48mm", (255, 150, 0)),
        (1470, 970, 1750, 1045, "Mặt cắt 44mm + 2 Tán + 2 Ốc", "Lọt lòng 44mm cho Pin gạch 2S2P", (0, 210, 255)),
    ]
    for x1, y1, x2, y2, title, sub, color_rgb in cols:
        draw.rounded_rectangle([x1, y1, x2, y2], radius=8, fill=(15, 20, 26, 230), outline=(*color_rgb, 200), width=2)
        draw.text((x1 + 12, y1 + 10), title, font=font_callout, fill=(*color_rgb, 255))
        draw.text((x1 + 12, y1 + 35), sub, font=font_callout, fill=(200, 210, 220, 220))

    # Composite and save
    out = Image.alpha_composite(im, overlay).convert("RGB")
    out.save(IMG_PATH, "PNG")
    print(f"Annotated preview image saved -> {IMG_PATH} ({os.path.getsize(IMG_PATH):,} bytes)")

if __name__ == "__main__":
    annotate_image()

