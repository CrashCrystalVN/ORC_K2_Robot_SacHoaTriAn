import sys
import re
import urllib.request
import ssl
import os

with open("canva_curl.html", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

doc_imgs = re.findall(r'(https://media\.canva\.com/v2/document-image/[^\"]+)', text)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

out_dir = r"C:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\canva_slides"

for i in range(12, len(doc_imgs)):
    url = doc_imgs[i].replace('&amp;', '&')
    out_path = os.path.join(out_dir, f"slide_{i+1}.jpg")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            with open(out_path, "wb") as out_f:
                out_f.write(resp.read())
        print(f"Saved slide_{i+1}.jpg ({os.path.getsize(out_path)} bytes)")
    except Exception as e:
        print(f"Error {i+1}: {e}")

