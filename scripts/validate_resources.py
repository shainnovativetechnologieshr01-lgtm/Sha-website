import re
import os

with open('resources.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Validate images
imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
print(f"Total images found in resources.html: {len(imgs)}")
for i, img in enumerate(imgs, 1):
    if img.startswith('data:'):
        print(f"[{i:02d}] OK Data URI | {img[:35]}...")
    elif os.path.exists(img):
        print(f"[{i:02d}] OK File Exists | {img}")
    else:
        print(f"[{i:02d}] ERROR Missing | {img}")
        raise FileNotFoundError(f"Missing image: {img}")

# 2. Validate FAQ IDs and ARIA attributes
for idx in range(1, 7):
    assert f'id="res-faq-trig-{idx}"' in html, f"Missing trig {idx}"
    assert f'id="res-faq-ans-{idx}"' in html, f"Missing ans {idx}"
    assert f'aria-controls="res-faq-ans-{idx}"' in html, f"Missing aria-controls {idx}"
    assert f'aria-labelledby="res-faq-trig-{idx}"' in html, f"Missing aria-labelledby {idx}"
print("All 6 Resources FAQ items verified with proper ARIA accessibility!")

# 3. Validate Categories
cats = ['all', 'technology', 'career', 'development', 'digital']
for c in cats:
    assert f'data-category="{c}"' in html, f"Missing category {c}"
print("All resource categories verified!")

# 4. Check Headings & Key Sections
assert 'Knowledge for Technology, Learning &amp; Digital Growth' in html, "Hero H1 missing"
assert 'Featured Resource' in html, "Featured H2 missing"
assert 'Explore the Knowledge Library' in html, "Library H2 missing"
assert 'Explore by Your Goal' in html, "Paths H2 missing"
assert 'Practical Technology Knowledge' in html, "Topics H2 missing"
assert 'Questions About Our Knowledge Resources' in html, "FAQ H2 missing"
assert 'Keep Learning.' in html, "Final CTA missing"

print("\n>>> ALL VALIDATION CHECKS PASSED FOR RESOURCES.HTML! <<<")
