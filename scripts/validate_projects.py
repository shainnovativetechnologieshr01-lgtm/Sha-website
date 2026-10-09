import re
import os

with open('projects.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Validate images
imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
print(f"Total images found in projects.html: {len(imgs)}")
for i, img in enumerate(imgs, 1):
    if img.startswith('data:'):
        print(f"[{i:02d}] OK Data URI | {img[:35]}...")
    elif os.path.exists(img):
        print(f"[{i:02d}] OK File Exists | {img}")
    else:
        print(f"[{i:02d}] ERROR Missing | {img}")
        raise FileNotFoundError(f"Missing image: {img}")

# 2. Validate FAQ IDs and ARIA attributes
for idx in range(1, 9):
    assert f'id="proj-faq-trig-{idx}"' in html, f"Missing trig {idx}"
    assert f'id="proj-faq-ans-{idx}"' in html, f"Missing ans {idx}"
    assert f'aria-controls="proj-faq-ans-{idx}"' in html, f"Missing aria-controls {idx}"
    assert f'aria-labelledby="proj-faq-trig-{idx}"' in html, f"Missing aria-labelledby {idx}"
print("All 8 Project FAQ items verified with proper ARIA accessibility!")

# 3. Validate Featured Client Projects
assert 'https://msgroups-travels-puducherry.com/' in html, "Missing MS Groups Travels live link"
assert 'MS Groups Travels' in html, "Missing MS Groups Travels"
assert 'https://sai-shakthi-travels.vercel.app/' in html, "Missing Sai Shakthi Travels live link"
assert 'Sai Shakthi Travels' in html, "Missing Sai Shakthi Travels"
print("Featured Client Projects (MS Groups Travels & Sai Shakthi Travels) verified!")

# 4. Validate Categories
cats = ['all', 'web', 'digital', 'ui-ux']
for c in cats:
    assert f'data-category="{c}"' in html, f"Missing category {c}"
print("All project categories verified!")

# 5. Check Headings & Methodology
assert 'Work That Demonstrates What We Build' in html, "Hero H1 missing"
assert 'Real Projects. Practical Implementation.' in html, "Featured clients H2 missing"
assert 'Technology, Digital &amp; Creative Work' in html, "Selected work H2 missing"
assert 'From Requirement to Working Solution' in html, "Methodology H2 missing"
assert 'Built With Practical Implementation in Mind' in html, "Principles H2 missing"
assert "Let's Build Something" in html, "Final CTA missing"

print("\n>>> ALL VALIDATION CHECKS PASSED FOR PROJECTS.HTML! <<<")
