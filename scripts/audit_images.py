import glob
import re

for html_file in sorted(glob.glob('*.html')):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
    print(f'=== {html_file} ===')
    for img in imgs:
        if 'logo' not in img and not img.startswith('data:'):
            print('  -', img)
