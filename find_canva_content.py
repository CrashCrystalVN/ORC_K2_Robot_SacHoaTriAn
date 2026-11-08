import sys
import re

sys.stdout.reconfigure(encoding="utf-8")

with open("canva_curl.html", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Look for all string literals in JS that have Vietnamese or assembly instructions
# Find tokens like "..."
strings = re.findall(r'\"([^\"]{3,200})\"', text)
seen = set()

print(f"Total raw strings: {len(strings)}")
print("\n=== TOÀN BỘ NỘI DUNG TỪNG BƯỚC / CHI TIẾT TRONG CANVA ===")
for s in strings:
    # decode unicode escape if any
    try:
        decoded = s.encode('utf-8').decode('unicode_escape', errors='ignore')
    except Exception:
        decoded = s
    decoded = decoded.replace('\\n', '\n').strip()
    
    # Check if it has Vietnamese characters or assembly instructions
    if re.search(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđĐ]', decoded):
        if decoded not in seen and len(decoded) > 3 and not decoded.startswith("http"):
            seen.add(decoded)
            print(f"---> {decoded}")

