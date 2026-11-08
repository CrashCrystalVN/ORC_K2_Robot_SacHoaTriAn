import sys
import re

sys.stdout.reconfigure(encoding="utf-8")

with open("canva_curl.html", "rb") as f:
    raw_bytes = f.read()

# Decode as utf-8
text = raw_bytes.decode("utf-8", errors="ignore")

# Find all occurrences of "GA25" and surrounding text (150 chars before and after)
for m in re.finditer(r'GA25', text):
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 100)
    snippet = text[start:end]
    # Clean up non-printable
    snippet = "".join(c if c.isprintable() else " " for c in snippet)
    print("--- SNIPPET ---")
    print(snippet)

