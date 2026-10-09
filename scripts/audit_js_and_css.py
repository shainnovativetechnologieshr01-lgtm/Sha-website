import os
import re

def audit_js_and_css():
    print("=== AUDITING JAVASCRIPT & CSS ARCHITECTURE ===")
    
    js_files = ["js/animations.js", "js/forms.js", "js/main.js", "js/navbar.js"]
    for jf in js_files:
        if not os.path.exists(jf):
            print(f"[ERROR] Missing {jf}")
            continue
        with open(jf, 'r', encoding='utf-8') as f:
            code = f.read()
        print(f"  [OK] {jf:18s}: {len(code)} bytes, {len(code.splitlines())} lines")

    css_files = ["css/style.css", "css/components.css", "css/responsive.css"]
    for cf in css_files:
        if not os.path.exists(cf):
            print(f"[ERROR] Missing {cf}")
            continue
        with open(cf, 'r', encoding='utf-8') as f:
            css = f.read()
        print(f"  [OK] {cf:18s}: {len(css)} bytes, {len(css.splitlines())} lines")

    # Check for any accidental 127.0.0.1 or localhost in js/css
    for folder in ['js', 'css']:
        for fname in os.listdir(folder):
            fpath = os.path.join(folder, fname)
            if os.path.isfile(fpath):
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    txt = f.read()
                if "127.0.0.1" in txt or "localhost" in txt:
                    print(f"[WARNING] Localhost reference found in {fpath}")

    print("=== JS & CSS INTEGRITY AUDIT COMPLETE ===")

if __name__ == "__main__":
    audit_js_and_css()
