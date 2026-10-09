import urllib.request
import json

ENDPOINT_URL = "https://script.google.com/macros/s/AKfycbxjQnFW5kRkosKcmHiybNkFmllvlM9s1a-17sBmcut6AF19c1wBWP4UZ06BmFMDmQ-xMA/exec"

def send_probe(payload):
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
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            res_body = response.read().decode('utf-8')
            parsed = json.loads(res_body)
            return True, parsed
    except Exception as e:
        return False, str(e)

print("=== TESTING ALL 4 TYPES ===")

types_to_test = [
    {
        "type": "contact",
        "name": "Audit Test Contact",
        "email": "audit.contact@example.com",
        "phone": "+91 93444 40310",
        "subject": "General Enquiry",
        "message": "Automated contact type verification probe."
    },
    {
        "type": "training",
        "name": "Audit Test Training",
        "email": "audit.training@example.com",
        "phone": "+91 93444 40310",
        "course": "Full Stack Web Development",
        "learning_mode": "Offline Classroom",
        "message": "Automated training type verification probe."
    },
    {
        "type": "internship",
        "name": "Audit Test Internship",
        "email": "audit.internship@example.com",
        "phone": "+91 93444 40310",
        "college": "Pondicherry Engineering College",
        "department": "Computer Science",
        "domain": "Web Engineering",
        "duration": "1 Month",
        "message": "Automated internship type verification probe."
    },
    {
        "type": "project",
        "name": "Audit Test Project",
        "email": "audit.project@example.com",
        "phone": "+91 93444 40310",
        "project_title": "Enterprise Web Portal",
        "technology": "Python, Django, PostgreSQL",
        "project_type": "Custom Software",
        "budget": "Standard",
        "deadline": "2 Months",
        "requirements": "Automated project type verification probe."
    }
]

for t in types_to_test:
    t_name = t["type"]
    print(f"\nProbing type: '{t_name}'...")
    ok, res = send_probe(t)
    if ok:
        print(f"  [SUCCESS] Type '{t_name}' -> Response: {res}")
    else:
        print(f"  [FAILED] Type '{t_name}' -> Error: {res}")
