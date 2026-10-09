import os
from bs4 import BeautifulSoup

with open('institutions.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
imgs = soup.find_all('img')

print(f"Found {len(imgs)} images in institutions.html\n")
all_valid = True
for idx, img in enumerate(imgs, start=1):
    src = img.get('src', '')
    alt = img.get('alt', '')
    if src.startswith('data:'):
        exists = True
    elif src.startswith(('http://', 'https://')):
        exists = False
    else:
        exists = os.path.exists(src)
    status = "OK" if exists else "MISSING"
    if not exists:
        all_valid = False
    print(f"[{idx:02d}] {status:7} | src: {src[:60]:60} | alt: {alt[:40]}")

print(f"\nFinal Result: {'ALL IMAGES VERIFIED LOCALLY' if all_valid else 'ERRORS FOUND'}")
