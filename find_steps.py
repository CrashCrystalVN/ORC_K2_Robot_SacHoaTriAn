import sys
import re
import json

sys.stdout.reconfigure(encoding="utf-8")

with open("canva_curl.html", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's search for "slide" or "page" or "#10" or page indices
# In Canva JSON, pages often have ids or titles.
pages = re.findall(r'\"pageIndex\":\s*(\d+)', text)
print(f"Page indices found: {set(pages)}")

# Let's find sections or steps:
steps = re.findall(r'(\d+\.\s*[^\n\"<]{4,80})', text)
for s in set(steps):
    print("Step:", s)

