import os
from bs4 import BeautifulSoup
import json

def audit_seo_full():
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

    print("=== FULL SEO AUDIT ACROSS ALL 9 PAGES ===")
    
    for page in pages:
        print(f"\n==================== {page} ====================")
        with open(page, 'r', encoding='utf-8') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')
        
        # 1. Title
        title = soup.find('title')
        print(f"Title: {title.text.strip() if title else 'NONE'}")

        # 2. Meta description
        m_desc = soup.find('meta', attrs={'name': 'description'})
        print(f"Meta Description: {m_desc['content'].strip() if m_desc else 'NONE'}")

        # 3. Canonical
        can = soup.find('link', attrs={'rel': 'canonical'})
        print(f"Canonical: {can['href'].strip() if can else 'NONE'}")

        # 4. Open Graph
        og_tags = {meta['property']: meta.get('content', '') for meta in soup.find_all('meta', attrs={'property': True}) if meta['property'].startswith('og:')}
        print("Open Graph:")
        for k, v in og_tags.items():
            print(f"  {k}: {v}")

        # 5. Twitter
        tw_tags = {meta['name']: meta.get('content', '') for meta in soup.find_all('meta', attrs={'name': True}) if meta['name'].startswith('twitter:')}
        print("Twitter:")
        for k, v in tw_tags.items():
            print(f"  {k}: {v}")

        # 6. JSON-LD
        json_scripts = soup.find_all('script', type="application/ld+json")
        print(f"JSON-LD blocks: {len(json_scripts)}")
        for i, js in enumerate(json_scripts):
            try:
                parsed = json.loads(js.string or "{}")
                print(f"  Block #{i+1} Type: {parsed.get('@type', parsed.get('@graph', 'Unknown'))}")
            except Exception as e:
                print(f"  Block #{i+1} ERROR: {e}")

if __name__ == "__main__":
    audit_seo_full()
