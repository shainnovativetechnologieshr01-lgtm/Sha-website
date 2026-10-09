import os
from bs4 import BeautifulSoup

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

print("=== ALL HTML FORMS AUDIT ===")
total_forms = 0

for hf in sorted(html_files):
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    forms = soup.find_all('form')
    if forms:
        total_forms += len(forms)
        print(f"\n==================================================")
        print(f"File: {hf} (Found {len(forms)} form(s))")
        print(f"==================================================")
        for i, form in enumerate(forms):
            form_id = form.get('id', 'No ID')
            form_class = " ".join(form.get('class', []))
            form_action = form.get('action', 'No action')
            form_method = form.get('method', 'No method')
            form_data_attrs = {k: v for k, v in form.attrs.items() if k.startswith('data-')}
            print(f"Form #{i+1}: ID='{form_id}', Class='{form_class}', Action='{form_action}', Method='{form_method}', DataAttrs={form_data_attrs}")
            
            inputs = form.find_all(['input', 'select', 'textarea', 'button'])
            print("  Fields & Controls:")
            for inp in inputs:
                tag = inp.name
                inp_type = inp.get('type', tag)
                inp_name = inp.get('name', 'No name')
                inp_id = inp.get('id', 'No ID')
                inp_req = '[REQUIRED]' if inp.has_attr('required') else '[OPTIONAL]'
                placeholder = inp.get('placeholder', '')
                print(f"    - <{tag}> type='{inp_type}' name='{inp_name}' id='{inp_id}' {inp_req} placeholder='{placeholder}'")
    else:
        print(f"File: {hf} -> 0 forms")

print(f"\nTotal forms discovered: {total_forms}")
