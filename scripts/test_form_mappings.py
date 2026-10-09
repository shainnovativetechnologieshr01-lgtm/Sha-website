import urllib.request
import json

ENDPOINT_URL = "https://script.google.com/macros/s/AKfycbxjQnFW5kRkosKcmHiybNkFmllvlM9s1a-17sBmcut6AF19c1wBWP4UZ06BmFMDmQ-xMA/exec"

def send_payload(payload):
    data_bytes = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        ENDPOINT_URL,
        data=data_bytes,
        headers={
            'Content-Type': 'text/plain;charset=utf-8',
            'User-Agent': 'Mozilla/5.0'
        },
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        res_body = response.read().decode('utf-8')
        return json.loads(res_body)

test_scenarios = [
    # Contact page Training submission
    {
        "type": "training",
        "name": "Integration Test - Contact Training",
        "email": "test.contact.training@example.com",
        "phone": "+91 93444 40310",
        "course": "Full Stack Training - Pondicherry University",
        "learning_mode": "Classroom",
        "message": "Testing Contact Page Training option submission."
    },
    # Contact page Internship submission
    {
        "type": "internship",
        "name": "Integration Test - Contact Internship",
        "email": "test.contact.internship@example.com",
        "phone": "+91 93444 40310",
        "college": "Achariya College of Engineering",
        "department": "Computer Science",
        "domain": "Web Development",
        "duration": "1 Month",
        "message": "Testing Contact Page Internship option submission."
    },
    # Contact page Project Requirement submission
    {
        "type": "project",
        "name": "Integration Test - Contact Project",
        "email": "test.contact.project@example.com",
        "phone": "+91 93444 40310",
        "project_title": "Project Requirement (Puducherry Retailer)",
        "technology": "Web App",
        "project_type": "Custom Software",
        "budget": "Standard",
        "deadline": "Flexible",
        "requirements": "Testing Contact Page Project option submission."
    },
    # Contact page General / Institution submission
    {
        "type": "contact",
        "name": "Integration Test - Contact General",
        "email": "test.contact.general@example.com",
        "phone": "+91 93444 40310",
        "subject": "Institutional Program - Christ College",
        "message": "Testing Contact Page Institutional/General enquiry submission."
    },
    # Index page Home submission
    {
        "type": "project",
        "name": "Integration Test - Home Web Dev",
        "email": "test.home.webdev@example.com",
        "phone": "+91 93444 40310",
        "project_title": "Web Development",
        "technology": "",
        "project_type": "Web Development",
        "budget": "",
        "deadline": "",
        "requirements": "Testing Home page consultation form submission."
    }
]

print("=== TESTING END-TO-END PAYLOAD MAPPINGS ===")
for sc in test_scenarios:
    name = sc['name']
    t = sc['type']
    print(f"\nSubmitting: {name} (type: '{t}')...")
    res = send_payload(sc)
    print(f"  Result: {res}")
