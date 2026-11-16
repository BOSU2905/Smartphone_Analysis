---
name: research-integrity
description: >-
  Enforces statistical rigor, data provenance, currency transparency, and strict data
  classification across all project phases. Use whenever writing copy, generating metrics,
  cleaning datasets, or constructing data visualizations.
---

# Research Integrity Skill

This skill governs the scientific, statistical, and journalistic integrity of the **"What Are We Really Paying For When We Buy a Smartphone?"** project.

---

## 1. WHEN TO ACTIVATE

Activate this skill whenever:
- Formulating or reviewing data cleaning and preprocessing scripts.
- Defining derived econometric or performance indices (e.g., Spec-to-Price Index, Brand Premium Index).
- Writing editorial narratives, chapter conclusions, or analytical claims.
- Designing charts, scatter plots, or statistical summaries.
- Validating currency conversions and international market disclaimers.

---

## 2. CORE RESPONSIBILITIES

1. **Enforce Data Provenance:** Ensure every empirical claim traces directly back to verified rows in the de-duplicated MySmartPrice dataset (2,256 unique records).
2. **Uphold Data Classification:** Mandate that all displayed numbers are explicitly categorized into one of the five approved tiers (Directly Measured, Derived Metric, External Research, Hypotheses & Models, Unavailable Information).
3. **Prevent False Causal Attribution:** Forbid claiming that raw hardware specifications (e.g., high megapixel count, high RAM capacity) prove superior real-world performance, durability, or longevity.
4. **Ensure Currency & Geographic Accuracy:** Verify that all prices originate from Indian retail prices (in INR) and are explicitly identified as such, rather than conflated with US or global retail MSRPs.
5. **Acknowledge Data Boundaries:** Clearly document temporal cutoffs (August 2024) and data absence without attempting to fabricate missing values.

---

## 3. MANDATORY RULES

- **RULE 1 (Zero Fabrication):** Never invent benchmark scores, prices, component specifications, or user ratings. If a model lacks a specific spec, state it as "Unknown" or exclude it with an explicit filter note.
- **RULE 2 (Ground Truth Currency):** The ground truth currency is strictly **INR (₹)**. Converted values in USD and IDR must be derived from verified fixed reference rates (August 2024: $1\text{ USD} = 83.90\text{ INR}$, $1\text{ USD} = 15,600\text{ IDR}$) and must carry the approved Indian-market context disclaimer.
- **RULE 3 (Pillar 02 Boundary):** Long-term ownership claims (software support lifecycles, repairability, battery degradation) must cite verified external research (Apple/Google/Samsung official policies, iFixit benchmarks), never fabricated or claimed to be measured directly by the MySmartPrice dataset.
- **RULE 4 (No Premature "Sweet Spots"):** Do not declare an authoritative "price sweet spot" or universal "best value smartphone" without showing the full mathematical distribution and efficiency frontier.
- **RULE 5 (Correlation vs. Causation):** Treat correlations between price and specs as market associations, not engineering determinants of product quality.

---

## 4. INTEGRITY WORKFLOW

```
[RAW DATA INGESTION]
       │
       ▼
[VERIFY PROVENANCE & DEDUPLICATION] ── (Confirm 2,256 unique records)
       │
       ▼
[CLASSIFY METRIC TIER] ─────────────── (Measured / Derived / External / Model / Unavailable)
       │
       ▼
[VALIDATE DERIVATION MATH] ─────────── (Check units: MB vs GB, TB vs GB, INR to USD)
       │
       ▼
[DISCLOSE BOUNDARIES & CONTEXT] ────── (Indian market, GST included, Aug 2024 cutoff)
```

---

## 5. QUALITY AUDIT CHECKLIST

Before approving any editorial section, chart, or code artifact, verify:
- [ ] Are prices stored as base `price_inr` and converted transparently?
- [ ] Is the Indian market origin explicitly stated where prices are displayed?
- [ ] Are 1TB devices verified to contain 1024GB (not 1GB) storage?
- [ ] Are legacy MB RAM devices (e.g., 512MB) parsed correctly as fractional GB rather than clipped to 1GB?
- [ ] Does copy avoid claiming that high RAM or battery capacity directly guarantees long-term durability?
- [ ] Are external benchmarks for software support clearly distinguished from dataset attributes?
- [ ] Are axes on statistical charts properly labeled with units and scale types (linear/log)?

---

## 6. PROJECT CONTEXT & EXPLICIT LIMITATIONS

- **Dataset Scope:** 2,256 unique smartphone models sold in India between mid-2011 and August 2024.
- **Limitations:** Does not contain post-August 2024 releases (iPhone 16, Pixel 9, Snapdragon 8 Elite). Does not contain physical laboratory drop-test results or factory Bill of Materials (BOM) cost breakdowns.
