import re
import os
import sys

def validate_redesigned_contact_page():
    print("=== STARTING REDESIGNED CONTACT PAGE VALIDATION ===")
    
    with open('contact.html', 'r', encoding='utf-8') as f:
        html = f.read()

    errors = []
    warnings = []

    # 1. Check title and meta
    if "<title>Contact SHA Innovative Technologies | Enquiries &amp; Requirements</title>" not in html and "<title>Contact | SHA Innovative Technologies</title>" not in html:
        errors.append("Title tag mismatch or missing.")
    
    if 'name="description"' not in html:
        errors.append("Meta description missing.")

    # 2. Section 01: Hero (Split corporate composition)
    if "Let's Start a Conversation" not in html:
        errors.append("Hero H1 mismatch.")
    if "CONTACT SHA" not in html:
        errors.append("Hero eyebrow mismatch.")
    if "Start an Enquiry" not in html:
        errors.append("Hero Primary CTA mismatch.")
    if "Explore Solutions" not in html:
        errors.append("Hero Secondary CTA mismatch.")
    if "contact-comm-visual" not in html:
        errors.append("Communication visual motif missing.")

    # 3. Section 02: Full-Width Interactive Requirement Bar (6 options)
    reqs = [
        "Training",
        "Internship",
        "Institutional Program",
        "Technology Solution",
        "Project Requirement",
        "General Enquiry"
    ]
    for r in reqs:
        if f'data-req="{r}"' not in html:
            errors.append(f"Requirement option '{r}' missing from selector bar.")
        if f'<option value="{r}"' not in html:
            errors.append(f"Requirement dropdown option '{r}' missing from form.")

    # 4. Section 03: Enquiry Workspace (Two-Panel Layout)
    if 'id="enquiry-workspace"' not in html:
        errors.append("Enquiry workspace container ID missing.")
    if 'contact-workspace-context' not in html or 'contact-workspace-form-card' not in html:
        errors.append("Two-panel workspace structure missing.")

    required_inputs = ['autocomplete="name"', 'autocomplete="email"', 'autocomplete="tel"', 'autocomplete="organization"']
    for req_attr in required_inputs:
        if req_attr not in html:
            errors.append(f"Form input missing attribute: {req_attr}")

    if 'name="message"' not in html or 'placeholder="Briefly describe what you would like to discuss..."' not in html:
        errors.append("Message textarea configuration mismatch.")

    # 5. Section 04: Large Horizontal Contact Strip
    if 'contact-horizontal-strip' not in html:
        errors.append("Horizontal contact strip structure missing.")
    if "+91 93444 40310" not in html or "+91 85310 66697" not in html:
        errors.append("Verified phone numbers missing.")
    if "shainnovativetechnologieshr01@gmail.com" not in html:
        errors.append("Verified email missing.")
    if "Villianur, Puducherry – 605110" not in html:
        errors.append("Verified address missing.")

    # 5b. Section 05: Office Location & Google Maps Embed
    if 'class="contact-map-section"' not in html:
        errors.append("Google Maps section container missing.")
    if "FIND US" not in html:
        errors.append("Google Maps section eyebrow 'FIND US' missing.")
    if "Visit SHA Innovative Technologies" not in html:
        errors.append("Google Maps section heading 'Visit SHA Innovative Technologies' missing.")
    if "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3710.6415164176624!2d79.75602797482303!3d11.919127888307859!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a5361faa8d638c3%3A0xb1b4098e907d1b26!2sSHA%20Innovative%20Technologies!5e1!3m2!1sen!2sin!4v1791525844304!5m2!1sen!2sin" not in html:
        errors.append("Google Maps iframe embed source mismatch.")
    if 'title="SHA Innovative Technologies location on Google Maps"' not in html:
        errors.append("Accessible iframe title missing.")
    if 'Get Directions' not in html:
        errors.append("Get Directions CTA missing.")

    # 6. Section 06: Vertical Response Flow (What Happens After You Contact Us?)
    steps = ["ENQUIRY RECEIVED", "REQUIREMENT REVIEW", "DISCUSSION", "NEXT STEP"]
    for s in steps:
        if s not in html:
            errors.append(f"Step '{s}' missing from Response Flow.")
    if "contact-flow-spine" not in html:
        errors.append("Vertical spine line motif missing from Response Flow.")

    # 7. Section 06: Split 2-Column FAQ (7 exact questions)
    faq_questions = [
        "What can I contact SHA about?",
        "Can I discuss a custom technology requirement?",
        "Can institutions contact SHA?",
        "Can I enquire about internships?",
        "Can I discuss an existing website or application?",
        "How should I describe my requirement?",
        "How can I start a project discussion?"
    ]
    for q in faq_questions:
        if q not in html:
            errors.append(f"FAQ Question '{q}' missing.")

    if 'contact-split-faq-sidebar' not in html:
        errors.append("Split 2-column FAQ layout structure missing.")

    # Check that all FAQ triggers are aria-expanded="false" by default
    exp_trues = re.findall(r'class="contact-faq-trigger"[^>]*aria-expanded="true"', html)
    if exp_trues:
        errors.append("FAQ items have aria-expanded='true' by default. Must be false.")

    # 8. Section 07: Final Connection CTA
    if "READY TO CONNECT?" not in html:
        errors.append("Final CTA Eyebrow mismatch.")
    if "Let's Discuss" not in html:
        errors.append("Final CTA H2 mismatch.")
    if "SEND AN ENQUIRY" not in html:
        errors.append("Final CTA Primary CTA mismatch.")
    if "VIEW PROJECTS" not in html:
        errors.append("Final CTA Secondary CTA mismatch.")

    # 9. Verify Asset Paths
    asset_matches = re.findall(r'(?:src|href)="([^"#:]+?\.(?:png|jpg|jpeg|webp|svg|css|js))"', html)
    for asset in set(asset_matches):
        if not os.path.exists(asset):
            errors.append(f"Referenced asset does not exist: {asset}")

    # 10. Check Locked files
    locked_files = [
        'index.html', 'about.html', 'training.html', 'internships.html',
        'solutions.html', 'institutions.html', 'projects.html', 'resources.html'
    ]
    for lf in locked_files:
        if not os.path.exists(lf):
            errors.append(f"Locked file missing: {lf}")

    print("\n--- RESULTS ---")
    if errors:
        print(f"FAILED with {len(errors)} error(s):")
        for e in errors:
            print(f"  [ERROR] {e}")
        sys.exit(1)
    else:
        print("ALL VERIFICATIONS PASSED PERFECTLY!")
        if warnings:
            for w in warnings:
                print(f"  [WARN] {w}")

if __name__ == "__main__":
    validate_redesigned_contact_page()
