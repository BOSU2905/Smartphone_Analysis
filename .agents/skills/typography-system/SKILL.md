---
name: typography-system
description: >-
  Governs the three-tier open-source Google Fonts typography hierarchy (Manrope, IBM Plex Sans,
  IBM Plex Mono), font loading, type scale, tabular numerals, line length, and licensing compliance.
  Use whenever defining CSS typography tokens or reviewing text formatting.
---

# Typography System Skill

This skill governs font pairing, typographic scale, tabular alignment, and reading ergonomics for **"What Are We Really Paying For When We Buy a Smartphone?"**.

---

## 1. WHEN TO ACTIVATE

Activate this skill whenever:
- Configuring web font imports, `@font-face` rules, or CSS custom properties.
- Applying font families, font weights, letter spacing, or line heights to UI components.
- Formatting numerical data, currency figures, specifications (GB, mAh, Hz), or chart axes.
- Setting up responsive typography scales using CSS `clamp()`.
- Auditing font loading performance and layout shift (CLS).

---

## 2. APPROVED TYPOGRAPHY SYSTEM (GOOGLE FONTS ONLY)

To guarantee zero licensing liability and seamless web distribution, typography is strictly limited to three approved open-source Google Fonts:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          APPROVED TYPEFACES                                 │
├─────────────────┬────────────────────┬──────────────────────────────────────┤
│ Family          │ Category           │ Role & Scope                         │
├─────────────────┼────────────────────┼──────────────────────────────────────┤
│ Manrope         │ Geometric Grotesque│ Display Headlines, Prominent H1/H2   │
│ IBM Plex Sans   │ Neutral Grotesque  │ Long-Form Editorial Prose, UI Labels │
│ IBM Plex Mono   │ Technical Monospace│ Specs, Prices, Units, Charts, Stamps │
└─────────────────┴────────────────────┴──────────────────────────────────────┘
```

### Prohibited Typefaces
Strictly prohibit commercial typefaces (e.g., PP Neue Montreal, Helvetica Now, Söhne) and generic system fallbacks used as primary fonts without proper loading. Prohibit futuristic stencil or decorative sci-fi fonts.

---

## 3. DESIGN TOKENS & TYPE SCALE

```css
:root {
  /* Font Family Stacks */
  --font-display: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-body: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'IBM Plex Mono', 'SF Mono', Menlo, Consolas, monospace;

  /* Font Weights */
  --fw-regular: 400;
  --fw-medium: 500;
  --fw-semibold: 600;
  --fw-bold: 700;
  --fw-extrabold: 800;

  /* Fluid Responsive Type Scale */
  --text-hero: clamp(2.5rem, 6vw, 5.5rem);       /* 40px – 88px | Line Height: 1.05 | Tracking: -0.04em */
  --text-h1: clamp(2.0rem, 4vw, 3.5rem);         /* 32px – 56px | Line Height: 1.15 | Tracking: -0.03em */
  --text-h2: clamp(1.5rem, 2.5vw, 2.25rem);      /* 24px – 36px | Line Height: 1.25 | Tracking: -0.02em */
  --text-h3: clamp(1.125rem, 1.5vw, 1.5rem);     /* 18px – 24px | Line Height: 1.35 | Tracking: -0.01em */
  --text-body-lg: 1.125rem;                      /* 18px        | Line Height: 1.65 | Tracking: normal */
  --text-body: 1.0rem;                           /* 16px        | Line Height: 1.60 | Tracking: normal */
  --text-caption: 0.8125rem;                     /* 13px        | Line Height: 1.50 | Tracking: normal */
  --text-mono-md: 0.875rem;                      /* 14px        | Line Height: 1.40 | Tracking: 0.04em */
  --text-mono-sm: 0.75rem;                       /* 12px        | Line Height: 1.40 | Tracking: 0.06em */
}
```

---

## 4. MANDATORY TYPOGRAPHIC RULES

1. **Tabular Numeral Alignment:** All financial values, hardware specifications (RAM, Storage, mAh, Hz, MP), and chart tick marks must enforce:
   ```css
   font-variant-numeric: tabular-nums;
   font-feature-settings: 'tnum' on, 'zero' on;
   ```
   This prevents numbers from jumping or misaligning when values update or sort.
2. **Reading Ergonomics (Line Length):** Long-form body paragraphs must be constrained using:
   ```css
   max-width: 68ch;
   ```
   Line lengths beyond 75 characters induce severe reading fatigue.
3. **Tracking Calibration:**
   - Display headings (`Manrope` at $\ge 32\text{px}$) must use tight negative tracking (`letter-spacing: -0.02em` to `-0.04em`).
   - Technical labels and monospace elements (`IBM Plex Mono`) must use loose positive tracking (`letter-spacing: 0.04em` to `0.06em`) with `text-transform: uppercase`.
4. **Font Loading Hygiene:** Always include `font-display: swap;` in font definitions to prevent Invisible Text Flash (FOIT). Preconnect to Google Fonts domains (`fonts.googleapis.com` and `fonts.gstatic.com`).

---

## 5. QUALITY AUDIT CHECKLIST

Before approving any UI view or CSS stylesheet, verify:
- [ ] Are all headlines rendered in `Manrope` with negative tracking?
- [ ] Is long-form editorial copy rendered in `IBM Plex Sans` with line-height $\ge 1.6$?
- [ ] Are prices, specifications, coordinates, and units rendered in `IBM Plex Mono`?
- [ ] Are prices and specs configured with `font-variant-numeric: tabular-nums`?
- [ ] Is paragraph width clamped to a maximum of `68ch`?
- [ ] Are commercial, unverified, or decorative fonts completely absent?
- [ ] Does typography remain sharp and readable on both high-DPI and standard displays?

---

## 6. PROJECT CONTEXT & EXPLICIT LIMITATIONS

- **Context:** The typography system establishes the intellectual and aesthetic credibility of the website.
- **Limitations:** Do not load more than 5 combined font weights across all families to prevent font payload bloat.
