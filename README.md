# SHA Innovative Technologies — Website Redesign

A modern, high-performance static website for **SHA Innovative Technologies**, positioning the company as a premier **Technology + Training + Digital Solutions** enterprise.

---

## 1. Project Overview

- **Company**: SHA Innovative Technologies
- **Headquarters**: 5, Villiyanur Main Road, Taluk, Sulthanpet, Villianur, Puducherry – 605110
- **Founded**: June 25, 2025
- **Positioning**: Technology & Business Solutions + Education & Career Development
- **Architecture**: Static Web Architecture (Zero framework overhead)
- **Target Deployment Platform**: Cloudflare Pages / Static CDN

---

## 2. Technology Stack

- **HTML5**: Semantic markup, Open Graph metadata, JSON-LD Schema structured data.
- **CSS3 (Vanilla)**: Centralized design tokens via CSS custom properties, modular stylesheets, zero external CSS dependencies.
- **JavaScript (Vanilla ES6+)**: Lightweight, accessible interactive components, zero frontend frameworks.
- **Typography**: Inter & Plus Jakarta Sans via Google Fonts.

---

## 3. Directory Structure

```text
/
├── index.html                  # Complete corporate Home page (15 structured sections)
├── css/
│   ├── style.css               # Design tokens, CSS variables, typography & reset
│   ├── components.css          # Reusable UI components (Navbar, buttons, cards, forms, FAQ, footer)
│   └── responsive.css          # Responsive breakpoint overrides (320px to 1440px+)
├── js/
│   ├── main.js                 # Global application lifecycle, auto-year & FAQ accordion
│   ├── navbar.js               # Accessible sticky navigation, mobile drawer & dropdowns
│   ├── animations.js           # Lightweight scroll reveal (prefers-reduced-motion aware)
│   └── forms.js                # Form validation & Google Apps Script pipeline
├── assets/
│   ├── images/                 # Production image assets
│   ├── icons/                  # Scalable SVG icons
│   ├── logos/                  # Brand assets & logos
│   └── certificates/           # Sample certification/recognition assets
├── README.md                   # Technical setup, architecture & deployment guide
├── DESIGN-SYSTEM.md            # Comprehensive design tokens & UI guidelines
└── CONTENT-PLAN.md             # Complete multi-page content strategy & status roadmap
```

---

## 4. Current Implementation Status

- **Design System & Tokens**: `[COMPLETED]` — CSS variables for colors, typography, spacing, shadows, radii, and responsive breakpoints are fully centralized.
- **Navigation & Header**: `[COMPLETED]` — Accessible sticky header with desktop dropdowns (Training, Solutions, Resources), mobile hamburger drawer, and touch-friendly controls.
- **Home Page (`index.html`)**: `[COMPLETED]` — Full 15-section corporate Home page balancing Education & Career and Technology Solutions without unverified claims.
- **Global Footer**: `[COMPLETED]` — 4-column responsive footer with verified contact numbers, address in Puducherry, verified email, and social links.
- **Form Architecture**: `[COMPLETED]` — Client validation and submission pipeline prepared for Google Apps Script.
- **Inner Pages (`about.html`, `training.html`, etc.)**: `[FUTURE]` — Page blueprints established in `CONTENT-PLAN.md`, scheduled for Step 3+.

---

## 5. How to Run Locally

### Option A: Python Built-in Server (Recommended)
```bash
python -m http.server 8000
```
Open your browser at `http://localhost:8000`.

### Option B: Node static server
```bash
npx serve .
```

### Option C: VS Code Live Server
Right-click `index.html` and select **"Open with Live Server"**.

---

## 6. How to Deploy to Cloudflare Pages

1. **Push to GitHub / GitLab repository**:
   ```bash
   git init
   git add .
   git commit -m "Step 2: Complete Home Page implementation"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```
2. **Log into Cloudflare Dashboard**:
   - Navigate to **Workers & Pages** > **Create application** > **Pages** > **Connect to Git**.
3. **Configure Build Settings**:
   - **Framework preset**: None
   - **Build command**: *(Leave blank)*
   - **Build output directory**: `/` (Root directory)
4. **Deploy**:
   - Click **Save and Deploy**. Cloudflare Pages will serve your ultra-fast static site globally with automatic HTTPS, Brotli compression, and edge caching.
