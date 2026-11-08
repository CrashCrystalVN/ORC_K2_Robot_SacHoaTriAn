import sys
import re

sys.stdout.reconfigure(encoding="utf-8")

with open("canva_curl.html", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's search for image URLs or SVG paths or layout info for Slide 3, 4, 5, 6, 7, 8
# Find all image URLs (.png, .jpg) in the Canva doc
img_urls = re.findall(r'https://[^\"\']+\.(?:png|jpg)[^\"\']*', text)
print(f"Total image URLs: {len(img_urls)}")
for u in img_urls[:20]:
    print("Img:", u[:120])

