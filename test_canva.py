import re, sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('canva_curl.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's find the titles of pages / slides
# Look for slide/page blocks
# In Canva, pages are often in a list
# Let's search around "Encoder trái - E1"
idx = text.find("Encoder trái - E1")
start = max(0, idx - 4000)
end = min(len(text), idx + 4000)
snippet = text[start:end]

for line in snippet.split('\n'):
    if any(k in line for k in ['title', 'text', 'Động cơ', 'Encoder', 'M1', 'M2', 'E1', 'E2', 'slide', 'page']):
        print(line[:120])
