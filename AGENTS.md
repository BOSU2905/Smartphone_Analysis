# AGENTS.md — PROJECT GOVERNANCE & AGENT DIRECTIVE

> **PROJECT TITLE:** What Are We Really Paying For When We Buy a Smartphone?  
> **PRODUCT IDENTITY:** Experimental Technical Editorial  
> **SCOPE & CONTEXT:** Indian Smartphone Market Research (2011 – Mid-2024), 2,256 Unique Empirical Records  
> **MANDATORY WORKFLOW:** DISCOVER → AUDIT → PLAN → APPROVE → IMPLEMENT → REVIEW

---

## 1. PROJECT OVERVIEW & CORE MISSION

This repository contains the data assets, research foundation, and technical architecture for an interactive editorial investigation into smartphone pricing, hardware specifications, brand positioning, and ownership economics.

The project is **not** a generic smartphone comparison website, an e-commerce affiliate catalogue, or a subjective "best phone" recommendation engine. Its goal is to provide technology enthusiasts, consumers, and data-oriented readers with an intellectually rigorous, visually compelling, and interactive teardown of mobile economics.

### The Two Investigative Pillars

1. **Pillar 01 — Purchase Value:**
   - Empirical relationship between retail price and hardware specifications (SoC silicon, RAM, storage, battery capacity, fast charging, display technology, optics).
   - Brand positioning, market tiering, and quantification of the "brand premium" (e.g., Apple and Samsung pricing floors versus aggressive value brands like Xiaomi, Realme, and Poco).
   - Divergence between expert technical ratings and consumer perception ratings.
   - Analysis of diminishing returns across price brackets.

2. **Pillar 02 — Ownership Value:**
   - Software support lifecycles (guaranteed Android OS updates and security patches vs. Apple iOS historical longevity).
   - Physical durability, ingress protection (IP ratings), and glass standards.
   - Repairability scores, parts availability, and modularity.
   - Battery cycle degradation models.
   - Long-term Total Cost of Ownership (TCO) and residual resale depreciation.

---

## 2. REPOSITORY PRESERVATION & INTEGRITY RULES

All agents operating in this workspace must strictly obey the following preservation constraints:

1. **Zero Silent Modification of Raw Data:** Never edit, truncate, overwrite, or re-encode `Data/raw/smartphones_uncleaned.csv`. The raw dataset is the immutable ground truth.
2. **Preservation of Research Assets:** Never delete or overwrite the historical notebooks (`notebooks/main.ipynb`, `notebooks/analyze.ipynb`) or intermediate datasets.
3. **Legacy Prototype Preservation:** The existing Streamlit prototype (`app.py`) represents historical project discovery. In accordance with approved decision **H01**, `app.py` will be preserved under `legacy/streamlit_prototype/` when frontend implementation begins. It must not be deleted.
4. **Clean Git State:** Inspect `git status` before beginning work. Never perform unrelated refactoring. Every commit must correspond to an approved roadmap phase.

---

## 3. RESEARCH INTEGRITY & DATA PROVENANCE RULES

Every agent, writer, and engineer must maintain strict academic and journalistic integrity:

1. **Market Origin Transparency:** The empirical dataset originates from the Indian smartphone retail market (*MySmartPrice*, scraped mid-2024). All baseline prices are in Indian Rupees (INR). Converted prices (USD, IDR) must always be labeled as converted Indian retail prices, reflecting local GST (18%) and import tariffs. Never present converted INR prices as official US or global retail MSRP.
2. **Rigorous Data Classification:** Every metric presented in copy, charts, or tables must belong to one of five explicit classifications:
   - **Directly Measured:** Verified data from the 2,256 unique records (Price in INR, RAM in GB, Storage in GB, Battery mAh, Charging Watts, Display specs, SoC vendor/model, Ratings).
   - **Derived Metric:** Statistically calculated indices (Price per GB RAM, Spec-to-Price Index, Brand Premium Index).
   - **External Research:** Peer-reviewed benchmarks or verified official documentation (OEM update policies from Apple/Google/Samsung, iFixit repairability ratings).
   - **Hypotheses & Models:** Explicit mathematical simulations (e.g., 3-year TCO amortizations, depreciation models).
   - **Unavailable Information:** Explicit disclosures where data is missing (e.g., factory Bill of Materials for obscure legacy devices, official RMA failure rates).
3. **No Fabricated Evidence:** Never invent citations, benchmark scores, or specifications. If a data point is unverified, state its absence clearly.
4. **No Premature Conclusions:** Never declare an arbitrary "price sweet spot" or universal "value score" without presenting the underlying empirical methodology and sensitivity analysis.

---

## 4. AGENT WORKFLOW & PHASE GOVERNANCE

Agents must adhere to the six-stage workflow lifecycle without exception:

$$\text{DISCOVER} \longrightarrow \text{AUDIT} \longrightarrow \text{PLAN} \longrightarrow \text{APPROVE} \longrightarrow \text{IMPLEMENT} \longrightarrow \text{REVIEW}$$

1. **DISCOVER:** Inspect the workspace, read existing files, and verify dependencies before taking action.
2. **AUDIT:** Measure dimensions, identify edge cases, catalog defects, and evaluate performance overhead.
3. **PLAN:** Formulate a structured implementation proposal with concrete acceptance criteria and risk mitigations.
4. **APPROVE:** Surface all key architectural, visual, and econometric decisions to the user. **Wait for explicit approval.** Never proceed to implementation without authorization.
5. **IMPLEMENT:** Execute the approved plan cleanly within defined phase boundaries. Do not jump ahead to subsequent phases.
6. **REVIEW:** Perform automated linting, test suites, accessibility audits (WCAG 2.1 AA), and performance checks. Verify that git changes match the approved scope.

---

## 5. SKILLS ARCHITECTURE & ACTIVATION DIRECTORY

The project utilizes eight dedicated workspace skills located in `.agents/skills/`. Agents must consult and activate these skills whenever performing tasks within their respective domains:

```
.agents/skills/
├── research-integrity/        # Enforces data classification, provenance, and statistical ethics
├── editorial-copywriting/     # Guides compelling, natural English editorial prose without AI clichés
├── visual-art-direction/      # Governs the Experimental Technical Editorial aesthetic and layout
├── typography-system/         # Manages Manrope, IBM Plex Sans, IBM Plex Mono hierarchy and tokens
├── data-visualization/        # Governs D3.js charts, responsive scales, and ethical data representation
├── interaction-design/        # Manages 3D scroll disassembly, micro-interactions, and accessibility
├── frontend-engineering/      # Governs Vite, React, TypeScript, state management, and build hygiene
└── quality-review/            # Comprehensive audit checklists for QA, WCAG 2.1 AA, and Lighthouse 95+
```

### Synergy with Built-in Antigravity Capabilities
- Use `modern-web-guidance` for HTML/CSS modern web platform APIs and container queries.
- Use `chrome-devtools` and `a11y-debugging` for DOM inspection and WCAG verification.
- Use `debug-optimize-lcp` and `memory-leak-debugging` for performance profiling.
- Use `agy-customizations` as the authoritative reference on customization discovery and precedence.

---

## 6. TECHNICAL CONVENTIONS & ARCHITECTURE

- **Data Pipeline:** Python 3.10+ scripts located in `scripts/`. Must be reproducible, fully typed, unit-tested with `pytest`, and output immutable static JSON files for frontend ingestion.
- **Frontend Stack:**
  - Build Engine: Vite
  - Language: TypeScript (strict mode enabled, zero `any` types for dataset entities)
  - UI Library: React 18+
  - Data Visualization: D3.js (`d3-scale`, `d3-axis`, `d3-shape`, `d3-selection`)
  - 3D Graphics: Three.js via React Three Fiber (`@react-three/fiber`) and Drei (`@react-three/drei`)
  - Styling: CSS Modules / Vanilla CSS Custom Properties (strict adherence to Design Constitution tokens)
- **Deployment Target:** Static bundle deployable to Vercel, Netlify, Cloudflare Pages, or GitHub Pages. Zero runtime server overhead.

---

## 7. KEY REFERENCE DOCUMENTS

- **Product Requirements Document (PRD):** [`docs/PRD.md`](file:///c:/Smartphone%20Analysis/Smartphone_Analysis/docs/PRD.md)
- **Design Constitution:** [`docs/DESIGN_CONSTITUTION.md`](file:///c:/Smartphone%20Analysis/Smartphone_Analysis/docs/DESIGN_CONSTITUTION.md)
- **Architectural Decision Log:** [`docs/DECISION_LOG.md`](file:///c:/Smartphone%20Analysis/Smartphone_Analysis/docs/DECISION_LOG.md)
- **Phase 01 Forensic Audit Report:** Delivered in Phase 01 executive transcripts.
