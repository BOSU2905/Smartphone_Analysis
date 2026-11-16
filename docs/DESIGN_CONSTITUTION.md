# DESIGN CONSTITUTION

> **PRODUCT IDENTITY:** Experimental Technical Editorial  
> **DESIGN REFERENCE:** Inspired by the visual restraint, industrial precision, and technical hierarchy of `zrk.technology` (strictly non-military)  
> **CORE MOTTO:** Analytical Precision Meets Editorial Art Direction  

---

## 1. CORE PHILOSOPHY & IDENTITY

The design of **"What Are We Really Paying For When We Buy a Smartphone?"** establishes a new standard for data journalism. It repudiates both sterile corporate SaaS dashboards and superficial marketing brochures.

### The Six Pillars of the Aesthetic
1. **Industrial Precision:** Interfaces evoke high-end laboratory instruments, engineering blueprints, and aerospace technical documentation.
2. **Editorial Storytelling:** Content unfolds in deliberate narrative chapters, guiding the reader from market illusions to economic realities.
3. **Restrained Technical Hierarchy:** Layouts feature crisp grid structures, delicate technical coordinate marks, thin hairline dividers, and compact metadata chips.
4. **Deliberate Density (Anti-Fluff):** Avoid excessive empty whitespace. Information density is kept high, structured, and organized, respecting the user's intelligence and desire for substance.
5. **Interactive Intelligence:** Data graphics and 3D models invite tactile exploration, inspection, and user control.
6. **Visual Restraint:** Zero decorative gradients, zero blurry glassmorphism, zero floating animated blobs. Every element must communicate functional or analytical meaning.

---

## 2. COLOR SYSTEM

The palette is rooted in **Dark Technical with Accent**, providing deep contrast for technical specifications and data graphics.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              COLOR TOKENS                                   │
├──────────────────────┬──────────────────────┬───────────────────────────────┤
│ Token Name           │ Hex Value            │ Usage Role                    │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│ --color-canvas       │ #0B0C0E              │ Deep Graphite Background      │
│ --color-surface-1    │ #131519              │ Technical Charcoal Panels     │
│ --color-surface-2    │ #1C1F26              │ Elevated Cards & Modals       │
│ --color-surface-3    │ #252A34              │ Interactive Hover States      │
│ --color-border       │ rgba(255,255,255,0.08)│ Hairline Grid Boundaries     │
│ --color-border-focus │ #E63946              │ Active Selection Accent       │
│ --color-text-primary │ #F3F4F6              │ Off-White Headings & Primary  │
│ --color-text-secondary│ #9CA3AF             │ Slate Grey Body Copy          │
│ --color-text-muted   │ #6B7280              │ Metadata, Units, Labels       │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│ --color-accent       │ #E63946              │ Industrial Crimson (Trial 1)  │
│ --color-accent-hover │ #FF4D5A              │ Accent Interactive Glow       │
│ --color-accent-alt   │ #D4FF00              │ Signal Lime (Backup Accent)   │
└──────────────────────┴──────────────────────┴───────────────────────────────┘
```

### Contrast & Accessibility Compliance
- **Text Primary (`#F3F4F6`) on Canvas (`#0B0C0E`):** Contrast ratio **15.8:1** (Exceeds WCAG AAA requirement of 7:1).
- **Text Secondary (`#9CA3AF`) on Canvas (`#0B0C0E`):** Contrast ratio **7.2:1** (Exceeds WCAG AA requirement of 4.5:1).
- **Accent Industrial Crimson (`#E63946`) on Canvas (`#0B0C0E`):** Contrast ratio **4.9:1** (Exceeds WCAG AA requirement for UI elements and large text).
- **Validation Rule:** All interactive data points and chart marks using the accent color must be reinforced with shape, size, or explicit text labels to ensure full accessibility for color-vision-deficient users.

---

## 3. TYPOGRAPHY SYSTEM

Typography is strictly composed using open-source **Google Fonts** to guarantee zero licensing liability while achieving an authentic editorial feel.

```
Manrope (Display)           IBM Plex Sans (Body)        IBM Plex Mono (Technical)
Aa Bb Cc 123                Aa Bb Cc 123                Aa Bb Cc 123
Tight Tracking (-0.03em)    Balanced Reading (1.65)     Tabular Numerals
Prominent Headlines         Editorial Narratives        Specs, Units, Prices
```

### Type Hierarchy Specifications

```css
/* Typography Design Tokens */
:root {
  --font-display: 'Manrope', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-body: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'IBM Plex Mono', 'Courier New', monospace;

  /* Type Scale */
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

### Typographic Rules
1. **Tabular Numerals:** All financial figures, specs (RAM, Storage, mAh), and chart axes must use CSS `font-variant-numeric: tabular-nums` to ensure exact column alignment.
2. **Controlled Line Length:** Long-form editorial body copy must be clamped to a maximum width of `68ch` to maintain optimal reading ergonomics.
3. **No Decorative Fonts:** Strictly avoid novelty, futuristic, or decorative display fonts that degrade reading speed.

---

## 4. LAYOUT & SPATIAL COMPOSITION

### Deliberate Density Framework
The user interface avoids vast expanses of purposeless whitespace. Spatial composition is guided by the **Structured Technical Grid**:

- **Grid Columns:** 12-column responsive layout with `16px` gutters on desktop, collapsible to 4 columns on mobile.
- **Section Rhythm:** Sections are framed as distinct editorial chapters separated by subtle hairline borders (`1px solid rgba(255, 255, 255, 0.08)`) and technical section identifiers (e.g., `// CHAPTER 01: SILICON ECONOMICS`).
- **Data Densification:** Information is packaged into compact technical matrices, spec chips, and coordinate stamps rather than sprawling consumer cards.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ [TOP BAR] LOGO / WORKING TITLE           [CURRENCY: USD $ ▼] [EXPLORE BTN]  │
├─────────────────────────────────────────────────────────────────────────────┤
│ // 00.01 / TEARDOWN INTRO                                                   │
│                                                                             │
│                   WHAT ARE WE REALLY PAYING FOR?                            │
│                                                                             │
│   ┌───────────────────────────────────┬─────────────────────────────────┐   │
│   │                                   │  COMPONENT TELEMETRY:           │   │
│   │                                   │  [01] AMOLED Display (120Hz)    │   │
│   │          [3D SMARTPHONE           │  [02] CNC Titanium Chassis      │   │
│   │            EXPLODED               │  [03] Snapdragon 8 Gen 3 SoC    │   │
│   │             VIEW]                 │  [04] 5,400 mAh Battery Cell    │   │
│   │                                   │  [05] 50MP Periscope Optics     │   │
│   │                                   │                                 │   │
│   │  [◄ SCRUBBER ►] [REASSEMBLE]      │  ESTIMATED BOM SHARE: ~52%      │   │
│   └───────────────────────────────────┴─────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Fixed Compact Navigation
- Height: `56px`.
- Sticky positioning (`position: sticky; top: 0; z-index: 100`).
- Subtle backdrop blur (`backdrop-filter: blur(12px); background: rgba(11, 12, 14, 0.85)`).
- Contains: Project Title, Chapter Quick-Jump Anchor, Currency Switcher (`USD`, `INR`, `IDR`), and a prominent direct link to the `/explore` route.

---

## 5. HERO EXPERIENCE & 3D INTERACTIVE DISASSEMBLY

### Fictional Concept Smartphone
The 3D model represents an idealized fictional concept smartphone. It intentionally avoids copying any specific commercial device (such as the iPhone 15 Pro or Galaxy S24 Ultra) to prevent misleading teardown claims and intellectual property conflicts.

### Visual Quality Benchmarks
- **Geometry:** Clean quad/tri topology with smooth beveled edges; zero low-poly faceting or jagged silhouettes.
- **PBR Materials:**
  - *Chassis:* Anodized dark titanium with subtle anisotropic micro-brushing.
  - *Display Assembly:* Ultra-glossy cover glass with deep black active OLED matrix beneath.
  - *Logic Board:* Dark matte FR4 PCB with visible gold-plated contacts and solder traces.
  - *SoC Heat Spreader:* Copper vapor chamber with laser-etched fictional markings.
  - *Battery:* Matte silver/black lithium pouch cell with micro-warning labels.
  - *Optics:* Multi-element coated camera lenses with realistic antireflective purple/blue reflections.
- **Lighting & Shadows:** Three-point studio lighting with high-contrast rim highlights and soft contact ambient occlusion.

### Interactive Scroll Disassembly Choreography

$$\begin{array}{rll}
0\% - 20\%: & \textbf{Fully Assembled} & \text{Device rests intact, slight glancing light reflection} \\
20\% - 40\%: & \textbf{Enclosure Separation} & \text{Front display panel and rear glass lift outward on Z-axis} \\
40\% - 65\%: & \textbf{Core Components Emerge} & \text{Battery cell, camera array, and vapor chamber lift from frame} \\
65\% - 85\%: & \textbf{Logic Board Breakdown} & \text{Motherboard, SoC shield, and secondary sub-boards separate} \\
85\% - 100\%: & \textbf{Fully Exploded Technical View} & \text{All 7 internal layers suspended with active interactive hotspot pins}
\end{array}$$

### Interaction & Accessibility Controls
1. **Interactive Hotspots:** Clicking an exploded component highlights its mesh and opens a technical telemetry card displaying its manufacturing complexity and estimated share of total Bill of Materials (BOM).
2. **Manual Scrubber:** A compact slider bar allows non-scrolling users to scrub component separation directly.
3. **Reassemble Button:** One-click reset returning the phone smoothly to its 0% assembled state.
4. **Skip Button:** Floating action pill jumping past the 3D scroll track directly to Chapter 01.
5. **No Scroll-Jacking:** Implemented via standard CSS sticky positioning (`position: sticky; top: 0; height: 100vh`) inside a `350vh` container. Normal scroll momentum is never hijacked.
6. **Reduced-Motion Fallback:** When `prefers-reduced-motion: reduce` is active, the 3D scroll track is replaced by an interactive 2D exploded technical blueprint with accessible tabs.

---

## 6. MOTION & TRANSITIONS (HYBRID CINEMATIC MOTION)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            MOTION HIERARCHY                                 │
├────────────────────┬────────────────────────────────────────────────────────┤
│ Layer              │ Behavior                                               │
├────────────────────┼────────────────────────────────────────────────────────┤
│ Page Scroll        │ Cinematic smooth scrolling with natural browser physics│
│ Chapter Transitions│ Distinct chapters with seamless continuous framing     │
│ 3D Disassembly     │ Scroll-synchronized transformation (Z-axis separation) │
│ Data Visualizations│ D3 smooth data joins and morphs on filter change (400ms)│
│ Cards & Chips      │ Micro-hover states (150ms ease-out)                    │
│ Editorial Copy     │ Completely static for relaxed, fatigue-free reading    │
│ Ambient Decor      │ Strict zero; no spinning loops or battery-draining GPU │
└────────────────────┴────────────────────────────────────────────────────────┘
```

---

## 7. DATA VISUALIZATION SPECIFICATIONS

1. **Analytical Clarity Over Novelty:** Standard charts (Scatter plots, Box plots, Histograms, Slope charts) are enhanced with technical precision rather than replaced by confusing novelty charts.
2. **Selective 3D Visualizations:** 3D charts are permitted *only* when illustrating true 3-dimensional parameter spaces (e.g., Price vs. RAM vs. Release Year surface distribution). 2D charts must never be artificially rendered in 3D.
3. **Interactive D3 Tooltips:** Hovering a data point displays a technical telemetry card containing:
   - Device Name & Brand
   - Exact Retail Price in Active Selected Currency
   - Key Specs (RAM, Storage, Battery, SoC)
   - MySmartPrice Expert Rating (where available)
   - Excerpt from verified editorial review
4. **Accessible Tables:** Every complex chart includes a togglable accessible data table for keyboard and screen-reader accessibility.

---

## 8. PERFORMANCE TARGETS

- **Lighthouse Performance Score:** $\ge 90$ on desktop, $\ge 80$ on mid-tier mobile.
- **Core Web Vitals:**
  - Largest Contentful Paint (LCP): $< 2.5\text{s}$
  - First Input Delay (FID) / Interaction to Next Paint (INP): $< 100\text{ms}$
  - Cumulative Layout Shift (CLS): $< 0.05$
- **3D Asset Budget:** Draco-compressed GLB asset $\le 3.5\text{ MB}$; textures $\le 2048\times 2048$ WebP.
- **Client Data Bundle:** Cleaned and indexed market JSON $\le 300\text{ KB}$ gzipped.
