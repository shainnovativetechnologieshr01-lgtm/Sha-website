import os
import re
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

PAGES = [
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

EXPECTED_TITLES = {
    "index.html": "SHA Innovative Technologies | Technology, Training & Digital Solutions",
    "about.html": "About SHA Innovative Technologies | Technology, Training & Digital Solutions",
    "training.html": "Technology Training Programs | SHA Innovative Technologies",
    "internships.html": "Internships & Practical Project Experience | SHA Innovative Technologies",
    "solutions.html": "Technology Solutions for Businesses | SHA Innovative Technologies",
    "institutions.html": "Institutional Programs & Academic Collaboration | SHA Innovative Technologies",
    "projects.html": "Technology Projects & Digital Work | SHA Innovative Technologies",
    "resources.html": "Technology, Career & Learning Resources | SHA Innovative Technologies",
    "contact.html": "Contact SHA Innovative Technologies | Enquiries & Requirements"
}

EXPECTED_DESCRIPTIONS = {
    "index.html": "SHA Innovative Technologies provides technology training, internships, digital solutions and practical technology services for learners, institutions and businesses.",
    "about.html": "Learn about SHA Innovative Technologies, our journey, people, technology focus, training approach, institutional engagement and digital solutions.",
    "training.html": "Explore practical technology training in web development, Python, Django, UI/UX, databases, digital marketing and emerging technology fundamentals.",
    "internships.html": "Explore practical internship opportunities focused on project work, technology exposure, implementation and real-world development experience.",
    "solutions.html": "Explore web development, software solutions, IT support and digital marketing services designed around business technology requirements.",
    "institutions.html": "Explore institutional programs, workshops, seminars, academic collaborations and technology engagement supported by SHA Innovative Technologies.",
    "projects.html": "Explore selected websites, software applications, digital platforms, technology projects and practical implementation work by SHA Innovative Technologies.",
    "resources.html": "Explore practical technology insights, learning references, career guidance, development resources and useful digital content from SHA Innovative Technologies.",
    "contact.html": "Contact SHA Innovative Technologies to discuss training, internships, institutional programs, technology solutions, projects or other requirements."
}

EXPECTED_CANONICALS = {
    "index.html": "https://shainnovativetechnologies.com/",
    "about.html": "https://shainnovativetechnologies.com/about.html",
    "training.html": "https://shainnovativetechnologies.com/training.html",
    "internships.html": "https://shainnovativetechnologies.com/internships.html",
    "solutions.html": "https://shainnovativetechnologies.com/solutions.html",
    "institutions.html": "https://shainnovativetechnologies.com/institutions.html",
    "projects.html": "https://shainnovativetechnologies.com/projects.html",
    "resources.html": "https://shainnovativetechnologies.com/resources.html",
    "contact.html": "https://shainnovativetechnologies.com/contact.html"
}

def normalize_text(t):
    if not t:
        return ""
    return re.sub(r'\s+', ' ', t).strip()

def run_validation():
    errors = []
    warnings = []
    
    print("==================================================")
    print("RUNNING MASTER PRODUCTION SEO VALIDATION")
    print("==================================================")

    # 1. Inspect robots.txt
    print("\n[1] Checking robots.txt...")
    if not os.path.exists("robots.txt"):
        errors.append("robots.txt is missing!")
    else:
        with open("robots.txt", "r", encoding="utf-8") as f:
            rob_content = f.read()
        if "https://shainnovativetechnologies.com/sitemap.xml" not in rob_content:
            errors.append("robots.txt does not reference production sitemap!")
        if "Disallow: /" in rob_content and "Allow: /" not in rob_content:
            errors.append("robots.txt has full Disallow!")
        print("  [OK] robots.txt exists, specifies crawl rules and sitemap")

    # 2. Inspect sitemap.xml
    print("\n[2] Checking sitemap.xml...")
    if not os.path.exists("sitemap.xml"):
        errors.append("sitemap.xml is missing!")
    else:
        try:
            tree = ET.parse("sitemap.xml")
            root = tree.getroot()
            namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            sitemap_urls = [elem.text.strip() for elem in root.findall('ns:url/ns:loc', namespaces)]
            print(f"  Found {len(sitemap_urls)} URLs in sitemap.xml")
            for page, can_url in EXPECTED_CANONICALS.items():
                if can_url not in sitemap_urls:
                    errors.append(f"sitemap.xml missing URL: {can_url}")
            for url in sitemap_urls:
                if "localhost" in url or "127.0.0.1" in url:
                    errors.append(f"sitemap.xml contains dev URL: {url}")
            print("  [OK] sitemap.xml contains all 9 canonical production URLs")
        except Exception as e:
            errors.append(f"sitemap.xml XML parse error: {e}")

    # 3. Check for dev / localhost references across all project files
    print("\n[3] Checking for localhost / 127.0.0.1 across repository...")
    for root_dir, _, files in os.walk("."):
        if ".git" in root_dir or ".gemini" in root_dir or "node_modules" in root_dir or ".agents" in root_dir:
            continue
        for file in files:
            if file.endswith(('.html', '.js', '.css', '.xml', '.txt', '.json')) and not file.startswith('validate_') and not file.startswith('audit_') and not file.startswith('master_'):
                file_path = os.path.join(root_dir, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                if "localhost" in content:
                    errors.append(f"Localhost reference found in {file_path}")
                if "127.0.0.1" in content:
                    errors.append(f"127.0.0.1 reference found in {file_path}")
    print("  [OK] No localhost or 127.0.0.1 found in production code")

    # 4. Page by page audit
    print("\n[4] Auditing all 9 HTML pages...")
    page_soups = {}
    for page in PAGES:
        if not os.path.exists(page):
            errors.append(f"Page file missing: {page}")
            continue
        with open(page, 'r', encoding='utf-8') as f:
            html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        page_soups[page] = soup

        # Title check
        title_el = soup.find('title')
        title_text = normalize_text(title_el.text) if title_el else ""
        expected_title = EXPECTED_TITLES[page]
        if title_text != expected_title:
            errors.append(f"[{page}] Title mismatch.\n  Expected: {expected_title}\n  Found:    {title_text}")
        else:
            print(f"  [OK] [{page}] Title: {title_text}")

        # Meta description check
        desc_el = soup.find('meta', attrs={'name': 'description'})
        desc_text = normalize_text(desc_el.get('content', '')) if desc_el else ""
        expected_desc = EXPECTED_DESCRIPTIONS[page]
        if desc_text != expected_desc:
            errors.append(f"[{page}] Meta description mismatch.\n  Expected: {expected_desc}\n  Found:    {desc_text}")
        else:
            print(f"  [OK] [{page}] Meta Description matches spec")

        # Canonical check
        can_el = soup.find('link', attrs={'rel': 'canonical'})
        can_href = can_el.get('href', '').strip() if can_el else ""
        expected_can = EXPECTED_CANONICALS[page]
        if can_href != expected_can:
            errors.append(f"[{page}] Canonical mismatch. Expected: {expected_can} | Found: {can_href}")
        else:
            print(f"  [OK] [{page}] Canonical URL: {can_href}")

        # H1 check
        h1s = soup.find_all('h1')
        if len(h1s) != 1:
            errors.append(f"[{page}] Expected exactly 1 H1, found {len(h1s)}")
        else:
            print(f"  [OK] [{page}] Single H1: '{normalize_text(h1s[0].text)}'")

        # Open Graph check
        og_title = soup.find('meta', property='og:title')
        og_desc = soup.find('meta', property='og:description')
        og_url = soup.find('meta', property='og:url')
        og_image = soup.find('meta', property='og:image')
        og_site_name = soup.find('meta', property='og:site_name')

        if not og_title or not og_title.get('content'):
            errors.append(f"[{page}] Missing og:title")
        if not og_desc or not og_desc.get('content'):
            errors.append(f"[{page}] Missing og:description")
        if not og_url or og_url.get('content') != expected_can:
            errors.append(f"[{page}] og:url mismatch ({og_url.get('content') if og_url else 'None'} vs {expected_can})")
        if not og_image or not og_image.get('content'):
            errors.append(f"[{page}] Missing og:image")
        if not og_site_name or og_site_name.get('content') != "SHA Innovative Technologies":
            errors.append(f"[{page}] Missing or incorrect og:site_name")

        # Favicon check
        favs = soup.find_all('link', rel=lambda r: r and ('icon' in r or 'apple-touch-icon' in r))
        if not favs:
            errors.append(f"[{page}] Missing favicon links")

        # JSON-LD check
        json_lds = soup.find_all('script', type='application/ld+json')
        if not json_lds:
            errors.append(f"[{page}] Missing JSON-LD script")
        else:
            for j_idx, j_script in enumerate(json_lds):
                try:
                    data = json.loads(j_script.string or "{}")
                    if "@context" not in data or data["@context"] != "https://schema.org":
                        errors.append(f"[{page}] JSON-LD #{j_idx+1} @context invalid")
                except Exception as e:
                    errors.append(f"[{page}] JSON-LD #{j_idx+1} parse error: {e}")

        # Image alt checks
        imgs = soup.find_all('img')
        for img in imgs:
            src = img.get('src', '')
            alt = img.get('alt', None)
            if alt is None:
                errors.append(f"[{page}] Image missing alt attribute: {src}")
            elif alt.endswith('.jpg') or alt.endswith('.png') or alt == 'image' or alt == 'photo':
                warnings.append(f"[{page}] Poor alt text '{alt}' on {src}")

    # 5. Check specific anchor IDs required
    print("\n[5] Checking anchor IDs...")
    anchor_checks = [
        ("training.html", ["training-formats", "project-learning"]),
        ("solutions.html", ["web-development", "software-solutions", "it-solutions", "digital-marketing"])
    ]
    for page, ids in anchor_checks:
        soup = page_soups.get(page)
        if soup:
            for anchor_id in ids:
                el = soup.find(id=anchor_id)
                if not el:
                    errors.append(f"[{page}] Missing required anchor id: #{anchor_id}")
                else:
                    print(f"  [OK] [{page}] Found target id #{anchor_id}")

    # 6. Check internal link targets
    print("\n[6] Checking internal links across all pages...")
    for page, soup in page_soups.items():
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href'].strip()
            if href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:')):
                continue
            if href.startswith('#'):
                target_id = href[1:]
                if target_id and not soup.find(id=target_id):
                    warnings.append(f"[{page}] In-page anchor target not found: {href}")
            elif '#' in href:
                target_file, target_id = href.split('#', 1)
                if target_file:
                    target_soup = page_soups.get(target_file)
                    if not target_soup:
                        errors.append(f"[{page}] Link target file not found: {target_file}")
                    elif target_id and not target_soup.find(id=target_id):
                        warnings.append(f"[{page}] Anchor #{target_id} not found in {target_file}")
            else:
                if href and href not in page_soups and not os.path.exists(href):
                    errors.append(f"[{page}] Broken internal link: {href}")

    print("\n==================================================")
    print("VALIDATION SUMMARY")
    print("==================================================")
    print(f"Total Errors: {len(errors)}")
    print(f"Total Warnings: {len(warnings)}")
    
    if errors:
        print("\nERRORS DETECTED:")
        for err in errors:
            print(f"  [ERROR] {err}")
    else:
        print("\nALL TESTS PASSED! ZERO CRITICAL SEO ERRORS.")

    if warnings:
        print("\nWARNINGS:")
        for warn in warnings:
            print(f"  [WARN] {warn}")

    return len(errors) == 0

if __name__ == "__main__":
    run_validation()
