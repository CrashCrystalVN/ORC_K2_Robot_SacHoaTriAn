import sys
import re
import json

sys.stdout.reconfigure(encoding="utf-8")

with open("canva_curl.html", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Look for patterns like "A":["text..."]
matches = re.findall(r'\"A\":\s*\[\s*\"([^\"]+)\"\s*\]', text)
print(f"Found {len(matches)} text items in Canva JSON:")

for i, m in enumerate(matches):
    m_clean = m.encode('utf-8').decode('unicode_escape', errors='ignore').replace('\\n', '\n').strip()
    if len(m_clean) > 0 and not m_clean.startswith("http"):
        print(f"--- [Slide item {i+1}] ---")
        print(m_clean)

