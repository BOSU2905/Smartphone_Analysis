# ARCHITECTURAL & PRODUCT DECISION LOG

> **PROJECT:** What Are We Really Paying For When We Buy a Smartphone?  
> **STATUS:** Approved Baseline  
> **LAST UPDATED:** 2026-11-16  

This document logs all fundamental product, architectural, econometric, and design decisions approved for the project. No approved decision may be reversed without explicit stakeholder review.

---

## 1. APPROVED CORE DECISIONS (H01 – H05)

### Decision H01: Legacy Streamlit Prototype Disposition
- **Status:** APPROVED
- **Context:** The original repository contains `app.py`, an exploratory Streamlit prototype.
- **Decision:** Preserve `app.py` and its dependencies under `legacy/streamlit_prototype/` when frontend implementation begins in later phases. Do not delete or overwrite the historical prototype. Maintain Git commit continuity.
- **Rationale:** Preserves historical provenance, allowing validation of original findings while decoupling the modern web application.

### Decision H02: 3D Hero Asset Procurement Strategy
- **Status:** APPROVED
- **Context:** The hero requires an interactive smartphone exploded view with smooth component separation and realistic engineering materials.
- **Decision:** Utilize a curated, high-fidelity engineering 3D model of a fictional concept smartphone, subject to license verification (CC0 / Royalty-Free), geometric topology inspection, clean material group separation, and Draco GLB compression (<3.5 MB).
- **Rationale:** Balances photorealistic product visualization with fast web load times; prevents any legal or factual claims that the model represents an exact commercial teardown.

### Decision H03: Primary Accent Color Selection
- **Status:** APPROVED (INITIAL TRIAL)
- **Context:** The Dark Technical visual palette requires a high-contrast accent token.
- **Decision:** Execute the initial design implementation using **Industrial Crimson** (`#E63946` / `#FF3B30`). Maintain **Signal Lime** (`#D4FF00`) as a validated fallback if contrast audits or visual testing reveal legibility issues in data charts.
- **Rationale:** Industrial Crimson delivers an urgent, precision-engineering aesthetic inspired by technical instrumentation without resorting to generic SaaS blues.

### Decision H04: Currency Architecture & Exchange-Rate Baseline
- **Status:** APPROVED
- **Context:** The dataset originated from the Indian market (prices in INR). The existing notebook used a crude hardcoded factor of `0.011`.
- **Decision:**
  - Base currency stored in data pipeline: Indian Rupee (INR, ₹).
  - Default display currency on site: United States Dollar (USD, $).
  - Alternative supported currencies: Indian Rupee (INR, ₹) and Indonesian Rupiah (IDR, Rp).
  - Historical reference baseline rates (August 2024):
    - $1\text{ USD} = 83.90\text{ INR}$ (Reserve Bank of India reference rate, August 2024)
    - $1\text{ USD} = 15,600\text{ IDR}$ (Bank Indonesia reference rate, August 2024)
    - $1\text{ INR} = 185.94\text{ IDR}$ (Cross-rate calculation)
  - Clear user labeling: All converted prices must feature an explicit disclaimer stating they reflect Indian retail prices (inclusive of 18% GST and import duties) converted at fixed August 2024 reference rates for international comparison, not US/EU retail MSRP.
- **Rationale:** Ensures econometric honesty, prevents misleading comparisons with US retail pricing, and avoids dynamic exchange-rate drift across historical phone releases.

### Decision H05: Scope of Pillar 02 (Ownership Value) External Research
- **Status:** APPROVED
- **Context:** The raw dataset contains hardware specs and ratings, but lacks empirical measurements of software update lifecycles, repairability scores, and battery degradation.
- **Decision:** Incorporate a curated reference ledger of verified external benchmarks from authoritative sources:
  - Official OEM software update commitments (Apple 5–7 years, Google Pixel 7 years, Samsung Galaxy 7 years, Xiaomi/Realme/Motorola 1–3 years).
  - Standardized repairability scores (iFixit and French Repairability Index benchmarks).
  - Standard lithium-ion battery degradation modeling (80% retention at 500 to 1,000 cycles).
  - Total Cost of Ownership (TCO) simulation amortized over 1, 3, and 5 years.
  - Strict classification: These values must be explicitly labeled as *External Research & Models*, never conflated with directly measured dataset fields.
- **Rationale:** Fulfills the core mission of exploring long-term value without fabricating data or claiming hardware specs prove longevity on their own.

---

## 2. APPROVED DESIGN & USER EXPERIENCE DECISIONS

### Decision D01: Two-Tier Website Architecture
- **Status:** APPROVED
- **Architecture:**
  - **Tier A: Main Research Journey (Homepage `/`):** A cinematic, chapter-based long-form editorial narrative with scroll-driven transitions and embedded interactive visualizations.
  - **Tier B: Independent Explore Experience (`/explore`):** A dedicated analytical tool containing the complete searchable catalog of 2,256 models, multi-dimensional filters, scatter plots, brand positioning matrices, and individual device deep-dives.
  - The homepage provides an interactive teaser and prominent entry points to `/explore`.
- **Rationale:** Prevents the editorial story from degenerating into a chaotic SaaS dashboard, while satisfying power users who want unrestricted data exploration.

### Decision D02: Typography System (Google Fonts Only)
- **Status:** APPROVED
- **Approved Typefaces:**
  - **Manrope:** Display headlines, section headers, and bold editorial statements.
  - **IBM Plex Sans:** Long-form body copy, explanatory callouts, and interface text.
  - **IBM Plex Mono:** Hardware specifications, prices, currency symbols, chart axes, metadata tags, and technical coordinates.
- **Rationale:** 100% open-source Google Fonts with zero licensing liability; provides high legibility, clean tabular numbers, and a technical editorial aesthetic.

### Decision D03: Hero Concept — Fictional Smartphone Teardown
- **Status:** APPROVED
- **Concept:** The 3D model represents an idealized fictional flagship smartphone, not an imitation of any real-world device (e.g., iPhone or Galaxy).
- **Interaction:** Interactive Scroll Disassembly with standard CSS sticky positioning (`position: sticky`), progress scrubber, component click inspection, reassemble button, skip button, and full `prefers-reduced-motion` 2D fallback.
- **Disclaimer:** The site clearly states that the exploded view is an illustrative engineering visualization of modern smartphone component distribution.

### Decision D04: Layout Density & Rhythm
- **Status:** APPROVED
- **Rule:** Avoid excessive empty white/graphite space. Employ structured technical composition with high information density, clean grid borders (`1px solid rgba(255,255,255,0.08)`), compact data chips, and clear typographic hierarchy.
- **Rationale:** Respects user preference for dense, purposeful technical interfaces over generic minimalist fluff.

### Decision D05: Motion & Transition Hierarchy
- **Status:** APPROVED
- **Framework:** Hybrid Cinematic Motion.
  - Smooth scrolling for narrative momentum.
  - Distinct editorial chapters with seamless continuity.
  - Interactive chart transitions.
  - Subtle hover states on data cards.
  - Static, calm reading state for body text.
  - Zero decorative animation loops that burn CPU/GPU cycles.
