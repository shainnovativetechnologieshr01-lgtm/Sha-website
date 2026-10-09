# Design System — SHA Innovative Technologies

A comprehensive reference for design tokens, typography, UI components, spacing scales, and accessibility rules for the SHA Innovative Technologies web platform.

---

## 1. Color Palette & CSS Custom Properties

### Primary & Brand Colors
| Token | Variable | Value | Usage |
|---|---|---|---|
| **Primary Purple** | `--color-primary` | `#6D28D9` | Main brand color, primary buttons, active states |
| **Primary Dark** | `--color-primary-dark` | `#4C1D95` | Button hover states, deep brand accents |
| **Primary Light** | `--color-primary-light`| `#7C3AED` | Bright accent highlights |
| **Primary Subtle** | `--color-primary-subtle`| `#EDE9FE` | Soft lavender badges, icon containers |
| **Dark Corporate** | `--color-dark-purple` | `#16082B` | Footer background, deep contrasting cards |
| **Logo Tech Blue** | `--color-secondary` | `#2563EB` | Secondary brand accents, tech indicators |
| **Innovation Cyan**| `--color-accent` | `#00D4B2` | Tech badges, innovation highlights |
| **Accent Subtle** | `--color-accent-subtle` | `#E6FBF7` | Cyan badge background, feature highlights |

### Surface & Background Colors
| Token | Variable | Value | Usage |
|---|---|---|---|
| **Canvas Background** | `--color-bg` | `#FFFFFF` | Page canvas, pure white cards |
| **Secondary Lavender**| `--color-surface-lavender`| `#F7F5FE`| Alternating lavender section backgrounds |
| **Surface Soft** | `--color-surface` | `#F8F6FE` | Section surfaces |
| **Surface Hover** | `--color-surface-hover` | `#F1EDFD` | Nav item hover, interactive elements |
| **Border Default** | `--color-border` | `#E2E8F0` | Card borders, dividers, form borders |
| **Border Purple** | `--color-border-purple` | `#DDD6FE` | Lavender accent borders, active borders |
| **Border Focus** | `--color-border-focus` | `#6D28D9` | Brand purple focus rings |

### Text & Semantic Colors
| Token | Variable | Value | Usage |
|---|---|---|---|
| **Text Primary** | `--color-text-primary` | `#0F172A` | Primary headings & high-contrast emphasis |
| **Text Secondary** | `--color-text-secondary`| `#334155` | Standard paragraph body copy |
| **Text Muted** | `--color-text-muted` | `#64748B` | Captions, dates, helper hints |
| **Text Lavender** | `--color-text-lavender` | `#DDD6FE` | Subtitles on dark purple backgrounds |
| **Text White** | `--color-text-white` | `#FFFFFF` | Text on dark backgrounds and primary buttons |
| **Success** | `--color-success` | `#10B981` | Success alerts, confirmed badges |
| **Warning** | `--color-warning` | `#F59E0B` | Warning alerts, notice badges |
| **Error** | `--color-error` | `#EF4444` | Form validation errors, error alerts |
| **Info** | `--color-info` | `#0284C7` | Informational messages, notices |

---

## 2. Typography System

### Font Families
- **Primary Body Font**: `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`
- **Headings Font**: `Plus Jakarta Sans, Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`

### Modular Type Scale
| Element / Scale | Variable | Font Size (rem / px) | Weight | Line Height |
|---|---|---|---|---|
| **H1 (Hero)** | `--font-size-4xl` | `3.00rem` (48px) | 800 (ExtraBold) | 1.15 |
| **H2 (Sections)** | `--font-size-3xl` | `2.25rem` (36px) | 700 (Bold) | 1.25 |
| **H3 (Sub-sections)** | `--font-size-2xl` | `1.875rem` (30px) | 700 (Bold) | 1.25 |
| **H4 (Card Titles)** | `--font-size-xl` | `1.50rem` (24px) | 600 (SemiBold) | 1.30 |
| **H5 (Sub-headings)** | `--font-size-lg` | `1.25rem` (20px) | 600 (SemiBold) | 1.35 |
| **Body Lead** | `--font-size-md` | `1.125rem` (18px) | 400 (Regular) | 1.68 |
| **Body Standard** | `--font-size-base` | `1.00rem` (16px) | 400 (Regular) | 1.68 |
| **Small / UI Text** | `--font-size-sm` | `0.875rem` (14px) | 500 (Medium) | 1.50 |
| **Extra Small / Badges**| `--font-size-xs` | `0.75rem` (12px) | 600 (SemiBold) | 1.40 |

---

## 3. Spacing Scale

Built on a 4px modular grid:
- `--space-1`: `0.25rem` (4px)
- `--space-2`: `0.50rem` (8px)
- `--space-3`: `0.75rem` (12px)
- `--space-4`: `1.00rem` (16px)
- `--space-5`: `1.25rem` (20px)
- `--space-6`: `1.50rem` (24px)
- `--space-8`: `2.00rem` (32px)
- `--space-10`: `2.50rem` (40px)
- `--space-12`: `3.00rem` (48px)
- `--space-16`: `4.00rem` (64px)
- `--space-20`: `5.00rem` (80px)
- `--space-24`: `6.00rem` (96px)

---

## 4. Radii & Shadows

### Border Radii
- `--radius-xs`: `4px`
- `--radius-sm`: `6px`
- `--radius-md`: `8px`
- `--radius-lg`: `12px`
- `--radius-xl`: `16px`
- `--radius-2xl`: `24px`
- `--radius-full`: `9999px`

### Box Shadows
- `--shadow-xs`: `0 1px 2px 0 rgba(15, 23, 42, 0.05)`
- `--shadow-sm`: `0 1px 3px 0 rgba(15, 23, 42, 0.08), 0 1px 2px -1px rgba(15, 23, 42, 0.08)`
- `--shadow-md`: `0 4px 6px -1px rgba(15, 23, 42, 0.08), 0 2px 4px -2px rgba(15, 23, 42, 0.06)`
- `--shadow-lg`: `0 10px 15px -3px rgba(15, 23, 42, 0.08), 0 4px 6px -4px rgba(15, 23, 42, 0.04)`
- `--shadow-card-hover`: `0 16px 32px -4px rgba(10, 37, 64, 0.12), 0 6px 12px -4px rgba(10, 37, 64, 0.06)`

---

## 5. Responsive Breakpoint Matrix

| Breakpoint | Target Screen | Primary Layout Adjustments |
|---|---|---|
| **&ge; 1440px** | Large Desktop | Expanded container max-width (1320px), prominent headings |
| **1024px – 1279px** | Small Desktop / Laptops | Standard desktop menu, 4-column footer |
| **768px – 1023px** | Tablets / iPads | Mobile drawer navigation enabled, 2-column card grid, 2-column footer |
| **481px – 767px** | Large Mobile Phones | Single column card stack, single column footer, full-width CTA buttons |
| **320px – 480px** | Small & Standard Mobile | Streamlined logo, compact padding, 100vw drawer, touch-friendly 44px min targets |

---

## 6. Component Guidelines

### Buttons
- **Primary (`.btn-primary`)**: Solid tech blue, white text, subtle hover lift. Used for main CTA ("Enquire Now", "Enroll").
- **Secondary (`.btn-secondary`)**: Dark navy, white text. Used for alternative primary actions.
- **Outline (`.btn-outline-primary`, `.btn-outline-secondary`, `.btn-outline-white`)**: Transparent background with crisp 1px borders.
- **Sizes**: Small (`.btn-sm`), Standard (default), Large (`.btn-lg`).

### Cards
- **Standard (`.card`)**: 1px border (`#E2E8F0`), white background, 12px radius, padding 32px.
- **Interactive (`.card-interactive`)**: On hover, -4px vertical transform, elevated dual-layer shadow, border tint.

### Forms
- High contrast field borders with distinct focus rings (`--color-secondary` at 3px alpha glow).
- Clear inline error validation states (`.has-error`) with explicit helper message.

---

## 7. Accessibility (A11y) Rules
- Minimum color contrast ratio of 4.5:1 for all standard body copy against background.
- Skip-to-main-content landmark link on all pages.
- Focus rings visible on keyboard tab navigation (`:focus-visible`).
- Full keyboard support for mobile drawer and dropdowns (`Esc`, `ArrowDown`, `Enter`, `Space`).
- `prefers-reduced-motion` honored for all micro-animations.
