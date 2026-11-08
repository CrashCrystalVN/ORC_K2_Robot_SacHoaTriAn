import re

with open("C:/Users/vuasu/.gemini/antigravity/scratch/ORC_K2_Robot_SacHoaTriAn/hub_product.html", "r", encoding="utf-8") as f:
    html = f.read()

imgs = re.findall(r'src=["\'](https://ohstem\.vn/wp-content/uploads/[^"\']+\.(?:jpg|png|webp))["\']', html)
for img in set(imgs):
    if any(k in img.lower() for k in ["control", "hub", "orc", "product", "mach"]):
        print(img)

