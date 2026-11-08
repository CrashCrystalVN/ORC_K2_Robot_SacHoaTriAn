import sys
import re
import json

sys.stdout.reconfigure(encoding="utf-8")

with open("canva_curl.html", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Canva encodes its design documents as JSON inside script tags.
# Let's search for JSON blocks with pages/slides.
# Let's look for all strings ending in \n or text objects.
matches = re.findall(r'\"(?:text|title|label|content)\":\s*\"([^\"]+)\"', text)
print(f"Total text fields: {len(matches)}")

# Filter and clean up
unique_lines = []
for m in matches:
    cleaned = m.encode('utf-8').decode('unicode_escape', errors='ignore')
    cleaned = cleaned.replace('\\n', '\n').strip()
    if cleaned and cleaned not in unique_lines and not cleaned.startswith('http') and len(cleaned) < 500:
        unique_lines.append(cleaned)

print("\n=== EXTRACTED CANVA TEXT CONTENT ===")
for i, line in enumerate(unique_lines):
    print(f"[{i+1}] {line}")

