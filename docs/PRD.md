# PRODUCT REQUIREMENTS DOCUMENT (PRD)

> **PROJECT:** What Are We Really Paying For When We Buy a Smartphone?  
> **STATUS:** Final Approved Baseline (Phase 02)  
> **TARGET AUDIENCE:** Technology Enthusiasts, Smartphone Consumers, Data-Oriented Readers  
> **LANGUAGE:** English  

---

## 1. PRODUCT OVERVIEW

"What Are We Really Paying For When We Buy a Smartphone?" is an interactive, research-driven editorial publication and data exploration platform. The product deconstructs smartphone retail pricing, hardware specifications, brand markup, and lifetime ownership economics. 

Rather than serving as another generic product comparison engine or declaring a single "best smartphone brand," the website empowers readers to understand:
- What components and costs actually comprise a modern smartphone.
- How specifications scale with price, and where the law of diminishing returns begins.
- How different brands position their hardware (e.g., Apple and Samsung pricing floors versus aggressive spec-sheet volume from Xiaomi, Realme, and Poco).
- The hidden long-term ownership factors—software update longevity, repairability, and battery health—that determine true value over time.

---

## 2. PROBLEM STATEMENT

The modern smartphone purchasing experience is obscured by aggressive marketing claims, superficial spec inflation, and brand prestige:
- **The Megapixel & Core Myth:** Consumers are bombarded with numbers (200MP cameras, 16-core NPUs, 24GB RAM) without understanding whether these specifications represent tangible real-world improvements or cheap marketing differentiators.
- **The True Cost of Brand Prestige:** Premium manufacturers command substantial price markups that consumers struggle to decouple from actual Bill of Materials (BOM) hardware costs.
- **The Ownership Blindspot:** While consumers scrutinize the upfront purchase price, they rarely account for the total cost of ownership—specifically, how software abandonment, non-modular construction, and battery degradation render a "cheap" phone expensive over a 3-to-5-year lifecycle.
- **Affiliate Bias in Tech Journalism:** Most tech comparison platforms are affiliate-driven shopping directories incentivized to push purchase transactions rather than provide objective economic critique.

---

## 3. PRODUCT GOALS

1. **Deliver an Authoritative Research Experience:** Present an intellectually rigorous, data-driven investigation that demystifies smartphone hardware economics.
2. **Provide Dual-Experience Architecture:** Combine an art-directed, chapter-based editorial narrative on the Homepage with an independent, multi-dimensional analytical tool on `/explore`.
3. **Pioneer Interactive Hardware Education:** Utilize a 3D fictional concept smartphone exploded teardown in the Hero to visually ground the discussion of component manufacturing costs.
4. **Maintain Absolute Scientific Integrity:** Clearly delineate directly measured empirical data from derived indices, external benchmarks, and analytical hypotheses.

---

## 4. TARGET AUDIENCE

1. **Technology Enthusiasts & Power Users:** Individuals who appreciate deep technical specifications, semiconductor architectures, and engineering schematics.
2. **Informed Consumers:** Prospective buyers looking to maximize value-for-money without being misled by marketing jargon.
3. **Data Analysts & Economics Students:** Readers interested in empirical pricing distributions, market tiering, and econometric storytelling.

---

## 5. RESEARCH QUESTIONS

1. **Silicon vs. Price:** How strongly does chipset performance (Snapdragon, MediaTek, Apple A-Series, Exynos) dictate retail price brackets?
2. **The Memory Markup:** What is the marginal cost per gigabyte of RAM and storage to the consumer, and how does it compare to raw NAND/DRAM spot market prices?
3. **The Brand Premium Index:** Holding hardware specifications constant, how much additional markup is commanded by Tier-1 brands (Apple, Samsung) compared to value-tier brands (Xiaomi, Realme, Infinix)?
4. **Diminishing Returns Threshold:** At what price threshold does each additional dollar invested in hardware yield statistically marginal gains in performance, display quality, and camera capability?
5. **Total Cost of Ownership (TCO):** When software support lifecycles, repair costs, and historical residual depreciation are factored in, does a flagship phone deliver a lower cost-per-day than budget devices?

---

## 6. RESEARCH FRAMEWORK & DATA CLASSIFICATION

The research is organized around two complementary investigative pillars:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           RESEARCH FRAMEWORK                                │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ PILLAR 01: PURCHASE VALUE            │ PILLAR 02: OWNERSHIP VALUE           │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • Retail Price Distribution (INR/USD)│ • Software Support Longevity (Years) │
│ • Component Specifications & Scaling │ • Physical Durability & IP Ingress   │
│ • Semiconductor / Chipset Hierarchy  │ • Repairability Index (iFixit / EU)  │
│ • RAM & Storage Margins              │ • Battery Degradation Curves         │
│ • Brand Premium Quantification       │ • Total Cost of Ownership Modeling   │
│ • Expert vs User Rating Divergence   │ • Resale Value Depreciation          │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

### Data Classification Matrix
Every data point in the product must strictly belong to one of five explicit classifications:
1. **Directly Measured:** Verified attributes from the de-duplicated MySmartPrice dataset (Price in INR, RAM in GB, Storage in GB, Battery mAh, Charging Watts, Display specs, SoC vendor/model, Ratings).
2. **Derived Metric:** Statistically calculated indices (Price per GB RAM, Price per Wh Battery, Megapixel density, Spec-to-Price Index, Brand Premium Index).
3. **External Research:** Published empirical benchmarks from authoritative third parties (official OEM software update policies from Apple/Google/Samsung, iFixit repairability scores).
4. **Hypotheses & Models:** Analytical projections (3-year and 5-year TCO simulations, residual depreciation models).
5. **Unavailable Information:** Explicit disclosures of data gaps (e.g., lack of public factory BOM teardowns for long-tail budget models, absence of official warranty RMA return rates).

---

## 7. DATA SOURCES & PROVENANCE

- **Primary Source:** Scraped catalog from Indian consumer technology portal *MySmartPrice* (`mysmartprice.com`), verified by `review_link` URL structures.
- **Original Dataset Size:** 2,928 rows.
- **De-duplicated Verified Size:** Exactly 2,256 unique records (672 duplicate rows removed; verified to be pagination crawl artifacts).
- **Temporal Coverage:** Mid-2011 (legacy feature phones like Nokia Asha 210) through August 2024 (Samsung Galaxy Z Fold6, iPhone 15 Pro Max, CMF Phone 1).
- **Original Currency:** Indian Rupee (INR, ₹).

---

## 8. DATA LIMITATIONS & DISCLAIMERS

1. **Geographic Market Scope:** The empirical pricing data reflects the **Indian retail smartphone market**. Indian retail prices incorporate 18% Goods and Services Tax (GST) and import tariffs on completely built units (CBUs), which inflate imported flagship prices (notably Apple iPhones) relative to locally assembled budget models.
2. **International Audience Context:** While the website caters to global technology readers, all converted prices (USD, IDR) represent mathematical conversions of Indian retail prices at fixed reference rates, not official US or Indonesian MSRPs.
3. **Temporal Cutoff:** The dataset concludes in August 2024. Late-2024 flagship releases (Apple iPhone 16 series, Google Pixel 9 series, Snapdragon 8 Elite, Dimensity 9400) are not present in the empirical dataset and must be contextualized as post-dataset developments where discussed.

---

## 9. INFORMATION ARCHITECTURE

The application is structured into two complementary routes:

```
WEBSITE INFORMATION ARCHITECTURE
├── / (HOMEPAGE: THE RESEARCH JOURNEY)
│   ├── [Global Navigation & Currency Selector]
│   ├── Chapter 00: Hero Teardown (Fictional 3D Exploded View)
│   ├── Chapter 01: Silicon Economics (SoC Hierarchy vs Price)
│   ├── Chapter 02: Memory Margins (RAM & Storage Markup Curves)
│   ├── Chapter 03: The Prestige Tax (Brand Positioning & Value Frontier)
│   ├── Chapter 04: The Ownership Reality (Software Lifespan, TCO, Repairability)
│   ├── Chapter 05: Editorial Synthesis & Recommendations
│   ├── Chapter 06: Data Provenance & Methodology Ledger
│   └── [Interactive Teaser & CTA to /explore]
└── /explore (INDEPENDENT DATA EXPLORATION ENGINE)
    ├── [Global Navigation & Currency Selector]
    ├── Global Market Summary Dashboard (KPIs, Price Tiers)
    ├── Multi-Dimensional Filtering Bar (Brand, Price, SoC, RAM, Display)
    ├── Interactive Value Frontier Scatter Plot (Spec Score vs Price)
    ├── Full Searchable Smartphone Catalog (2,256 Models)
    └── Device Detail Telemetry Drawer (Specs, Expert Reviews, TCO Estimate)
```

---

## 10. USER JOURNEYS

- **Journey 1 (The Narrative Reader):** Lands on `/` -> explores the 3D scroll disassembly -> reads Chapters 01 to 05 sequentially -> tests the embedded TCO simulator -> inspects the methodology ledger.
- **Journey 2 (The Analytical Explorer):** Lands on `/` -> clicks "Explore All 2,256 Models" in the top navigation -> navigates to `/explore` -> applies filters for "$200–$400", "Snapdragon", "120Hz AMOLED" -> explores the efficiency frontier on the scatter plot -> opens device telemetry cards.
- **Journey 3 (The International Buyer):** Changes global currency toggle to INR or IDR -> notes the currency disclaimer -> navigates through both `/` and `/explore` with all figures, tooltips, and calculations updated in real-time.

---

## 11. FUNCTIONAL REQUIREMENTS

- **FR01 (Global Currency Toggle):** Persistent selector in top navigation supporting USD ($), INR (₹), and IDR (Rp). State persists in memory/localStorage and instantaneously updates all displayed prices across both routes without page reloads.
- **FR02 (3D Interactive Scroll Disassembly):** The 3D Hero on `/` binds scroll progress ($t \in [0, 1]$) to component Z-axis translation across 7 discrete mesh groups. Includes manual scrubber, reassemble button, and skip button.
- **FR03 (Multi-Dimensional Catalog Filtering):** The `/explore` route provides responsive client-side filtering by:
  - Price Range (Slider / Min-Max inputs in active currency)
  - Brand (Multi-select checkbox covering all extracted brands)
  - Chipset Vendor (Snapdragon, MediaTek, Apple, Exynos, Unisoc, Tensor)
  - RAM Capacity (4GB, 6GB, 8GB, 12GB, 16GB+)
  - Display Type (AMOLED, OLED, IPS, LCD)
  - Refresh Rate (60Hz, 90Hz, 120Hz, 144Hz+)
- **FR04 (Interactive Value Frontier):** D3 scatter plot on `/explore` plotting Hardware Spec Score against Retail Price, with interactive zoom, hover tooltips, and Pareto efficiency frontier overlay.
- **FR05 (Device Detail Drawer):** Clicking any phone row in `/explore` opens a technical drawer showing full specifications, battery charging wattage, expert rating, user rating count, and excerpt from MySmartPrice review.
- **FR06 (Total Cost of Ownership Simulator):** Interactive calculator allowing users to configure expected ownership duration (1 to 5 years), estimated daily usage, and repair contingencies, outputting an amortized cost-per-day calculation.

---

## 12. NON-FUNCTIONAL REQUIREMENTS

- **NFR01 (Client-Side Responsiveness):** Filter adjustments and currency switches in `/explore` must re-render the catalog and charts within $< 50\text{ms}$.
- **NFR02 (Rendering Performance):** The 3D WebGL hero and D3 charts must maintain 60 FPS on modern desktop browsers and $\ge 30\text{ FPS}$ on mid-tier mobile devices.
- **NFR03 (Asset Footprint):**
  - Production JavaScript bundle: $\le 250\text{ KB}$ gzipped (initial entry chunk).
  - 3D Model: $\le 3.5\text{ MB}$ Draco-compressed GLB.
  - Pre-processed Data JSON: $\le 300\text{ KB}$ gzipped.
- **NFR04 (Reliability):** Zero fatal client-side crashes; defensive handling of null or missing attributes in legacy records.

---

## 13. DATA VISUALIZATION REQUIREMENTS

1. **Ethical Axis Scaling:** Zero artificially truncated zero-baselines on bar charts. Scatter plot axes must clearly indicate whether scales are linear or logarithmic.
2. **Dual-Axis Synchronization:** Where dual-axis charts are used (e.g., Price vs. Spec Score), gridlines and zero-points must align mathematically.
3. **Informative Tooltips:** Every chart point must render rich metadata via accessible HTML tooltips rather than native browser title attributes.
4. **Accessible Fallbacks:** Every data visualization must offer an accessible tabular alternative togglable via button or screen-reader announcement.

---

## 14. HERO & INTERACTION REQUIREMENTS

- **Fictional Concept Smartphone:** The 3D model is explicitly designed as a fictional engineering prototype.
- **Component Separation Groups:**
  1. Front Display Assembly (Cover glass, OLED matrix)
  2. CNC Chassis Frame & Antenna Bands
  3. Logic Board (Motherboard with surface-mounted chips)
  4. Application Processor (SoC with vapor chamber heat pipe)
  5. Camera Module Array (Multi-lens optics)
  6. Lithium-Ion Battery Pouch Cell
  7. Rear Frosted Glass Backing
- **Non-Invasive Scroll Pinned Container:** Utilizes standard CSS sticky positioning (`position: sticky; top: 0; height: 100vh`) inside a `350vh` track. Never implements raw window scroll-jacking.
- **Full Reduced-Motion Support:** Automatic replacement with a 2D tabbed exploded blueprint when `prefers-reduced-motion` is detected.

---

## 15. CURRENCY BEHAVIOR & CONVERSION BASELINE

- **Ground Truth Storage:** All records store `price_inr` as an immutable integer.
- **Conversion Baseline (August 2024 Reference Rates):**
  - $1\text{ USD} = 83.90\text{ INR}$ (Reserve Bank of India reference rate, August 2024)
  - $1\text{ USD} = 15,600\text{ IDR}$ (Bank Indonesia reference rate, August 2024)
  - $1\text{ INR} = 185.94\text{ IDR}$
- **Formatting Standards:**
  - USD: `$X,XXX` (e.g., `$385`)
  - INR: `₹XX,XXX` (e.g., `₹34,999`)
  - IDR: `Rp X.XXX.XXX` (e.g., `Rp 6.006.000`)
- **Prominent Context Disclaimer:** Displayed adjacent to currency selector:  
  *"Prices reflect Indian market retail MSRP (inclusive of 18% GST and local import duties) converted at fixed August 2024 reference rates for international comparison, not US/EU retail MSRP."*

---

## 16. ACCESSIBILITY REQUIREMENTS (WCAG 2.1 AA)

- **Color Contrast:** Minimum 4.5:1 for body copy; minimum 3:1 for large display text and interactive UI elements.
- **Keyboard Navigation:** Full operational capability via `Tab`, `Shift+Tab`, `Enter`, `Space`, and `Escape`. Focus indicators must be prominent (`2px solid #E63946`).
- **Screen Reader Compatibility:** Semantic HTML tags (`<main>`, `<nav>`, `<article>`, `<section>`, `<aside>`); ARIA live regions for filtering status updates.
- **Motion Controls:** Strict compliance with `prefers-reduced-motion`.

---

## 17. PERFORMANCE REQUIREMENTS

- **Lighthouse Performance Score:** $\ge 90$ on desktop.
- **Core Web Vitals:** LCP $< 2.5\text{s}$, INP $< 100\text{ms}$, CLS $< 0.05$.
- **Asset Optimization:** WebP texture compression, Draco geometry compression, code splitting for Three.js and D3.js.

---

## 18. TECHNICAL ARCHITECTURE DIRECTION

- **Data Engineering:** Python 3.10+ reproducible script (`scripts/clean_data.py`) outputting sanitized JSON data bundles (`smartphones_cleaned.json`, `market_summary.json`).
- **Frontend Core:** Vite + React 18+ + TypeScript (Strict Mode).
- **Styling:** CSS Modules / Vanilla CSS Custom Properties following the Design Constitution.
- **3D Engine:** Three.js + React Three Fiber + Drei.
- **Charting Engine:** D3.js modular packages.
- **Hosting:** Static production export deployable to Vercel, Netlify, or GitHub Pages.

---

## 19. RISKS & MITIGATIONS

| Risk ID | Description | Severity | Mitigation Strategy |
|---|---|---|---|
| **R01** | Low-end mobile GPUs struggle with 3D WebGL Hero. | High | Detect mobile viewport and WebGL capability; offer 1-click fallback to 2D technical diagram. |
| **R02** | Readers assume converted prices equal US MSRP. | Medium | Persistent, prominent market origin disclaimers attached to currency switcher and charts. |
| **R03** | Dataset cuts off mid-2024, excluding iPhone 16 / Pixel 9. | Low | Explicitly title and frame the research as a comprehensive analysis of the 2024 smartphone landscape. |
| **R04** | Readers misinterpret specification scores as objective quality. | High | Distinguish directly measured specs from derived scores; explicitly state that software optimization and optics tuning cannot be measured by hardware numbers alone. |

---

## 20. ACCEPTANCE CRITERIA

- [ ] All 672 duplicate rows removed from active data pipeline (yielding exactly 2,256 unique records).
- [ ] Zero instances of corrupted 1GB storage on 1TB devices; zero instances of corrupted RAM values.
- [ ] All 40+ brands accurately parsed and attributed.
- [ ] Global currency switcher operational across USD, INR, and IDR with real-time recalculation.
- [ ] Homepage renders chapter-based narrative with 3D exploded view Hero (0% to 100% disassembly).
- [ ] `/explore` route provides responsive filtering and sorting across all 2,256 models.
- [ ] D3 Value Frontier scatter plot renders smoothly with interactive tooltips and table fallback.
- [ ] Full `prefers-reduced-motion` compliance across 3D and scroll animations.
- [ ] Zero unhandled console warnings or errors.

---

## 21. FUTURE OPPORTUNITIES

1. **Global Retail Price API:** Real-time ingestion of US and EU retail pricing via retail APIs to compare international price differentials directly against Indian MSRPs.
2. **Interactive Blind Camera Test Integration:** Embedding community blind test data to contrast real user perceptual quality with megapixel counts.
3. **Consumer Longevity Survey Module:** Self-reporting tool for long-term battery degradation and component failures.
