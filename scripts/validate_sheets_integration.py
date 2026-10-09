import subprocess
import json
import urllib.request

ENDPOINT_URL = "https://script.google.com/macros/s/AKfycbxjQnFW5kRkosKcmHiybNkFmllvlM9s1a-17sBmcut6AF19c1wBWP4UZ06BmFMDmQ-xMA/exec"

def run_tests():
    print("==================================================")
    print("VALIDATING GOOGLE SHEETS & APPS SCRIPT INTEGRATION")
    print("==================================================")

    # 1. Check js/forms.js config
    with open("js/forms.js", "r", encoding="utf-8") as f:
        forms_js = f.read()

    assert ENDPOINT_URL in forms_js, "Endpoint URL missing in js/forms.js"
    assert "isConfigured: true" in forms_js, "isConfigured is not true in js/forms.js"
    assert "buildPayload" in forms_js, "buildPayload helper missing in js/forms.js"
    print("[PASS] js/forms.js configuration & architecture verified")

    # 2. Check HTML forms
    with open("contact.html", "r", encoding="utf-8") as f:
        contact_html = f.read()
    assert 'id="contact-enquiry-form"' in contact_html, "contact-enquiry-form ID missing"
    assert 'data-validate-form' in contact_html, "data-validate-form attribute missing in contact.html"
    print("[PASS] contact.html form structure verified")

    with open("index.html", "r", encoding="utf-8") as f:
        index_html = f.read()
    assert 'data-validate-form' in index_html, "data-validate-form attribute missing in index.html"
    print("[PASS] index.html form structure verified")

    # 3. Test Live Submission for All 4 Types
    print("\n[3] Testing live Apps Script submission across all 4 types...")
    test_cases = [
        {
            "type": "contact",
            "name": "QA Verification Contact",
            "email": "qa.contact@example.com",
            "phone": "+91 93444 40310",
            "subject": "QA Test Subject",
            "message": "QA Contact test message."
        },
        {
            "type": "training",
            "name": "QA Verification Training",
            "email": "qa.training@example.com",
            "phone": "+91 93444 40310",
            "course": "Full Stack Web Development",
            "learning_mode": "Classroom",
            "message": "QA Training test message."
        },
        {
            "type": "internship",
            "name": "QA Verification Internship",
            "email": "qa.internship@example.com",
            "phone": "+91 93444 40310",
            "college": "Pondicherry University",
            "department": "Computer Science",
            "domain": "Web Development",
            "duration": "1 Month",
            "message": "QA Internship test message."
        },
        {
            "type": "project",
            "name": "QA Verification Project",
            "email": "qa.project@example.com",
            "phone": "+91 93444 40310",
            "project_title": "Enterprise Portal Build",
            "technology": "Python, Django",
            "project_type": "Custom Software",
            "budget": "Standard",
            "deadline": "2 Months",
            "requirements": "QA Project test message."
        }
    ]

    for tc in test_cases:
        t = tc["type"]
        data_bytes = json.dumps(tc).encode("utf-8")
        req = urllib.request.Request(
            ENDPOINT_URL,
            data=data_bytes,
            headers={"Content-Type": "text/plain;charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8")
            res_json = json.loads(body)
            assert res_json.get("success") is True, f"Failed for type {t}: {body}"
            print(f"  [OK] Type '{t}' -> Confirmed Enquiry ID: {res_json.get('enquiry_id')}")

    print("\nALL INTEGRATION TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
