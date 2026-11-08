import sys
import re

sys.stdout.reconfigure(encoding="utf-8")

with open("canva_curl.html", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Find all blocks of text
# Canva has JSON structures with text runs
pattern = r'\"text\":\"([^\"]+)\"'
matches = re.findall(pattern, text)

print(f"Total 'text' attributes: {len(matches)}")
for i, m in enumerate(matches):
    m_clean = m.encode('utf-8').decode('unicode_escape', errors='ignore').replace('\\n', '\n').strip()
    if any(c in m_clean for c in "áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđĐ"):
        print(f"[{i}] {m_clean}")

