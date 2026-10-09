import urllib.request
import urllib.parse
import json
import ssl

ENDPOINT_URL = "https://script.google.com/macros/s/AKfycbxjQnFW5kRkosKcmHiybNkFmllvlM9s1a-17sBmcut6AF19c1wBWP4UZ06BmFMDmQ-xMA/exec"

def test_endpoint():
    print("=== TESTING GOOGLE APPS SCRIPT ENDPOINT ===")
    
    # Test GET
    print("\n[1] Testing GET request...")
    try:
        req = urllib.request.Request(ENDPOINT_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8')
            print(f"GET Status: {response.status}")
            print(f"GET Response: {content[:300]}")
    except Exception as e:
        print(f"GET Error: {e}")

    # Test POST with contact payload
    print("\n[2] Testing POST request with JSON (contact payload)...")
    payload = {
        "type": "contact",
        "name": "Audit Test Lead",
        "email": "audit.test@example.com",
        "phone": "+91 93444 40310",
        "subject": "General Enquiry",
        "message": "Automated verification probe for safe sheets integration."
    }
    
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
            print(f"POST Status: {response.status}")
            print(f"POST Response URL: {response.geturl()}")
            print(f"POST Response Body: {res_body}")
            try:
                parsed = json.loads(res_body)
                print(f"POST Parsed JSON: {parsed}")
            except Exception:
                print("Could not parse response as JSON")
    except Exception as e:
        print(f"POST Error: {e}")

if __name__ == "__main__":
    test_endpoint()
