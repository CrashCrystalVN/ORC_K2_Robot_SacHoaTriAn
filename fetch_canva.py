import urllib.request
import ssl
import json
import re

url = "https://www.canva.com/design/DAG7vVnbD5g/BGgMI_RwMW461QmWgZkAsA/view?utlId=h9652c4cc09#10"
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
        print("Status:", resp.status)
        print("HTML length:", len(html))
        
        # Save HTML for analysis
        with open("canva_page.html", "w", encoding="utf-8") as f:
            f.write(html)
            
        titles = re.findall(r"<title>(.*?)</title>", html)
        print("Title:", titles)
        
        # Search for any embedded JSON or text
        script_matches = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
        print("Scripts found:", len(script_matches))
        
        # Look for text strings in scripts or body
        text_snippets = set()
        for m in re.finditer(r'["\']([A-Za-z0-9_\sÀ-ỹ\-]{4,50})["\']', html):
            s = m.group(1).strip()
            if any(k in s.lower() for k in ["ohstem", "ga25", "mecanum", "servo", "k2", "động cơ", "bánh xe", "pin", "mạch", "kẹp"]):
                text_snippets.add(s)
        
        print("Relevant keywords found:", len(text_snippets))
        for t in list(text_snippets)[:30]:
            print("  *", t)
            
except Exception as e:
    print("Fetch error:", e)

