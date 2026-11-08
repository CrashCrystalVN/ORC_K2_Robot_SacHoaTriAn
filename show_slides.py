import sys
import re

sys.stdout.reconfigure(encoding="utf-8")

with open("canva_curl.html", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's extract items in order and group them by slide / page
# In Canva, pages are usually delimited by page ID or specific markers
items = re.findall(r'\"A\":\s*\[\s*\"([^\"]+)\"\s*\]', text)

slide_num = 1
current_slide_texts = []

for item in items:
    cleaned = item.encode('utf-8').decode('unicode_escape', errors='ignore').replace('\\n', ' ').strip()
    if not cleaned or cleaned.startswith("http") or "www.orc.vn" in cleaned or "contact@ohstem.vn" in cleaned:
        continue
    
    # Check if cleaned is a standalone number indicating slide number
    if re.match(r'^\d{1,2}$', cleaned):
        val = int(cleaned)
        if val > slide_num and val <= slide_num + 3:
            if current_slide_texts:
                print(f"\n==================== SLIDE {slide_num} ====================")
                for t in current_slide_texts:
                    print(f"  * {t}")
                current_slide_texts = []
            slide_num = val
            continue
            
    current_slide_texts.append(cleaned)

if current_slide_texts:
    print(f"\n==================== SLIDE {slide_num} ====================")
    for t in current_slide_texts:
        print(f"  * {t}")

