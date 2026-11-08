import sys
import re
import json

sys.stdout.reconfigure(encoding="utf-8")

with open("canva_curl.html", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

print("Title:", re.findall(r"<title>(.*?)</title>", text))

# Look for meta description
for m in re.finditer(r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', text):
    print("Description:", m.group(1))

for m in re.finditer(r'<meta\s+[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']+)["\']', text):
    print("OG Description:", m.group(1))

# Search for JSON data blobs
scripts = re.findall(r'<script[^>]*>(.*?)</script>', text, re.DOTALL)
print("Scripts count:", len(scripts))

for i, s in enumerate(scripts):
    if "GA25" in s or "Mecanum" in s or "OhStem" in s:
        print(f"Script {i} contains keywords, len={len(s)}")
        # find text snippets in strings
        matches = re.findall(r'["\']([^"\']{4,100})["\']', s)
        for val in matches:
            if any(k in val.lower() for k in ["ga25", "mecanum", "ohstem", "k2", "động cơ", "bánh xe", "servo", "kẹp", "pin", "nhôm", "beam"]):
                print("   Found:", val)
