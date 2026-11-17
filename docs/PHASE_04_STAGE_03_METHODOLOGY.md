# PHASE 04 — STAGE 03: METHODOLOGY DESIGN & RESEARCH FRAMEWORK (FINAL VALIDATION)
## Econometric Specifications, Identification Strategy, and Statistical Governance

> **PROJECT TITLE:** What Are We Really Paying For When We Buy a Smartphone?  
> **PRODUCT IDENTITY:** Experimental Technical Editorial  
> **DOCUMENT TYPE:** Research Methodology Design & Pre-Analysis Protocol (Revision 04 — Formal Sign-Off)  
> **AUTHOR / ROLE:** Senior Data Scientist, Applied Econometrician & Quantitative Methodologist  
> **STATUS:** APPROVED BY PROJECT OWNER — FORMAL STAGE 03 METHODOLOGY BASELINE  
> **TARGET IMPLEMENTATION:** Phase 04 — Stage 04 (Analytical Modeling)  
> **ACCEPTED DATA BASELINE:** Commit `59906f6` (`phase-04-stage-02-implementation`)  
> **ANALYTICAL DATASET:** Exactly 2,256 verified, deduplicated records from Indian retail market catalog coverage (2011 – mid-2024)  
> **REVISION BASELINE:** Commit `73c70f0` (`docs/PHASE_04_STAGE_03_METHODOLOGY.md`)

---

## 01. Executive Summary

This document establishes the validated econometric methodology, statistical diagnostic hierarchy, and research governance protocols for investigating smartphone retail pricing, component specifications, and brand positioning.

The central research question is:
$$\textbf{"What are consumers actually paying for when purchasing a smartphone, and how do hardware specifications, brand identity, and market positioning relate to its listed retail price?"}$$

### The Methodological Stance: Observational Hedonic Econometrics

The research investigates smartphone pricing strictly as an **observational market equilibrium phenomenon**. In competitive differentiated-product markets, listed retail prices reflect both supply-side manufacturing costs (silicon, display panels, memory, optics, assembly, logistics, royalties) and demand-side valuation (brand reputation, operating system ecosystem, perceived build quality, marketing positioning, and consumer willingness-to-pay).

Because this study relies on observational web-scraped retail catalog data, **no simple regression model can establish pure causality**:
1. **Conditional Associations, Not Engineering Costs:** Regression coefficients reflect conditional empirical correlations between advertised specifications and listed retail prices. They do not measure the factory Bill of Materials (BOM) cost of components or the marginal cost of production.
2. **Compound Nature of Brand Differentials:** Estimated brand fixed effects ($\hat{\theta}_b$) capture both true brand equity (consumer willingness-to-pay for a badge) **and all unobserved product attributes correlated with that brand** (proprietary software optimization, industrial chassis metallurgy, IP water resistance certifications, optical image stabilization engineering, thermal dissipation chambers, acoustic tuning, and post-sales service networks). They must **never** be characterized in public editorial copy as "pure brand prestige taxes" or "irrational consumer markups."
3. **Target Population and External Validity:** 
   $$\textbf{"The findings describe associations within the collected smartphone listings represented in the dataset, sourced from the Indian retail catalog coverage documented by the project."}$$
   The dataset reflects the **menu of retail offerings cataloged on Indian price-comparison aggregators**, not unit sales, transaction volumes, or consumer adoption. A model with one listing may have sold five million units, while another sold five thousand. Listing counts must never be interpreted as consumer adoption, unit sales, or commercial market share.

---

## 02. Research Questions and Formal Hypotheses

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       RESEARCH QUESTION HIERARCHY                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ CENTRAL QUESTION: What are consumers actually paying for when purchasing   │
│ a smartphone, and how do hardware specifications, brand identity, and       │
│ market positioning relate to its listed retail price?                       │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ PILLAR 01: SPECIFICATION SCALING     │ PILLAR 02: BRAND POSITIONING         │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • RQ1.1: Memory Upgrades & Scaling   │ • RQ2.1: Conditional Brand Spreads   │
│ • RQ1.2: Semiconductor Stratification│ • RQ2.2: Spec-Sheet Explanatory Share│
│ • RQ1.3: Battery Ergonomic Decoupling│ • RQ2.3: Segment Brand Heterogeneity │
│ • RQ1.4: Display Technology Premium  │                                      │
├──────────────────────────────────────┴──────────────────────────────────────┤
│ PILLAR 03: MARKET SEGMENTATION & DIMINISHING RETURNS                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ • RQ3.1: Structural Elasticity Shifts Across Editorial Price Tiers         │
│ • RQ3.2: Exploratory Quantile Trajectories (Model 6 Extension)              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Pillar 01 — Specification Scaling & Marginal Hedonic Associations
- **RQ1.1 (Memory Scaling):** Holding other observable hardware attributes constant, what is the conditional percentage price difference associated with an additional gigabyte of RAM and an additional gigabyte of internal storage in the cross-section of retail offerings?
- **RQ1.2 (Semiconductor Hierarchy):** What conditional price differentials exist across application processor manufacturers (Qualcomm Snapdragon, MediaTek, Apple Silicon, Samsung Exynos, Unisoc, HiSilicon Kirin) when controlling for memory and display attributes?
- **RQ1.3 (Battery Capacity & Ergonomic Decoupling):** Does battery capacity (mAh) maintain a positive conditional association with retail price, or does its association turn negative/negligible once physical dimensions, weight, and flagship tiering are accounted for?
- **RQ1.4 (Display Panel Technology):** What is the conditional price premium associated with OLED display panels (AMOLED, P-OLED, Super AMOLED) relative to baseline LCD panels (IPS, TFT)?

### Pillar 02 — Brand Positioning & Price Differentials
- **RQ2.1 (Conditional Brand Spread):** After adjusting for observable hardware components, what conditional price differentials exist between established Tier-1 manufacturers (Apple, Samsung, Google) and high-volume value brands (Xiaomi, Redmi, Realme, POCO)?
- **RQ2.2 (Spec-Sheet Explanatory Share):** What proportion of cross-brand pricing variance is accounted for by observable hardware characteristics versus residual brand indicator fixed effects?
- **RQ2.3 (Brand Segment Heterogeneity):** Do brand price markups remain uniform across market tiers, or do they amplify in the upper-mid and premium brackets?

### Pillar 03 — Market Segmentation & Diminishing Returns
- **RQ3.1 (Segment Elasticity Shifts):** How do specification returns vary across the five established editorial price tiers (Entry-level $< ₹10\text{k}$, Budget-to-mid $₹10\text{k}–₹20\text{k}$, Mid-range $₹20\text{k}–₹35\text{k}$, Upper-mid $₹35\text{k}–₹60\text{k}$, Premium $\ge ₹60\text{k}$)?
- **RQ3.2 (Exploratory Quantile Trajectories):** How do returns to RAM, storage, and silicon vary across conditional price quantiles ($\tau \in \{0.10, 0.25, 0.50, 0.75, 0.90\}$)?

### Formal Research Hypotheses

| Hypothesis ID | Statement | Null Hypothesis ($H_0$) | Alternative Hypothesis ($H_A$) | Econometric Test |
|---|---|---|---|:---:|
| **H1 (Storage Association)** | Internal storage capacity exhibits a statistically significant positive conditional association with retail price. | $\beta_{\text{storage}} \le 0$ | $\beta_{\text{storage}} > 0$ | Cluster-robust $t$-test on $\beta_{\text{storage}}$ |
| **H2 (RAM Association)** | RAM capacity exhibits a statistically significant positive conditional association with retail price. | $\beta_{\text{ram}} \le 0$ | $\beta_{\text{ram}} > 0$ | Cluster-robust $t$-test on $\beta_{\text{ram}}$ |
| **H3 (Battery Decoupling)** | In a multivariate hedonic model controlling for screen size, SoC, and brand, battery capacity (mAh) exhibits a non-positive or statistically negligible association with retail price. | $\beta_{\text{battery}} > 0$ | $\beta_{\text{battery}} \le 0$ | Cluster-robust one-sided $t$-test |
| **H4 (OLED Panel Premium)** | OLED display technology commands a statistically significant conditional price premium over baseline LCD technology. | $\delta_{\text{OLED}} \le 0$ | $\delta_{\text{OLED}} > 0$ | Cluster-robust $t$-test on $\delta_{\text{OLED}}$ |
| **H5 (Apple Conditional Differential)** | Holding observable hardware specifications constant, Apple devices command a statistically significant positive price markup over the baseline reference brand. | $\theta_{\text{Apple}} \le 0$ | $\theta_{\text{Apple}} > 0$ | Cluster-robust $t$-test on $\theta_{\text{Apple}}$ |
| **H6 (Within-Device Upgrade Association)** | Upgrading internal storage within the identical smartphone model chassis is associated with a statistically significant positive price increase. | $\beta_{\text{within\_storage}} \le 0$ | $\beta_{\text{within\_storage}} > 0$ | Within-estimator $t$-test on $\Delta\text{Storage}$ |

---

## 03. Data & Variable Inventory

The econometric analysis will be conducted on the verified, deduplicated dataset produced in Phase 04 Stage 02:
- **Canonical Files:** [`Data/processed/smartphones_cleaned.csv`](file:///c:/Smartphone%20Analysis/Smartphone_Analysis/Data/processed/smartphones_cleaned.csv) and [`Data/processed/smartphones_cleaned.json`](file:///c:/Smartphone%20Analysis/Smartphone_Analysis/Data/processed/smartphones_cleaned.json)
- **Population:** Exactly 2,256 verified unique smartphone records.
- **Geographic Market:** Indian retail smartphone market catalog coverage.
- **Temporal Span:** Mid-2011 through August 2024 (unrecorded dates; see Section 09).

### Complete Variable Role & Missingness Ledger

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 VERIFIED VARIABLE INVENTORY & ROLES                                    │
├──────────────────────────────┬───────────┬──────────────┬────────────┬─────────────────────────────────┤
│ Field Name                   │ Data Type │ Role         │ Valid N (%)│ Description / Unit              │
├──────────────────────────────┼───────────┼──────────────┼────────────┼─────────────────────────────────┤
│ original_listed_price_inr    │ Integer   │ Dependent    │ 2256 (100%)│ Indian Rupee retail price (₹)   │
│ log_price_inr                │ Float     │ Transformed  │ 2256 (100%)│ ln(original_listed_price_inr)   │
│ listing_id                   │ String    │ Identifier   │ 2256 (100%)│ Source row provenance (rec_XXXX)│
│ device_id                    │ String    │ Cluster ID   │ 2256 (100%)│ Base model slug (1,647 unique)  │
│ config_id                    │ String    │ Identifier   │ 2256 (100%)│ Variant slug (2,255 unique)     │
│ ram_capacity_gb              │ Float     │ Core Regressor│ 2248 (99.6%)│ RAM capacity in Gigabytes (GB)  │
│ storage_capacity_gb          │ Float     │ Core Regressor│ 2254 (99.9%)│ Storage capacity in GB          │
│ battery_capacity_mah         │ Integer   │ Core Regressor│ 2256 (100%)│ Battery capacity in mAh         │
│ screen_size_inches           │ Float     │ Core Regressor│ 2255 (100%)│ Screen diagonal in inches       │
│ display_panel_family         │ Enum      │ Core Regressor│ 2254 (99.9%)│ OLED vs LCD binary category     │
│ rear_main_sensor_mp          │ Float     │ Core Regressor│ 2256 (100%)│ Primary rear camera resolution  │
│ rear_lens_count              │ Integer   │ Core Regressor│ 2256 (100%)│ Total rear optical lenses count │
│ front_main_sensor_mp         │ Float     │ Core Regressor│ 2224 (98.6%)│ Front selfie sensor resolution  │
│ processor_manufacturer       │ Enum      │ Core Regressor│ 2196 (97.3%)│ Silicon vendor (Qualcomm, etc.) │
│ brand_name                   │ Enum      │ Core Regressor│ 2256 (100%)│ 63 canonical brand names        │
│ brand_tier                   │ Enum      │ Stratifier   │ 2256 (100%)│ MAJOR (18), MID (15), NICHE (30)│
├──────────────────────────────┼───────────┼──────────────┼────────────┼─────────────────────────────────┤
│ charging_wattage             │ Float     │ Extended Reg │ 1321 (58.6%)│ Fast charging speed in Watts (W)│
│ refresh_rate_hz              │ Float     │ Extended Reg │ 1133 (50.2%)│ Panel refresh rate (Hz)         │
│ processor_core_count         │ Float     │ Extended Reg │ 2039 (90.4%)│ CPU cores count                 │
│ expert_rating                │ Float     │ Telemetry    │ 1398 (62.0%)│ MySmartPrice editorial score    │
│ user_rating_score            │ Float     │ Telemetry    │ 2185 (96.9%)│ Consumer star rating (0–5)      │
│ user_rating_count            │ Integer   │ Weighting    │ 2185 (96.9%)│ Total consumer review count     │
│ price_quintile               │ Enum      │ Segmentation │ 2256 (100%)│ Q1..Q5 (Right-closed intervals) │
│ editorial_price_tier         │ Enum      │ Segmentation │ 2256 (100%)│ Entry, Budget, Mid, Upper, Prem │
└──────────────────────────────┴───────────┴──────────────┴────────────┴─────────────────────────────────┘
```

> [!CRITICAL]
> **Zero Time Variables in Dataset:** Inspection of the raw scraped dataset (`smartphones_uncleaned.csv`) and processed dataset (`smartphones_cleaned.json`) confirms that **zero temporal fields exist** (no launch dates, release years, scrape timestamps, or listing publication dates). All temporal analysis must be framed within this fundamental limitation (see Section 09).

---

## 04. Cross-Sectional Hedonic Model Strategy

We formulate three primary cross-sectional hedonic regression models to evaluate market-wide specification scaling, semiconductor stratification, and brand positioning.

### Model 1: Baseline Core Hedonic Specification
Evaluates universal component scaling on the near-complete catalog ($N = 2,246$ complete cases, 99.56% of records).
$$\ln(\text{Price}_i) = \beta_0 + \beta_1 \text{RAM}_i + \beta_2 \text{Storage}_i + \beta_3 \left(\frac{\text{Battery}_i}{1000}\right) + \beta_4 \text{ScreenSize}_i + \beta_5 \text{RearMP}_i + \beta_6 \text{RearLenses}_i + \delta_1 \mathbf{1}\{\text{OLED}_i\} + \epsilon_i$$
- **Cluster Variable:** `device_id` (1,647 unique clusters).
- **Standard Errors:** Cluster-robust sandwich variance estimator ($V_{\text{cluster}}$) to account for correlation among variant listings sharing a base model.

### Model 2: Semiconductor Platform Specification
Introduces categorical controls for the primary mobile application processor manufacturer.
$$\ln(\text{Price}_i) = \beta_0 + \mathbf{X}_{i, \text{core}}' \boldsymbol{\beta} + \sum_{m \in \text{SoC}} \gamma_m \mathbf{1}\{\text{SoC\_Manufacturer}_i = m\} + \epsilon_i$$
- **Reference Category:** `MediaTek` ($N = 921$, 40.8% of dataset, representing the dominant volume/value semiconductor baseline in India).
- **Silicon Groups:** Qualcomm ($N = 839$), Samsung Exynos ($N = 156$), Unisoc ($N = 135$), Apple Silicon ($N = 88$), HiSilicon ($N = 24$), and `Other_SoC` ($N = 33$, pooling Intel, Google Tensor, Broadcom, Marvell, ST-Ericsson, Nvidia). Complete-case $N = 2,195$ (97.30% of records).

### Model 3: Full Brand Fixed Effects Specification (Workhorse Model)
Evaluates conditional brand price differentials while holding observable hardware components and semiconductor vendor constant.
$$\ln(\text{Price}_i) = \beta_0 + \mathbf{X}_{i, \text{core}}' \boldsymbol{\beta} + \mathbf{D}_{\text{SoC}, i}' \boldsymbol{\gamma} + \sum_{b \in \text{Brands}} \theta_b \mathbf{1}\{\text{Brand}_i = b\} + \epsilon_i$$
- **Primary Reference Brand:** `Xiaomi` ($N = 41$ listings; see Section 06 for detailed evaluation and sensitivity baselines).
- **Sample:** $N = 2,195$ complete cases across all core specs, SoC, and brand indicators.

---

## 05. Revised Within-Device Model Strategy (Model 4)
### Within-Device Price Association for RAM and Storage Upgrades

> [!WARNING]
> **Strict Descriptive Framing:** Model 4 estimates the **conditional within-device retail price association** for RAM and storage upgrades across manufacturer configurations. It controls for time-invariant base-device attributes, but does not eliminate all omitted-variable bias, isolate pure engineering costs, or establish causal marginal costs of production.

### Clarification of Units of Observation
To avoid confusing distinct statistical concepts, we strictly distinguish three levels of observation:
1. **Configuration-Level Observations ($N = 1,092$):** The primary analytical unit of observation ($ij$), where index $i$ denotes the base device model and index $j$ denotes the specific commercial hardware configuration (e.g., iPhone 13 128GB vs. iPhone 13 256GB).
2. **Device Model Clusters ($G = 483$):** The cluster grouping variable (`device_id`). These represent the multi-variant base models exhibiting more than one configuration ($J_i > 1$).
3. **Pairwise Upgrade Steps ($K = 609$):** The number of incremental configuration steps relative to the lowest-memory base tier ($1,092 - 483 = 609$ degrees of freedom available for within-device variation).  
   *Methodological Mandate:* We do **not** treat the 609 pairwise upgrade steps as equivalent to 1,092 configuration-level observations. The primary estimator runs directly on the $N = 1,092$ configuration-level records using device fixed effects.

### Mathematical Formulation & Handling of Multiple Configurations
$$\ln(\text{Price}_{ij}) = \alpha_i + \beta_{\text{RAM}}^{\text{within}} \text{RAM}_{ij} + \beta_{\text{Storage}}^{\text{within}} \text{Storage}_{ij} + \nu_{ij}$$
where:
- $\alpha_i$ represents the unobserved time-invariant base device fixed effect (chassis metallurgy, display panel, base camera, speaker acoustics, brand prestige).
- Multiple configurations per device ($J_i \in \{2, 3, 4\}$) are handled via the standard **within-transformation (de-meaning)**:
  $$\left(\ln(\text{Price}_{ij}) - \overline{\ln(\text{Price}_i)}\right) = \beta_{\text{RAM}}^{\text{within}} \left(\text{RAM}_{ij} - \overline{\text{RAM}}_i\right) + \beta_{\text{Storage}}^{\text{within}} \left(\text{Storage}_{ij} - \overline{\text{Storage}}_i\right) + \left(\nu_{ij} - \bar{\nu}_i\right)$$
  where $\bar{Z}_i = \frac{1}{J_i} \sum_{j=1}^{J_i} Z_{ij}$ is the device-level mean for variable $Z$.
- **Inference:** Standard errors will be computed using cluster-robust variance estimation clustered at the device level (`device_id`, $G = 483$ clusters) where statistically appropriate, accounting for arbitrary residual correlation $\text{Cov}(\nu_{ij}, \nu_{ik})$ across configurations of the same phone.

### Descriptive Character of Delta Correlation
Across the 609 pairwise upgrade steps, the empirical correlation between memory deltas is $r = -0.092$.
> [!NOTE]
> The reported correlation of $-0.092$ is **descriptive evidence only**. It demonstrates that in this sample, RAM and storage upgrade steps are not mechanically collinear in the aggregate. However, it does **not** independently establish coefficient identification, rank sufficiency, or estimator stability. Identification must be formally verified through pre-estimation diagnostic checks.

### Empirical Variation Patterns Across Multi-Variant Devices ($N = 483$)
Inspection of the 483 multi-variant devices reveals four distinct patterns of variation:
1. **Both RAM and Storage vary simultaneously:** **227 devices** (47.0% of multi-variant sample). In these models, a RAM upgrade is strictly bundled with a storage upgrade (e.g., 6GB/128GB stepping up to 8GB/256GB).
2. **Only RAM varies (Storage held constant):** **121 devices** (25.1% of multi-variant sample). For example, 6GB/128GB stepping up to 8GB/128GB.
3. **Only Storage varies (RAM held constant):** **134 devices** (27.7% of multi-variant sample). For example, 8GB/128GB stepping up to 8GB/256GB.
4. **Neither varies (identical RAM & Storage):** **1 device** (0.2%, Infinix Hot 12 Play, presenting two distinct listings at ₹8,499 and ₹8,999).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              WITHIN-DEVICE MEMORY VARIATION DISTRIBUTION (N = 483)          │
├──────────────────────────────────────────┬──────────────┬───────────────────┤
│ Variation Pattern                        │ Device Count │ Share of Subsample│
├──────────────────────────────────────────┼──────────────┼───────────────────┤
│ Both RAM & Storage Vary Simultaneously   │ 227 devices  │ 47.0%             │
│ Only Storage Varies (RAM Constant)       │ 134 devices  │ 27.7%             │
│ Only RAM Varies (Storage Constant)       │ 121 devices  │ 25.1%             │
│ Neither Varies (Identical Memory Specs)  │ 1 device     │ 0.2%              │
└──────────────────────────────────────────┴──────────────┴───────────────────┘
```

### Mandatory Pre-Estimation Diagnostic Checks
Before estimating separate RAM and storage coefficients, the pipeline must execute the following validation checks:
1. **Within-Device Regressor Variance:** Confirm that de-meaned variances $\text{Var}(\tilde{\text{RAM}}_{ij}) > 0$ and $\text{Var}(\tilde{\text{Storage}}_{ij}) > 0$.
2. **Rank and Condition Number of Within-Design Matrix:** Compute the eigenvalues and condition number $\kappa(\tilde{\mathbf{X}}'\tilde{\mathbf{X}})$ of the de-meaned matrix to verify that the cross-product matrix is strictly non-singular and well-conditioned.
3. **Within-Device Multicollinearity:** Compute the Variance Inflation Factor (VIF) on de-meaned regressors $(\tilde{\text{RAM}}_{ij}, \tilde{\text{Storage}}_{ij})$.
4. **Independent Variation Support:** Verify the presence of the 121 RAM-only and 134 storage-only device clusters to provide off-diagonal support against collinearity.
5. **Hardware Invariance Verification:** Audit configurations for hardware differences beyond memory. Across the 483 multi-variant device clusters ($N = 1,092$ configurations), empirical audit identifies 7 devices (17 configurations) for sensitivity exclusion under approved Option 3:
   - 4 devices feature different processor models across configurations (`asus-zenfone-2-laser-ze550kl`, `asus-zenfone-3-deluxe`, `samsung-galaxy-on-nxt`, `vivo-y91`).
   - 2 devices feature different front camera resolutions (`panasonic-eluga-i2`, `vivo-y91i`).
   - 1 device features a degenerate memory tier with zero RAM and storage variation (`xiaomi-mi-max`, 2 configs, both 3GB/32GB).
   *(Note: 2 devices, `xiaomi-redmi-k20-pro` and `oneplus-7-pro`, feature unstated wattage on one listing rather than conflicting hardware, and are retained under Option 3).*
6. **Sensitivity to Hardware Confounding:** Estimate Model 4 on the full multi-variant sample ($N=483$ devices, 1,092 configurations) and re-estimate on the strictly hardware-invariant subsample ($N = 476$ devices, 1,075 configurations, dropping the 7 excluded devices) to confirm coefficient stability.

### Model 4 Estimation & Fallback Hierarchy

To maintain scientific integrity without improvising ad-hoc composite metrics, Model 4 strictly adheres to a sequential 5-tier estimation and fallback hierarchy:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                         MODEL 4 ESTIMATION & FALLBACK HIERARCHY                        │
├──────┬──────────────────────────────────┬──────────────────────────────────────────────┤
│ Tier │ Procedure / Specification        │ Decision Trigger & Criteria                  │
├──────┼──────────────────────────────────┼──────────────────────────────────────────────┤
│ 1    │ Primary Joint Estimation:        │ Attempt configuration-level within-device    │
│      │ Separate RAM & Storage Regressors│ fixed effects on full multi-variant sample   │
│      │ on N = 1,092 configs (G = 483).  │ (N=1,092, G=483), subject to pre-estimation  │
│      │                                  │ diagnostics (VIF < 5.0, matrix rank/cond).   │
├──────┼──────────────────────────────────┼──────────────────────────────────────────────┤
│ 2    │ Restricted RAM-Only Subsample    │ Triggered if joint estimation shows severe   │
│      │ (Sub-Model 4A):                  │ multicollinearity or rank instability.       │
│      │ Storage held strictly constant.  │ Evaluates N = 251 configs across G = 121     │
│      │                                  │ devices where RAM varies and Storage is fixed│
├──────┼──────────────────────────────────┼──────────────────────────────────────────────┤
│ 3    │ Restricted Storage-Only Subsample│ Triggered in parallel with Tier 2.           │
│      │ (Sub-Model 4B):                  │ Evaluates N = 296 configs across G = 134     │
│      │ RAM held strictly constant.      │ devices where Storage varies and RAM is fixed│
├──────┼──────────────────────────────────┼──────────────────────────────────────────────┤
│ 4    │ Disclose Restricted Diagnostics: │ Report observation count, cluster count, and │
│      │ Full transparency on sample      │ structural limitations for each restricted   │
│      │ scope and external validity.     │ subsample (Sub-Models 4A and 4B).            │
├──────┼──────────────────────────────────┼──────────────────────────────────────────────┤
│ 5    │ Explicit Reporting of Data       │ If separate RAM and storage associations     │
│      │ Insufficiency:                   │ cannot be established reliably across Tiers  │
│      │ No arbitrary metric creation.    │ 1–3, explicitly report that the dataset does │
│      │                                  │ not support reliable separate estimates.     │
└──────┴──────────────────────────────────┴──────────────────────────────────────────────┘
```

1. **Tier 1 — Primary Joint Estimation (Separate RAM & Storage):**  
   Attempt configuration-level within-device fixed effects with separate RAM and storage regressors on the full multi-variant sample ($N = 1,092$ configurations across $G = 483$ device clusters), subject to passing all pre-estimation diagnostics (positive regressor variance, matrix full rank, condition number $\kappa(\tilde{\mathbf{X}}'\tilde{\mathbf{X}})$, and $\text{VIF} < 5.0$).
2. **Tier 2 — Restricted RAM-Only Subsample (Sub-Model 4A):**  
   If joint estimation is statistically unstable or design matrix ill-conditioning arises, evaluate RAM upgrades exclusively within the subset of devices where internal storage remains strictly constant:
   $$\left(\ln(\text{Price}_{ij}) - \overline{\ln(\text{Price}_i)}\right) = \beta_{\text{RAM}}^{\text{pure}} \left(\text{RAM}_{ij} - \overline{\text{RAM}}_i\right) + \tilde{\nu}_{ij}$$
   - *Sample Scope:* Exactly **$N = 251$ configurations across $G = 121$ device clusters**.
3. **Tier 3 — Restricted Storage-Only Subsample (Sub-Model 4B):**  
   Evaluate storage upgrades exclusively within the subset of devices where RAM capacity remains strictly constant:
   $$\left(\ln(\text{Price}_{ij}) - \overline{\ln(\text{Price}_i)}\right) = \beta_{\text{Storage}}^{\text{pure}} \left(\text{Storage}_{ij} - \overline{\text{Storage}}_i\right) + \tilde{\nu}_{ij}$$
   - *Sample Scope:* Exactly **$N = 296$ configurations across $G = 134$ device clusters**.
4. **Tier 4 — Comprehensive Subsample Reporting:**  
   If reporting restricted models from Tiers 2 and 3, report each restricted sample's exact observation count, device-cluster count, and substantive limitations:
   - *Limitation:* Restricting to single-spec variation filters out the 227 devices (comprising 543 configurations, 47.0% of multi-variant sample) that bundle RAM and storage upgrades simultaneously, shifting the sample composition toward specific brands or price tiers.
5. **Tier 5 — Explicit Disclosure of Dataset Non-Identification:**  
   If reliable separate associations cannot be established across Tiers 1–3, the research pipeline will **explicitly report that the available observational dataset does not support reliable separate within-device RAM and storage estimates**, rather than constructing an arbitrary composite metric.

> [!IMPORTANT]
> **Prohibition of Composite Memory Indices:** The automatic creation of a "Combined Memory Tier Index" is strictly removed. Any composite memory index or metric aggregation may only be considered in a separately approved future methodology proposal accompanied by explicit formal construction, weighting justification, and mathematical validation.

---

## 06. Brand Taxonomy and Aggregation Methodology

### Preservation of Consumer-Facing Brand Identity (Phase 03 Compliance)
Phase 03 established that consumer-facing brand names represent distinct commercial identities in the Indian marketplace. In accordance with project governance:
- **Zero Merging of Xiaomi and Redmi:** Xiaomi and Redmi remain strictly separate categorical variables. Xiaomi represents higher-tier mid-to-premium offerings (e.g., Xiaomi 11, Xiaomi 12 Pro, Xiaomi 14), while Redmi represents high-volume budget and value devices (e.g., Redmi 9A, Redmi Note 12).
- **Verified Listing Counts:** In the cleaned dataset:
  - `Xiaomi`: Exactly **41 listings** (mean price: ₹33,829; median price: ₹29,999).
  - `Redmi`: Exactly **153 listings** (mean price: ₹13,446; median price: ₹11,999).
  - `Samsung`: Exactly **312 listings** (mean price: ₹27,824; median price: ₹16,999).
  - `Realme`: Exactly **210 listings** (mean price: ₹16,959; median price: ₹14,999).
  - `Vivo`: Exactly **195 listings** (mean price: ₹20,111; median price: ₹16,990).
  - `Apple`: Exactly **88 listings** (mean price: ₹77,597; median price: ₹68,499).

### Reference Category Evaluation (Provisionally Accepted Baseline)
To avoid the dummy variable trap, one brand must be omitted as the baseline reference category ($\theta_{\text{ref}} = 0$):
1. **Provisionally Accepted Baseline: `Xiaomi` ($N = 41$):**
   - *Rationale:* Xiaomi operates in the middle of the smartphone market (median price ₹29,999), offering sufficient sample size ($N = 41 > 30$) while providing an intuitive editorial benchmark: positive coefficients represent brands priced above Xiaomi holding specs constant; negative coefficients represent brands priced below Xiaomi.
2. **Alternative Baseline A: `Redmi` ($N = 153$):**
   - *Rationale:* As the high-volume entry/budget baseline (median price ₹11,999), choosing Redmi makes almost all major brand coefficients positive, representing premiums relative to a pure value brand.
3. **Alternative Baseline B: `Samsung` ($N = 312$):**
   - *Rationale:* Largest sample size in the catalog, providing the lowest standard error for the intercept.
4. **Alternative Baseline C: Weighted Market Mean (Deviation Coding):**
   - *Rationale:* Transforms coefficients so that $\theta_b$ represents deviation from the average catalog price rather than deviation from an arbitrary single brand.

### Interpretation of Brand Coefficients
The coefficient $\theta_b$ measures the **conditional percentage difference in listed retail price** between brand $b$ and the reference brand for devices with identical observable core specifications and semiconductor vendors.
> [!IMPORTANT]
> A positive brand coefficient ($\hat{\theta}_b > 0$) must **never** be cited in public editorial copy as a "pure brand tax" or "irrational consumer markup." It represents the conditional price differential attributable to both brand equity **and all unobserved product attributes correlated with that brand** (proprietary OS software, industrial chassis metallurgy, IP water resistance certifications, optical image stabilization engineering, thermal dissipation chambers, and post-sales service networks).

### Niche Brand Aggregation Thresholds (Provisionally Accepted at $\ge 20$)
The dataset contains **63 unique brand names**. Estimating separate coefficients for brands with only 1 or 2 listings produces extreme standard errors and incidental parameter distortion.

Thresholding is a researcher-defined modeling choice. We evaluate three explicit cutoffs:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        BRAND AGGREGATION THRESHOLD SENSITIVITY                         │
├───────────┬──────────────┬──────────────────┬──────────────┬───────────────────────────┤
│ Threshold │ Major Brands │ Records Covered  │ Niche Brands │ Niche Records Pooled (%)  │
├───────────┼──────────────┼──────────────────┼──────────────┼───────────────────────────┤
│ $\ge 10$  │ 33 brands    │ 2,170 records    │ 30 brands    │ 86 records (3.81%)        │
│ $\ge 20$  │ 29 brands    │ 2,120 records    │ 34 brands    │ 136 records (6.03%)       │
│ $\ge 30$  │ 23 brands    │ 1,982 records    │ 40 brands    │ 274 records (12.15%)      │
└───────────┴──────────────┴──────────────────┴──────────────┴───────────────────────────┘
```

- **Provisionally Accepted Primary Cutoff: $\ge 20$ listings:** 29 major brands covering 93.97% of records; 34 niche brands pooled into `Niche_Other`.
- **Reporting Rule on `Niche_Other`:** The pooled indicator `Niche_Other` is a mathematical modeling convenience to absorb long-tail variance. It must **never** be presented in charts, rankings, or public copy as if it were a real consumer-facing brand.
- **Mandatory Sensitivity Check:** Models will be re-estimated at thresholds of 10 and 30 listings to confirm that major brand coefficients remain stable regardless of aggregation cutoff.

---

## 07. Functional-Form Comparison: Linear INR vs. Log-Price

Rather than asserting that log-price is "econometrically mandatory," we evaluate log-price as the **primary candidate specification**, subject to direct empirical diagnostic testing against a linear price specification.

### Trade-Off Analysis Matrix

```
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│                           LINEAR PRICE (INR) VS. LOG-PRICE (LN(INR))                           │
├──────────────────────┬────────────────────────────────────┬────────────────────────────────────┤
│ Dimension            │ Linear Scale: Price = Xβ + ε       │ Semi-Log Scale: ln(Price) = Xβ + ε │
├──────────────────────┼────────────────────────────────────┼────────────────────────────────────┤
│ Economic Meaning     │ Constant absolute rupee markup     │ Proportional percentage markup     │
│                      │ (e.g., +₹1,500 per GB RAM)         │ (e.g., +8% price increase per GB)  │
├──────────────────────┼────────────────────────────────────┼────────────────────────────────────┤
│ High-Priced Outliers │ Extreme leverage from luxury phones│ Compresses luxury phone prices;    │
│                      │ (₹150,000+ flagships distort slope)│ reduces leverage of right tail     │
├──────────────────────┼────────────────────────────────────┼────────────────────────────────────┤
│ Error Variance       │ Severe heteroskedasticity; residual│ Substantially stabilizes residual  │
│                      │ spread scales with price level     │ variance across price tiers        │
├──────────────────────┼────────────────────────────────────┼────────────────────────────────────┤
│ Residual Behavior    │ Severe right skewness (skew = 3.36,│ Near-Gaussian symmetry             │
│                      │ kurt = 14.05); violates OLS norms  │ (skew = 0.80, kurt = 0.31)         │
├──────────────────────┼────────────────────────────────────┼────────────────────────────────────┤
│ Non-Negativity       │ Can predict negative prices for low│ Guarantees strictly positive       │
│                      │ spec combinations (Price < 0)      │ predicted prices: Price = exp(ŷ)   │
└──────────────────────┴────────────────────────────────────┴────────────────────────────────────┘
```

### Exact Mathematical Interpretation of Coefficients
In a semi-log model $\ln(\text{Price}) = \beta_0 + \beta_1 X + \epsilon$:
1. **Exact Percentage Effect:** A 1-unit increase in regressor $X$ is associated with an exact percentage change in price of:
   $$\% \Delta \text{Price} = 100 \times \left( \exp(\beta_1) - 1 \right)\%$$
2. **Small-Coefficient Approximation:** When $|\beta_1| < 0.10$, the Taylor series approximation $\exp(\beta_1) - 1 \approx \beta_1$ applies, meaning:
   $$\% \Delta \text{Price} \approx 100 \times \beta_1\%$$
   *Reporting Standard:* The analytical pipeline will compute and report **both** the exact percentage markup and the linear coefficient, explicitly noting when the approximation diverges (e.g., $\beta = 0.40 \implies \text{approx } +40\% \text{ vs exact } +49.18\%$).

### Exploratory Role and Limitations of Box-Cox
The Box-Cox power transformation will be evaluated as an **exploratory descriptive guide**, not as an automatic decision rule:
- **Purpose:** Identifies the power parameter $\lambda$ that maximizes the profile log-likelihood for $\text{Price}^{(\lambda)}$.
- **Limitations:** The Box-Cox procedure assumes that transformed disturbances are homoskedastic and normally distributed. In observational hedonic data with clustering and heteroskedasticity, these assumptions are routinely violated, causing the estimated $\lambda$ to be sensitive to outliers.
- **Decision Principle:** Functional form selection will be justified on the basis of economic interpretability, outlier robustness, and residual heteroskedasticity rather than mechanical adherence to $\hat{\lambda}_{\text{Box-Cox}}$.

---

## 08. Quantile Regression Exploratory Framework (Model 6)

> [!NOTE]
> Model 6 is classified as an **exploratory extension**, not a mandatory core workhorse model.

### Additional Research Purpose
While stratified OLS models (Section 12) evaluate specification returns within pre-defined discrete editorial price tiers, **Quantile Regression (Koenker & Bassett, 1978)** models the conditional distribution of prices continuously. It answers:
$$\textbf{"Do returns to RAM, storage, and semiconductor platforms differ at the 10th percentile (entry budget), 50th percentile (median), and 90th percentile (luxury flagship) of the conditional market distribution?"}$$

### Mathematical Formulation
$$\min_{\boldsymbol{\beta}(\tau)} \sum_{i=1}^N \rho_\tau \left( \ln(\text{Price}_i) - \mathbf{Z}_i' \boldsymbol{\beta}(\tau) \right)$$
where $\rho_\tau(u) = u (\tau - \mathbf{1}\{u < 0\})$ is the check loss function, evaluated at $\tau \in \{0.10, 0.25, 0.50, 0.75, 0.90\}$.

### Methodological Limitations & Clustered Inference Warning
1. **Clustering Challenge in Quantile Regression:** Unlike linear OLS, where cluster-robust Huber-White sandwich estimators are standard and well-behaved, quantile regression with clustered data (`device_id`, $G = 1,647$) is econometrically challenging. Standard asymptotic formulas assume independent observations. Block-bootstrapping on clusters often suffers from non-convergence or singularity when sparse categorical dummies (such as niche brands or rare SoCs) are included.
2. **Feature Variation Requirements:** At extreme quantiles ($\tau = 0.10$ or $\tau = 0.90$), cells for low-frequency brands can become degenerate (zero variation).
3. **Governance Mandate:** If cluster-bootstrapped standard errors cannot achieve stable convergence in Model 6, **we will explicitly document this limitation** and report Model 6 with asymptotic or non-clustered bootstrap standard errors accompanied by a prominent research caveat, rather than claiming cluster-robust inference was achieved.

---

## 09. Temporal Confounding and Selection Bias

### 9.1 Temporal Confounding (The Unobserved Era Problem)
The empirical dataset spans devices released from approximately **2011 through mid-2024**. Over this 13-year period, mobile technology experienced massive deflationary and architectural shifts:
- A ₹20,000 retail price in 2013 purchased a top-tier flagship with 2GB of RAM and a single 13MP camera.
- A ₹20,000 retail price in 2024 purchases a mid-range phone with 8GB of RAM, a 50MP OIS camera, and 120Hz AMOLED display.

> [!CAUTION]
> **Defensible Time Variables Absent:** Inspection of both raw and processed datasets confirms that **zero time-related variables exist** (no launch year, announcement date, or listing timestamp). Therefore:
> - **Temporal confounding cannot be controlled via time fixed effects or time-trend variables.**
> - Cross-sectional spec coefficients will partially absorb historical specification inflation (e.g., higher RAM is associated with modern devices which may also have different market pricing dynamics).
> - This structural limitation must be prominently stated in all methodology reports and editorial chapters.

### 9.2 Selection Bias & Population of Generalization
1. **Catalog Aggregation, Not Random Sampling:** The 2,256 records represent smartphones cataloged by the Indian aggregator *MySmartPrice* that remained live and scrapeable in mid-2024. Obscure models from 2012 that were delisted before scraping are omitted.
2. **Catalog Offerings vs. Sales Volumes:** The dataset reflects the **menu of available retail choices** in the Indian market, not the units adopted by consumers. A popular phone selling 10 million units appears as 1 to 3 listing records; an obscure phone selling 500 units also appears as 1 listing record.
3. **Target Population Definition:** All findings generalize strictly to:
   $$\textbf{"The population of consumer smartphone configurations cataloged for online retail purchase in India between 2011 and mid-2024."}$$
   Findings must **not** be extrapolated as global MSRP benchmarks, manufacturing cost curves, or consumer sales shares.

---

## 10. Missing-Data and Subsample Governance (Model 5)

### Systematic Missingness Analysis
In accordance with project governance, **zero missing values will be imputed**. 

Inspection of missingness across variables reveals a stark divide:
- **Core Hardware Specifications:** Nearly 100% complete across the catalog (RAM 99.6%, Storage 99.9%, Battery 100%, Screen Size 100%, Cameras 98.6%–100%, SoC Vendor 97.3%).
- **Extended Modern Specifications:** Exhibit substantial missingness:
  - `charging_wattage`: Missing in **935 records (41.45%)**.
  - `refresh_rate_hz`: Missing in **1,123 records (49.78%)**.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     MISSINGNESS MECHANISM CLASSIFICATION                    │
├─────────────────────┬──────────────┬──────────────────┬─────────────────────┤
│ Variable            │ Missing N (%)│ Missingness Type │ Nature of Mechanism │
├─────────────────────┼──────────────┼──────────────────┼─────────────────────┤
│ ram_capacity_gb     │ 8 (0.35%)    │ Low-Frequency    │ Parser drop         │
│ storage_capacity_gb │ 2 (0.09%)    │ Low-Frequency    │ Parser drop         │
│ display_panel_family│ 2 (0.09%)    │ Low-Frequency    │ Unstated panel type │
│ processor_mfg       │ 60 (2.66%)   │ Low-Frequency    │ Unbranded budget SoC│
├─────────────────────┼──────────────┼──────────────────┼─────────────────────┤
│ charging_wattage    │ 935 (41.45%) │ Potentially Syst.│ Missingness cannot  │
│ refresh_rate_hz     │ 1123 (49.78%)│ Potentially Syst.│ be conclusively     │
│                     │              │                  │ identified as MAR   │
│                     │              │                  │ vs. MNAR from data  │
└─────────────────────┴──────────────┴──────────────────┴─────────────────────┘
```

> [!IMPORTANT]
> **Defensible Missingness Classification:** While domain knowledge indicates that 60Hz panels and 5W–10W USB charging were ubiquitous default baselines prior to 2019 that spec sheets omitted, **the formal missingness mechanism cannot be conclusively identified as MAR or MNAR from the available observed variables alone**. Testing MAR vs. MNAR requires unobserved counterfactuals. Therefore, we classify missingness as **potentially systematic**, and evaluate it directly by comparing missingness patterns across observed variables.

### Missingness Comparisons Across Observed Variables
To evaluate the extent of sample selection, the pipeline will compare records with complete vs. missing modern features across:
- **Price:** Median price of complete records (₹18,996) is **+31.0% higher** than the full catalog (₹14,499).
- **RAM Capacity:** Mean RAM of complete records (7.38 GB) is **+41.9% higher** than full catalog (5.20 GB).
- **Storage Capacity:** Mean Storage of complete records (176.9 GB) is **+56.0% higher** than full catalog (113.4 GB).
- **Editorial Price Tier:** Entry-level tier share collapses from 32.2% in full catalog down to 14.8% in complete records; mid-range and premium shares expand substantially.
- **Brand Distribution:** Major modern brands (Realme, OnePlus, iQOO, Xiaomi) exhibit high reporting rates (>80%), while legacy brands (Micromax, Karbonn, Panasonic) exhibit near-zero reporting rates.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               FULL CATALOG VS. MODEL 5 MODERN FEATURE SUBSAMPLE                        │
├──────────────────────────────┬────────────────────┬────────────────────┬───────────────┤
│ Metric                       │ Full Catalog       │ Model 5 Subsample  │ Shift / Skew  │
├──────────────────────────────┼────────────────────┼────────────────────┼───────────────┤
│ Record Count                 │ 2,256 (100.0%)     │ 1,101 (48.80%)     │ -51.2% sample │
│ Median Listed Price          │ ₹14,499            │ ₹18,996            │ +31.0% higher │
│ Mean Listed Price            │ ₹22,211            │ ₹28,583            │ +28.7% higher │
│ Mean RAM Capacity            │ 5.20 GB            │ 7.38 GB            │ +41.9% higher │
│ Mean Storage Capacity        │ 113.4 GB           │ 176.9 GB           │ +56.0% higher │
├──────────────────────────────┼────────────────────┼────────────────────┼───────────────┤
│ Entry-Level Tier (<₹10k)     │ 32.2% of catalog   │ 14.8% of sample    │ -17.4% drop   │
│ Budget-to-Mid Tier (₹10k-20k)│ 35.7% of catalog   │ 39.7% of sample    │ +4.0% share   │
│ Mid-Range Tier (₹20k-35k)    │ 17.5% of catalog   │ 24.6% of sample    │ +7.1% share   │
│ Upper-Mid Tier (₹35k-60k)    │ 8.7% of catalog    │ 11.8% of sample    │ +3.1% share   │
│ Premium Tier (≥₹60k)         │ 5.9% of catalog    │ 9.1% of sample     │ +3.2% share   │
└──────────────────────────────┴────────────────────┴────────────────────┴───────────────┘
```

### Subsample Governance Protocol (Provisionally Accepted)
1. **Core Models 1–3 Exclude Charging & Refresh:** Models 1, 2, and 3 will strictly exclude `charging_wattage` and `refresh_rate_hz` to maintain sample completeness ($N = 2,246$ to $2,195$, $>97\%$ of catalog).
2. **Model 5 Restricted to Modern Feature Cohort:** Model 5 will be estimated on the $N = 1,101$ subsample and explicitly documented as a **Restricted Modern Feature Cohort Specification**.
3. **Mandatory Generalization Caveat:** Model 5 results cannot be generalized to the complete 2011–2024 catalog. The report must present the sample composition shifts shown above alongside regression coefficients.

---

## 11. Statistical Diagnostics and Validation Plan

### Reorganized Diagnostic Hierarchy
To maintain econometric rigor, the statistical validation protocol separates assumptions required for **unbiased/consistent coefficient estimation** from assumptions required for **conventional statistical inference**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                       STATISTICAL DIAGNOSTIC HIERARCHY                                 │
├──────┬─────────────────────────┬───────────────────────────┬───────────────────────────┤
│ Rank │ Diagnostic Domain       │ Primary Empirical Test    │ Evaluation Standard       │
├──────┼─────────────────────────┼───────────────────────────┼───────────────────────────┤
│ 1    │ Functional Form &       │ Ramsey RESET Test,        │ Detects unmodeled         │
│      │ Residual Patterns       │ Component-Plus-Residual   │ non-linearities           │
├──────┼─────────────────────────┼───────────────────────────┼───────────────────────────┤
│ 2    │ Heteroskedasticity      │ Breusch-Pagan Test,       │ Mandates cluster-robust   │
│      │                         │ White Test                │ Huber-White SEs (p < 0.05)│
├──────┼─────────────────────────┼───────────────────────────┼───────────────────────────┤
│ 3    │ Multicollinearity       │ Variance Inflation Factor │ VIF > 5.0 (Review)        │
│      │                         │ (VIF) on continuous specs │ VIF > 10.0 (Remediate)    │
├──────┼─────────────────────────┼───────────────────────────┼───────────────────────────┤
│ 4    │ Influential Observations│ Cook's Distance ($D_i$),  │ $D_i > 4/N \approx 0.0018$│
│      │ & Leverage              │ DFBETAS                   │ Profile sensitivity       │
├──────┼─────────────────────────┼───────────────────────────┼───────────────────────────┤
│ 5    │ Cluster Dependence      │ Intra-class correlation   │ Confirms necessity of     │
│      │                         │ on device_id              │ cluster sandwich variance │
├──────┼─────────────────────────┼───────────────────────────┼───────────────────────────┤
│ 6    │ Specification           │ Subsample stability,      │ Evaluates coefficient     │
│      │ Sensitivity             │ Outlier truncation        │ invariance across forms   │
├──────┼─────────────────────────┼───────────────────────────┼───────────────────────────┤
│ Opt  │ Descriptive Normality   │ Jarque-Bera Test,         │ Descriptive only; NOT a   │
│      │                         │ Q-Q Residual Plot         │ pass/fail OLS requirement │
└──────┴─────────────────────────┴───────────────────────────┴───────────────────────────┘
```

### Critical Distinction: Estimation vs. Inference Regularity Conditions

To ensure statistical rigor, we explicitly distinguish the conditions required for calculating OLS point estimates from the regularity conditions required for valid large-sample statistical inference:

1. **Assumptions for OLS Coefficient Point Estimation:**
   - **Computational Feasibility:** Point estimates $\hat{\boldsymbol{\beta}} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$ require only that the sample design matrix $\mathbf{X}$ has full column rank ($\text{rank}(\mathbf{X}) = K$).
   - **Unbiasedness / Consistency:** Requires conditional mean exogeneity ($E[\epsilon_i \mid \mathbf{X}_i] = 0$) and suitable probability limits ($\frac{1}{N}\mathbf{X}'\mathbf{X} \xrightarrow{p} \mathbf{Q}_{xx}$, where $\mathbf{Q}_{xx}$ is finite and positive definite).
   - **Absence of Normality Requirement:** **Residual normality is not a general requirement for calculating OLS coefficient point estimates or for estimator consistency.** Point estimates remain mechanically computable and consistent under non-normal disturbances provided moment and exogeneity conditions hold.

2. **Regularity Conditions for Large-Sample Asymptotic Inference:**
   - **Asymptotic Normality is Not Automatic:** Asymptotic normality of $\sqrt{N}(\hat{\boldsymbol{\beta}} - \boldsymbol{\beta})$ does not hold unconditionally; it requires explicit regularity conditions:
     - *Exogeneity & Orthogonality:* $E[\mathbf{x}_i \epsilon_i] = \mathbf{0}$.
     - *Finite Moment Conditions:* Finite fourth moments of regressors ($E[X_{ik}^4] < \infty$) and disturbances ($E[\epsilon_i^4] < \infty$) to ensure consistent covariance matrix estimation.
     - *Regressor Matrix Regularity:* $\frac{1}{N} \sum_{i=1}^N \mathbf{x}_i \mathbf{x}_i'$ converges in probability to a strictly positive definite matrix $\mathbf{Q}_{xx}$.
     - *Appropriate Dependence Structure:* Standard asymptotic normality relies on independent (or weakly dependent) observations. When observations are clustered within groups, standard independently and identically distributed (i.i.d.) central limit theorems break down.

3. **Cluster Dependence & Regularity in Cluster-Robust Inference:**
   - **Within-Cluster Dependence:** In our dataset, repeated configurations sharing a base `device_id` create within-cluster error correlation ($\text{Cov}(\epsilon_{ij}, \epsilon_{ik} \mid \mathbf{X}) \ne 0$).
   - **Cluster-Level Regularity Conditions:** Cluster-robust inference (via the Liang-Zeger sandwich estimator $\mathbf{V}_{\text{cluster}}$) requires cluster-level asymptotics:
     - The number of independent clusters $G$ must grow large ($G \to \infty$).
     - Cluster sizes must remain bounded relative to total sample size ($\max_g N_g / N \to 0$).
     - Cluster-level moment bounds must be satisfied: $E[\|\mathbf{X}_g' \boldsymbol{\epsilon}_g\|^2] < \infty$.
   - **Disclosure of Cluster Dimensions:**
     - In the cross-sectional catalog (Models 1–3): Exactly **$G = 1,647$ clusters** across $N = 2,256$ listings.
     - In the multi-variant subsample (Model 4): Exactly **$G = 483$ clusters** across $N = 1,092$ listings.
     - Cluster size distribution: 1,164 clusters with size 1, 362 clusters with size 2, 116 clusters with size 3, and 5 clusters with size 4 (maximum cluster size $N_g = 4 \ll N$).
   - **Cluster-Robust SEs Are Not Automatically Valid:** Cluster-robust standard errors are not automatically valid simply because they are requested. When clusters are unbalanced, when influential high-leverage clusters exist, or when sparse dummy indicators isolate specific clusters, sandwich variance estimators can exhibit finite-sample downward bias. These properties will be scrutinized in diagnostics.

4. **Descriptive Role of Normality Diagnostics:**
   - **Jarque-Bera and Q-Q plots remain optional descriptive diagnostics**, not universal pass/fail criteria for OLS validity.
   - Rejection of the Jarque-Bera null hypothesis of normality reflects the non-Gaussian nature of pricing distributions, but does not invalidate large-sample OLS inference under cluster-robust asymptotics when the cluster regularity conditions above are satisfied.

---

## 12. Robustness and Sensitivity Analysis

To guarantee that findings are robust and not artifacts of arbitrary modeling choices, six sensitivity checks will be executed:

1. **Functional-Form Sensitivity:** Re-estimate models using linear INR prices, polynomial specifications ($\text{RAM}^2$, $\text{Storage}^2$), and log-log specifications ($\ln(\text{RAM})$, $\ln(\text{Storage})$).
2. **Brand Aggregation Cutoff Sensitivity:** Re-estimate Model 3 under three distinct brand thresholds:
   - Threshold $\ge 10$ listings (33 major brands).
   - Threshold $\ge 20$ listings (29 major brands; provisionally accepted baseline).
   - Threshold $\ge 30$ listings (23 major brands).
3. **Reference Category Sensitivity:** Re-estimate Model 3 varying the omitted reference brand across `Xiaomi` ($N = 41$), `Redmi` ($N = 153$), `Samsung` ($N = 312$), and a weighted market grand mean.
4. **Subsample Selection Robustness:** Fit Model 3 exclusively on the Model 5 subsample ($N = 1,101$) to isolate the impact of sample truncation from the addition of charging and refresh variables.
5. **Within-Device Specification Contrast:** Compare the joint within-device memory model (Model 4) against single-spec isolated upgrade models (Sub-Model 4A for storage-only devices; Sub-Model 4B for RAM-only devices) and the hardware-invariant subsample ($N=476$ devices, 1,075 configurations).
6. **Outlier Truncation:** Re-estimate all core models trimming the top 1% and bottom 1% of prices ($₹5,324 < \text{Price} < ₹138,675$).

---

## 13. Practical Interpretation Guidelines

To prevent misinterpretation in editorial copy, the following guidelines and exact mathematical formulas must be adhered to:

### Example A: Continuous Variable in Semi-Log Model (RAM)
Suppose the estimated coefficient on `ram_capacity_gb` is $\hat{\beta}_{\text{RAM}} = 0.082$.
- **Exact Interpretation:** Holding all other observable hardware specifications, silicon vendor, and brand constant, each additional gigabyte of RAM is associated with an exact price increase of:
  $$100 \times \left( \exp(0.082) - 1 \right)\% = +8.55\%$$
- **Linear Approximation:** $100 \times 0.082\% \approx +8.20\%$. (Acceptable for brief callouts, but exact figure reported in technical footnotes).
- **Prohibited Editorial Claim:** *"Adding 1GB of RAM costs the manufacturer 8.5% more to build."* (Conflates market retail pricing with manufacturing cost).

### Example B: Categorical Dummy Variable (OLED Panel)
Suppose the estimated coefficient on $\mathbf{1}\{\text{OLED}\}$ is $\hat{\delta}_{\text{OLED}} = 0.245$.
- **Exact Interpretation:** Holding all other specifications and brand constant, devices equipped with OLED display panels are listed at prices:
  $$100 \times \left( \exp(0.245) - 1 \right)\% = +27.76\% \text{ higher than comparable LCD devices}$$
- **Prohibited Editorial Claim:** *"OLED screens add a ₹5,000 premium to every phone."* (Absolute rupee markup varies with device price level; percentage is relative).

### Example C: Brand Fixed Effect Relative to Reference Brand
Suppose `Xiaomi` is the reference category ($\theta_{\text{Xiaomi}} = 0$) and the estimated coefficient for `Apple` is $\hat{\theta}_{\text{Apple}} = 0.620$.
- **Exact Interpretation:** Holding observable RAM, storage, battery, display, camera specs, and silicon vendor constant, Apple devices are listed at prices approximately:
  $$100 \times \left( \exp(0.620) - 1 \right)\% = +85.89\% \text{ higher than comparable Xiaomi devices}$$
- **Permissible Editorial Copy:** *"Holding observable spec sheets constant, Apple commands an estimated conditional price differential of +85.9% relative to Xiaomi. This differential reflects both brand equity and unobserved engineering factors such as iOS optimization, industrial materials, and post-sales support."*
- **Prohibited Editorial Claim:** *"Apple charges an 85.9% irrational brand tax for the exact same phone."*

### Example D: Within-Device Upgrade Markup (Model 4)
Suppose the within-device storage coefficient is $\hat{\beta}_{\text{within\_storage}} = 0.00185$ per GB (equivalent to $+23.68\%$ for a 128GB step).
- **Exact Interpretation:** Across configurations of the identical smartphone model chassis, upgrading internal storage by 128GB is associated with an average retail price increase of $+23.7\%$.
- **Permissible Editorial Copy:** *"Within identical device models, stepping from 128GB to 256GB of storage is associated with an average retail price increase of 23.7%, reflecting OEM tier pricing strategies."*
- **Prohibited Editorial Claim:** *"NAND flash costs the OEM 23.7% of the phone's price."*

> [!NOTE]
> All numerical coefficients in Examples A–D above are **[HYPOTHETICAL ILLUSTRATIONS FOR GUIDELINE DEMONSTRATION ONLY — NOT EMPIRICAL RESULTS]**. Actual empirical values will be determined during Phase 04 Stage 04 modeling.

---

## 14. Research Limitations & Explicit Boundaries

1. **Observational Cross-Section:** All regression models estimate conditional equilibrium correlations in a web-scraped retail catalog, not causal engineering determinants.
2. **Geographic Specificity (Indian Market):** All prices originate from the Indian retail smartphone market in Indian Rupees (INR, ₹), incorporating 18% Goods and Services Tax (GST) and Indian import tariffs on electronic sub-assemblies. Converted figures must not be presented as US or European MSRPs.
3. **Temporal Confounding (Unobserved Dates):** Because launch dates and scrape timestamps are unrecorded, models cannot control for time trends or historical spec inflation across the 2011–2024 era.
4. **Catalog Listings vs. Consumer Sales:** The dataset represents available retail options, not sales volume or market share.
5. **Omitted Physical & Software Attributes:** Key determinants of smartphone user experience—such as optical image stabilization (OIS), display color calibration ($\Delta E$), peak outdoor nit brightness, haptic motor quality, thermal dissipation vapor chambers, and long-term software support—are unrecorded in basic spec sheets.
6. **External Ownership Benchmarks Separation:** In accordance with Decision **H05**, longitudinal metrics (software update lifecycles, iFixit repairability scores, battery degradation curves, and TCO amortizations) are maintained in a dedicated external ledger (`Data/processed/external_ownership_benchmarks.json`) and must never be conflated with directly measured dataset variables.

---

## 15. Methodological Decision Status & Approval Log

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        METHODOLOGICAL DECISION STATUS MATRIX                           │
├────┬──────────────────────────────────┬───────────────────────────┬────────────────────┤
│ ID │ Decision Topic                   │ Resolved Framework        │ Status             │
├────┼──────────────────────────────────┼───────────────────────────┼────────────────────┤
│ D1 │ Reference Brand Selection        │ Xiaomi (N=41) baseline;   │ APPROVED           │
│    │                                  │ Redmi (N=153) separate;   │                    │
│    │                                  │ Samsung/Mean sensitivity  │                    │
├────┼──────────────────────────────────┼───────────────────────────┼────────────────────┤
│ D2 │ Niche Brand Aggregation Cutoff   │ Primary cutoff at ≥20;    │ APPROVED           │
│    │ Threshold                        │ Sensitivity at 10 and 30  │                    │
├────┼──────────────────────────────────┼───────────────────────────┼────────────────────┤
│ D3 │ Missing Data & Model 5 Strategy  │ Core Models 1-3 omit fast │ APPROVED           │
│    │                                  │ charge & Hz; Model 5 acts │                    │
│    │                                  │ as modern cohort subsample│                    │
├────┼──────────────────────────────────┼───────────────────────────┼────────────────────┤
│ D4 │ Model 4 Hardware-Invariance      │ Option 3: Exclude 7 devs  │ APPROVED           │
│    │ Sensitivity Subsample            │ (6 hardware + 1 degen mem)│                    │
│    │                                  │ -> 476 clusters / 1,075 cfg│                   │
├────┼──────────────────────────────────┼───────────────────────────┼────────────────────┤
│ D5 │ Dual Public Editorial Strategy   │ Feature Model 3 for market│ NOT YET APPROVED   │
│    │                                  │ spread & Model 4 for within-│ (Pending Stage 04│
│    │                                  │ device memory pricing     │  diagnostics)      │
└────┴──────────────────────────────────┴───────────────────────────┴────────────────────┘
```

### Formal Review Decisions Approved by Project Owner:
1. **Decision D1 — Reference Brand Selection:**
   - *Status:* **APPROVED** by Project Owner.
   - *Framework:* Xiaomi ($N=41$) serves as reference category. Redmi ($N=153$) is preserved as a distinct brand. Sensitivity analyses with Redmi, Samsung ($N=312$), and market mean are pre-specified.
2. **Decision D2 — Niche Brand Aggregation Threshold:**
   - *Status:* **APPROVED** by Project Owner.
   - *Framework:* Aggregation cutoff set to $\ge 20$ listings (29 major brands; 34 niche brands pooled into `Niche_Other`). Sensitivity analyses at thresholds of 10 and 30 are pre-specified. `Niche_Other` will not be presented as a consumer-facing brand.
3. **Decision D3 — Missing Data & Subsample Governance:**
   - *Status:* **APPROVED** by Project Owner.
   - *Framework:* Core Models 1–3 strictly omit `charging_wattage` and `refresh_rate_hz` to preserve $N = 2,195$ (>97% complete-case sample). Model 5 is restricted to the modern feature cohort ($N = 1,101$) with explicit disclosure that missingness is potentially systematic and results cannot be generalized to the complete catalog. Zero imputation.
4. **Decision D4 — Model 4 Sensitivity Subsample Definition:**
   - *Status:* **APPROVED** by Project Owner (Option 3: Revision 02 Empirical).
   - *Framework:* Excludes 7 devices (17 configurations: 4 SoC changes, 2 front camera changes, 1 degenerate memory tier `xiaomi-mi-max`), retaining 476 clusters (1,075 configurations). Within-VIF is 1.125 and standardized condition number is 2.00.
5. **Decision D5 — Public Editorial Presentation Strategy:**
   - *Status:* **NOT YET APPROVED**.
   - *Governance:* The proposal to feature Model 3 (Hedonic Brand Fixed Effects) and Model 4 (Within-Device Upgrade Associations) in the public web product is held pending empirical estimation, design matrix rank diagnostics, and formal project-owner review following Stage 04 modeling.

---

*End of Formal Methodology Document — Phase 04 Stage 03.*  
*Formally approved and baseline established.*
