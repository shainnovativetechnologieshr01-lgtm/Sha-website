import os
import re
import json
from bs4 import BeautifulSoup

def master_audit():
    print("============================================================")
    print("MASTER AUDIT: SHA INNOVATIVE TECHNOLOGIES PRODUCTION SUITE")
    print("============================================================")

    pages = [
        "index.html",
        "about.html",
        "training.html",
        "internships.html",
        "solutions.html",
        "institutions.html",
        "projects.html",
        "resources.html",
        "contact.html"
    ]

    issues = []
    warnings = []
    page_anchors = {}

    # Step 1: Collect all page anchors and check basic syntax
    for page in pages:
        if not os.path.exists(page):
            issues.append(f"[CRITICAL] Missing page file: {page}")
            continue
        
        with open(page, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')
        
        # Collect all IDs
        ids = set(tag['id'] for tag in soup.find_all(attrs={"id": True}))
        page_anchors[page] = ids

    # Step 2: Audit each page in detail
    for page in pages:
        if page not in page_anchors:
            continue
            
        with open(page, 'r', encoding='utf-8', errors='ignore') as f:
            raw_html = f.read()

        soup = BeautifulSoup(raw_html, 'html.parser')
        print(f"\n--- Auditing: {page} ---")

        # 2.1 SEO: Title Tag
        title = soup.find('title')
        if not title or not title.text.strip():
            issues.append(f"[{page}] Missing or empty <title> tag.")
        else:
            print(f"  [Title] {title.text.strip()}")

        # 2.2 SEO: Meta Description
        meta_desc = soup.find('meta', attrs={"name": re.compile(r"^description$", re.I)})
        if not meta_desc or not meta_desc.get('content', '').strip():
            issues.append(f"[{page}] Missing or empty meta description.")
        else:
            print(f"  [Meta Desc] {meta_desc['content'][:60]}...")

        # 2.3 SEO: Canonical Tag
        canonical = soup.find('link', attrs={"rel": "canonical"})
        if not canonical or not canonical.get('href', '').strip():
            issues.append(f"[{page}] Missing canonical link.")
        else:
            can_href = canonical['href']
            if "localhost" in can_href or "127.0.0.1" in can_href:
                issues.append(f"[{page}] Canonical contains local dev URL: {can_href}")
            if not can_href.startswith("https://shainnovativetechnologies.com"):
                warnings.append(f"[{page}] Canonical domain unusual: {can_href}")

        # 2.4 Social: Open Graph
        og_title = soup.find('meta', property="og:title")
        og_desc = soup.find('meta', property="og:description")
        og_image = soup.find('meta', property="og:image")
        if not (og_title and og_desc and og_image):
            warnings.append(f"[{page}] Missing some Open Graph tags (title/desc/image).")

        # 2.5 Structured Data JSON-LD
        json_scripts = soup.find_all('script', type="application/ld+json")
        for idx, j_script in enumerate(json_scripts):
            try:
                data = json.loads(j_script.string or "{}")
            except Exception as e:
                issues.append(f"[{page}] Invalid JSON-LD block #{idx+1}: {e}")

        # 2.6 Favicons
        favicons = soup.find_all('link', rel=re.compile(r"icon", re.I))
        if not favicons:
            issues.append(f"[{page}] No favicon linked.")
        for fav in favicons:
            href = fav.get('href', '')
            clean_href = href.split('?')[0]
            if clean_href and not os.path.exists(clean_href):
                issues.append(f"[{page}] Favicon file not found: {clean_href}")

        # 2.7 Active Navbar Link check
        active_links = soup.select('.site-header .nav-link.active, .site-header .nav-link[aria-current="page"]')
        active_hrefs = [a.get('href', '') for a in active_links]
        expected_page = "index.html" if page == "index.html" else page
        
        has_correct_active = False
        for ah in active_hrefs:
            if ah == expected_page or (page == "index.html" and (ah == "/" or ah == "index.html")):
                has_correct_active = True
                break
        if not has_correct_active:
            warnings.append(f"[{page}] Navbar active link might be misconfigured. Active hrefs found: {active_hrefs}")

        # 2.8 Check all Image Sources (src)
        imgs = soup.find_all('img')
        for img in imgs:
            src = img.get('src', '')
            if not src:
                issues.append(f"[{page}] <img> tag missing src attribute.")
                continue
            clean_src = src.split('?')[0].split('#')[0]
            if not clean_src.startswith('http') and not clean_src.startswith('data:'):
                if not os.path.exists(clean_src):
                    issues.append(f"[{page}] Broken image path: {src}")
            # Alt attribute check
            if 'alt' not in img.attrs:
                issues.append(f"[{page}] Image missing alt attribute: {src}")

        # 2.9 Check all CSS / JS assets
        css_links = soup.find_all('link', rel="stylesheet")
        for cl in css_links:
            href = cl.get('href', '')
            clean_href = href.split('?')[0]
            if clean_href and not clean_href.startswith('http') and not os.path.exists(clean_href):
                issues.append(f"[{page}] Missing CSS stylesheet: {href}")

        js_scripts = soup.find_all('script', src=True)
        for js in js_scripts:
            src = js.get('src', '')
            clean_src = src.split('?')[0]
            if clean_src and not clean_src.startswith('http') and not os.path.exists(clean_src):
                issues.append(f"[{page}] Missing JS script: {src}")

        # 2.10 Check all Internal Href Links & Anchors
        a_tags = soup.find_all('a', href=True)
        for a in a_tags:
            href = a['href'].strip()
            if not href or href.startswith(('javascript:', 'mailto:', 'tel:', 'http://', 'https://', '#')):
                if href.startswith('#') and len(href) > 1:
                    target_id = href[1:]
                    if target_id not in page_anchors[page]:
                        issues.append(f"[{page}] Broken internal anchor #{target_id}")
                continue

            # Page + Anchor link (e.g. solutions.html#web-development)
            if '#' in href:
                target_page, target_id = href.split('#', 1)
                if target_page:
                    if target_page not in page_anchors:
                        issues.append(f"[{page}] Link to non-existent page: {target_page}")
                    elif target_id and target_id not in page_anchors[target_page]:
                        issues.append(f"[{page}] Broken anchor '{href}': #{target_id} does not exist on {target_page}")
            else:
                if href not in page_anchors and not href.endswith('.pdf') and not href.endswith('.png'):
                    issues.append(f"[{page}] Link to non-existent page: {href}")

        # 2.11 Dev Artifacts / Forbidden Strings check
        forbidden = [
            "localhost",
            "127.0.0.1",
            "lorem ipsum",
            "TODO",
            "FIXME",
            "test_user"
        ]
        for f_word in forbidden:
            if f_word in raw_html.lower():
                # Check if it's in comments or text
                matches = re.findall(rf'.{{0,30}}{re.escape(f_word)}.{{0,30}}', raw_html, re.I)
                for m in matches:
                    if "shainnovativetechnologies" not in m:
                        warnings.append(f"[{page}] Potential placeholder/dev text '{f_word}': ...{m.strip()}...")

    # Summary
    print("\n============================================================")
    print("MASTER AUDIT REPORT")
    print("============================================================")
    print(f"Total Pages Checked: {len(pages)}")
    print(f"Critical Issues Found: {len(issues)}")
    print(f"Warnings Found: {len(warnings)}")
    
    if issues:
        print("\n--- ISSUES ---")
        for i, issue in enumerate(issues, 1):
            print(f"{i:2d}. {issue}")
            
    if warnings:
        print("\n--- WARNINGS ---")
        for i, warn in enumerate(warnings, 1):
            print(f"{i:2d}. {warn}")

    if not issues:
        print("\n>>> MASTER AUDIT PASSED WITH 0 CRITICAL ISSUES! <<<")

if __name__ == "__main__":
    master_audit()
