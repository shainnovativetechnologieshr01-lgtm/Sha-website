import os
from bs4 import BeautifulSoup

with open('internships.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
imgs = soup.find_all('img')

print(f"Found {len(imgs)} images in internships.html\n")
all_valid = True
for idx, img in enumerate(imgs, start=1):
    src = img.get('src', '')
    alt = img.get('alt', '')
    exists = os.path.exists(src) if not src.startswith(('http://', 'https://')) else False
    status = "OK" if exists else "MISSING"
    if not exists:
        all_valid = False
    print(f"[{idx:02d}] {status:7} | src: {src:65} | alt: {alt[:40]}")

print(f"\nFinal Result: {'ALL IMAGES VERIFIED LOCALLY' if all_valid else 'ERRORS FOUND'}")
