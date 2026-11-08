import sys
import re
import urllib.request
import ssl
import os

sys.stdout.reconfigure(encoding="utf-8")

with open("canva_curl.html", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Find document image URLs
doc_imgs = re.findall(r'(https://media\.canva\.com/v2/document-image/[^\"]+)', text)
print(f"Total doc images: {len(doc_imgs)}")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

out_dir = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\canva_slides"
os.makedirs(out_dir, exist_ok=True)

for i, url in enumerate(doc_imgs[:12]):
    url_clean = url.replace('&amp;', '&')
    out_path = os.path.join(out_dir, f"slide_{i+1}.jpg")
    try:
        req = urllib.request.Request(url_clean, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            with open(out_path, "wb") as out_f:
                out_f.write(resp.read())
        print(f"Saved slide_{i+1}.jpg ({os.path.getsize(out_path)} bytes)")
    except Exception as e:
        print(f"Error downloading {i+1}: {e}")

