# PHASE 04 — STAGE 03: METHODOLOGY DESIGN & RESEARCH FRAMEWORK
## Econometric Specifications, Identification Strategy, and Statistical Governance

> **PROJECT TITLE:** What Are We Really Paying For When We Buy a Smartphone?  
> **PRODUCT IDENTITY:** Experimental Technical Editorial  
> **DOCUMENT TYPE:** Research Methodology Design & Pre-Analysis Protocol  
> **AUTHOR / ROLE:** Senior Data Scientist, Applied Econometrician & Quantitative Methodologist  
> **STATUS:** PROPOSED — PENDING PROJECT OWNER APPROVAL  
> **TARGET IMPLEMENTATION:** Phase 04 — Stage 04 (Analytical Modeling)  
> **ACCEPTED DATA BASELINE:** Commit `59906f6` (`phase-04-stage-02-implementation`)  
> **ANALYTICAL DATASET:** Exactly 2,256 verified, deduplicated records from Indian retail market (2011 – mid-2024)  

---

## 01. Executive Summary

This document establishes the comprehensive econometric methodology, statistical validation framework, and research integrity protocols for investigating smartphone retail pricing and component specifications.

The central investigation addresses a fundamental question of consumer technology economics:
$$\textbf{"What are consumers actually paying for when purchasing a smartphone, and how do hardware specifications, brand identity, and market positioning relate to its listed retail price?"}$$

### The Methodological Stance: Observational Hedonic Econometrics
The research treats smartphone pricing strictly as an **observational market equilibrium phenomenon**. In competitive differentiated-product markets, listed retail prices reflect both supply-side manufacturing costs (component silicon, memory, display panels, chassis materials, assembly, logistics, royalties) and demand-side valuation (brand reputation, operating system ecosystem, perceived build quality, marketing positioning, and willingness-to-pay).

Because this study relies on observational web-scraped retail data, **no simple regression model can establish pure causality**. Observed correlations between specifications and prices reflect conditional market associations, not engineering determinants of product quality. Furthermore, estimated brand coefficients reflect both unobserved hardware attributes (optical stabilization, display calibration, haptic motors, thermal management) and true brand equity.

To provide rigorous, intellectually honest answers without resorting to marketing hype or generic data science clichés, we propose:
1. **A Semi-Log Hedonic Price Framework:** Modeling $\ln(\text{original\_listed\_price\_inr})$ to stabilize extreme raw price skewness ($3.36 \to 0.80$) and provide interpretable percentage markups.
2. **Device-Level Cluster-Robust Inference:** Adjusting standard errors for intra-cluster correlation across the 609 memory configurations belonging to multi-variant base devices ($G = 1,647$ clusters).
3. **A Dual-Level Identification Strategy:** Combining cross-sectional hedonic models (to evaluate market-wide component scaling and brand positioning) with a **Within-Device Fixed Effects Model** (to isolate pure marginal memory markups within the identical physical smartphone chassis).
4. **A Dedicated External Benchmark Ledger:** Strictly isolating external longitudinal metrics (software support commitments, repairability scores, battery degradation curves) from the primary empirical dataset.

---

## 02. Research Objectives

1. **Quantify Specification Scaling:** Estimate the conditional marginal association between key hardware attributes (RAM, internal storage, battery capacity, fast charging, display size, display technology, optics, and semiconductor platform) and listed retail prices in Indian Rupees (INR).
2. **Isolate the Marginal Price of Memory:** Distinguish the market-wide cross-sectional markup of RAM and storage from the within-chassis upgrade pricing set by original equipment manufacturers (OEMs).
3. **Measure Conditional Brand Differentials:** Evaluate whether specific brands command statistically significant price premiums after controlling for observable hardware specifications, and quantify how much pricing variation remains unexplained by spec-sheets alone.
4. **Characterize Structural Market Heterogeneity:** Analyze how specification returns and brand markups shift across the five established descriptive editorial price tiers (Entry-level, Budget-to-mid, Mid-range, Upper-mid, Premium).
5. **Establish a Defensible External Evidence Stream:** Create a standardized, documented protocol for integrating third-party longevity benchmarks (Pillar 02: Ownership Value) without contaminating empirical dataset provenance.

---

## 03. Research Questions Hierarchy

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
│ • RQ1.1: Storage & RAM Markups       │ • RQ2.1: Conditional Brand Spreads   │
│ • RQ1.2: Semiconductor Stratification│ • RQ2.2: Unobserved Variance Share   │
│ • RQ1.3: Battery Ergonomic Decoupling│ • RQ2.3: Segment-Specific Differentials│
│ • RQ1.4: Display Technology Premium  │                                      │
├──────────────────────────────────────┴──────────────────────────────────────┤
│ PILLAR 03: MARKET SEGMENTATION & DIMINISHING RETURNS                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ • RQ3.1: Structural Elasticity Shifts Across Editorial Price Tiers         │
│ • RQ3.2: Identification of Specification Plateau Thresholds                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Pillar 01 — Specification-Price Relationships
- **RQ1.1 (Memory Scaling):** Holding all other observable hardware attributes constant, what is the estimated percentage increase in retail price associated with an additional gigabyte of RAM and an additional gigabyte of internal storage?
- **RQ1.2 (Semiconductor Hierarchy):** What conditional price differentials exist across application processor manufacturers (Qualcomm Snapdragon, MediaTek, Apple Silicon, Samsung Exynos, Unisoc, HiSilicon Kirin) when controlling for memory and display attributes?
- **RQ1.3 (Battery Capacity & Ergonomic Decoupling):** Does battery capacity (mAh) retain a positive conditional association with price, or does its association turn negative/negligible once device dimensions and flagship status are controlled for?
- **RQ1.4 (Display Panel Technology):** What is the conditional price premium of OLED (AMOLED, P-OLED, Super AMOLED) display panels relative to baseline LCD (IPS, TFT) panels?

### Pillar 02 — Brand Positioning & Price Differentials
- **RQ2.1 (Conditional Brand Spread):** After adjusting for observable hardware components, do Tier-1 manufacturers (Apple, Samsung, Google) command statistically significant positive price differentials relative to high-volume value brands (Xiaomi/Redmi, Realme, POCO)?
- **RQ2.2 (Spec-Sheet Explanatory Power):** What proportion of cross-brand pricing variance is explained by spec-sheet hardware characteristics versus residual brand indicators?
- **RQ2.3 (Brand Segment Heterogeneity):** Do brand price markups remain constant across market tiers, or do they amplify in the upper-mid and premium brackets?

### Pillar 03 — Market Segmentation & Diminishing Returns
- **RQ3.1 (Segment Elasticity Shifts):** How do specification returns vary across the five established editorial price tiers (Entry-level $< ₹10\text{k}$, Budget-to-mid $₹10\text{k}–₹20\text{k}$, Mid-range $₹20\text{k}–₹35\text{k}$, Upper-mid $₹35\text{k}–₹60\text{k}$, Premium $\ge ₹60\text{k}$)?
- **RQ3.2 (Diminishing Marginal Utility Thresholds):** At what physical thresholds do marginal specification increases cease to correlate with higher consumer ratings or expert evaluation scores?

---

## 04. Formal Research Hypotheses

| Hypothesis ID | Statement | Null Hypothesis ($H_0$) | Alternative Hypothesis ($H_A$) | Econometric Parameter |
|---|---|---|---|:---:|
| **H1 (Storage Markup)** | Internal storage capacity exhibits a statistically significant positive conditional association with retail price. | $\beta_{\text{storage}} \le 0$ | $\beta_{\text{storage}} > 0$ | $t$-test on $\beta_{\text{storage}}$ |
| **H2 (RAM Markup)** | RAM capacity exhibits a statistically significant positive conditional association with retail price. | $\beta_{\text{ram}} \le 0$ | $\beta_{\text{ram}} > 0$ | $t$-test on $\beta_{\text{ram}}$ |
| **H3 (Battery Decoupling)** | In a multivariate hedonic model controlling for screen size, SoC, and brand, battery capacity (mAh) exhibits a non-positive or statistically negligible association with retail price. | $\beta_{\text{battery}} > 0$ | $\beta_{\text{battery}} \le 0$ | One-sided test on $\beta_{\text{battery}}$ |
| **H4 (OLED Panel Premium)** | OLED display technology commands a statistically significant price premium over baseline LCD technology. | $\delta_{\text{OLED}} \le 0$ | $\delta_{\text{OLED}} > 0$ | $t$-test on $\delta_{\text{OLED}}$ |
| **H5 (Apple Conditional Differential)** | Holding observable hardware specifications constant, Apple devices command a statistically significant positive price markup over baseline value manufacturers. | $\theta_{\text{Apple}} \le 0$ | $\theta_{\text{Apple}} > 0$ | $t$-test on $\theta_{\text{Apple}}$ |
| **H6 (Within-Device Storage Markup)** | Upgrading internal storage within the identical smartphone model chassis yields a statistically significant positive price increase. | $\beta_{\text{within\_storage}} \le 0$ | $\beta_{\text{within\_storage}} > 0$ | Within-estimator $t$-test |

---

## 05. Dataset & Variable Inventory

The econometric analysis will be conducted exclusively on the verified, deduplicated dataset produced in Phase 04 Stage 02:
- **Source Artifacts:** [`Data/processed/smartphones_cleaned.csv`](file:///c:/Smartphone%20Analysis/Smartphone_Analysis/Data/processed/smartphones_cleaned.csv) and [`Data/processed/smartphones_cleaned.json`](file:///c:/Smartphone%20Analysis/Smartphone_Analysis/Data/processed/smartphones_cleaned.json)
- **Population:** Exactly 2,256 verified unique smartphone records.
- **Geographic Market:** Indian retail smartphone market.
- **Temporal Span:** Mid-2011 through August 2024.

### Complete Variable Role & Missingness Ledger

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      VARIABLE INVENTORY & ROLES                                        │
├──────────────────────────────┬───────────┬──────────────┬────────────┬─────────────────────────────────┤
│ Field Name                   │ Data Type │ Role         │ Valid N (%)│ Description / Scale             │
├──────────────────────────────┼───────────┼──────────────┼────────────┼─────────────────────────────────┤
│ original_listed_price_inr    │ Integer   │ Dependent    │ 2256 (100%)│ Indian Rupee retail price (₹)   │
│ log_price_inr                │ Float     │ Transformed  │ 2256 (100%)│ ln(original_listed_price_inr)   │
│ listing_id                   │ String    │ Identifier   │ 2256 (100%)│ Source row provenance (rec_XXXX)│
│ device_id                    │ String    │ Cluster ID   │ 2256 (100%)│ Base model slug (1,647 unique)  │
│ config_id                    │ String    │ Identifier   │ 2256 (100%)│ Variant slug (2,255 unique)     │
│ ram_capacity_gb              │ Float     │ Core Regressor│ 2248 (99.6%)│ RAM capacity in Gigabytes (GB)  │
│ storage_capacity_gb          │ Float     │ Core Regressor│ 2254 (99.9%)│ Storage capacity in GB (1TB=1024)│
│ battery_capacity_mah         │ Integer   │ Core Regressor│ 2256 (100%)│ Battery capacity in mAh         │
│ screen_size_inches           │ Float     │ Core Regressor│ 2255 (100%)│ Screen diagonal in inches       │
│ display_panel_family         │ Enum      │ Core Regressor│ 2254 (99.9%)│ OLED (AMOLED/P-OLED) vs LCD     │
│ rear_main_sensor_mp          │ Float     │ Core Regressor│ 2256 (100%)│ Primary rear camera resolution  │
│ rear_lens_count              │ Integer   │ Core Regressor│ 2256 (100%)│ Total rear optical lenses count │
│ front_main_sensor_mp         │ Float     │ Core Regressor│ 2224 (98.6%)│ Front selfie sensor resolution  │
│ processor_manufacturer       │ Enum      │ Core Regressor│ 2196 (97.3%)│ Qualcomm, MediaTek, Apple, etc. │
│ brand_name                   │ Enum      │ Core Regressor│ 2256 (100%)│ 63 canonical brands             │
│ brand_tier                   │ Enum      │ Stratifier   │ 2256 (100%)│ Major (>=20), Mid, Niche        │
├──────────────────────────────┼───────────┼──────────────┼────────────┼─────────────────────────────────┤
│ charging_wattage             │ Float     │ Extended Reg │ 1321 (58.6%)│ Fast charging speed in Watts (W)│
│ refresh_rate_hz              │ Float     │ Extended Reg │ 1133 (50.2%)│ Panel refresh rate (Hz)         │
│ processor_core_count         │ Float     │ Extended Reg │ 2039 (90.4%)│ CPU cores (Hexa, Octa, etc.)    │
│ expert_rating                │ Float     │ Telemetry    │ 1398 (62.0%)│ MySmartPrice editorial score    │
│ user_rating_score            │ Float     │ Telemetry    │ 2185 (96.9%)│ Consumer star rating (0–5)      │
│ user_rating_count            │ Integer   │ Weighting    │ 2185 (96.9%)│ Total consumer review count     │
│ price_quintile               │ Enum      │ Segmentation │ 2256 (100%)│ Q1..Q5 (Right-closed intervals) │
│ editorial_price_tier         │ Enum      │ Segmentation │ 2256 (100%)│ Entry, Budget, Mid, Upper, Prem │
└──────────────────────────────┴───────────┴──────────────┴────────────┴─────────────────────────────────┘
```

---

## 06. Analytical Pillars

### Pillar 01 — Specification Scaling & Marginal Hedonic Value
Evaluates the physical specification returns across the smartphone landscape. We model listed price as a function of component capabilities, isolating the conditional contribution of memory density, screen estate, and processing silicon.

### Pillar 02 — Brand Positioning & Residual Markup Analysis
Quantifies the pricing spread across manufacturers while holding observable hardware specifications constant. 
> [!IMPORTANT]
> **Econometric Governance on Brand Premiums:** A positive brand coefficient ($\hat{\theta}_b > 0$) must **never** be cited in public editorial copy as a "pure brand tax" or "irrational consumer markup." It represents the conditional price differential attributable to both brand equity **and all unobserved product attributes correlated with that brand** (proprietary OS software, industrial chassis metallurgy, IP water resistance certifications, optical image stabilization engineering, thermal dissipation chambers, and post-sales service networks).

### Pillar 03 — Market Segmentation & Structural Elasticity Shifts
Examines how specification returns behave across different price tiers. Does an extra 2GB of RAM command the same percentage price premium in a sub-₹10,000 entry-level device as it does in a ₹40,000 mid-range phone? We employ stratified regressions and quantile regression to expose non-linearities and diminishing returns.

---

## 07. Candidate Econometric Models

We formulate six econometric model specifications designed to balance explanatory power, sample completeness, and identification rigor:

### Model 1: Baseline Core Hedonic Specification (OLS with Cluster-Robust SEs)
Evaluates universal component scaling on the near-complete sample ($N \approx 2,246$).
$$\ln(\text{Price}_i) = \beta_0 + \beta_1 \text{RAM}_i + \beta_2 \text{Storage}_i + \beta_3 \text{Battery}_i + \beta_4 \text{ScreenSize}_i + \beta_5 \text{RearMP}_i + \beta_6 \text{RearLenses}_i + \delta_1 \mathbf{1}\{\text{OLED}_i\} + \epsilon_i$$
- **Dependent Variable:** $\ln(\text{original\_listed\_price\_inr})$
- **Cluster Variable:** `device_id` (1,647 clusters)
- **Interpretation:** $\beta_k$ represents the semi-elasticity of price with respect to specification $k$: a 1-unit increase in $X_k$ is associated with approximately a $100 \times \beta_k\%$ change in price (exact: $100 \times (\exp(\beta_k) - 1)\%$).
- **Assumptions:** Zero conditional mean of error given core specifications ($E[\epsilon \mid \mathbf{X}] = 0$).

### Model 2: Hedonic Specification with Semiconductor Platform Fixed Effects
Controls for application processor silicon vendor tiering.
$$\ln(\text{Price}_i) = \beta_0 + \mathbf{X}_{i, \text{core}}' \boldsymbol{\beta} + \sum_{m \in \text{SoC}} \gamma_m \mathbf{1}\{\text{SoC\_Manufacturer}_i = m\} + \epsilon_i$$
- **Reference Category:** `MediaTek` (the high-volume value semiconductor baseline).
- **SoC Groups:** Qualcomm Snapdragon, Apple Silicon, Samsung Exynos, Unisoc, HiSilicon Kirin, Google Tensor, Other.
- **Purpose:** Prevents memory and display coefficients from absorbing the higher costs of flagship mobile chipsets.

### Model 3: Full Hedonic Specification with Brand Fixed Effects
The primary cross-sectional workhorse model for isolating conditional brand price differentials.
$$\ln(\text{Price}_i) = \beta_0 + \mathbf{X}_{i, \text{core}}' \boldsymbol{\beta} + \sum_{m \in \text{SoC}} \gamma_m \mathbf{1}\{\text{SoC}_i = m\} + \sum_{b \in \text{Brands}} \theta_b \mathbf{1}\{\text{Brand}_i = b\} + \epsilon_i$$
- **Reference Brand:** `Xiaomi` (including Redmi), representing the Indian market's dominant empirical volume/value baseline.
- **Brand Grouping Protocol:** Explicit indicator variables for the 29 established brands with $\ge 20$ listings; long-tail niche brands ($N < 20$) pooled into a unified `Niche_Other` indicator to avoid high-variance incidental parameter distortion.
- **Interpretation of $\theta_b$:** The percentage difference in listed price between brand $b$ and Xiaomi for devices with identical observable core specifications and silicon vendors.

### Model 4: Within-Device Fixed Effects Model (Pure Memory Upgrade Pricing)
Isolates the marginal retail price of RAM and storage within the exact same device chassis, eliminating all device-level unobservables.
$$\ln(\text{Price}_{ij}) = \alpha_i + \beta_{\text{RAM}}^{\text{within}} \text{RAM}_{ij} + \beta_{\text{Storage}}^{\text{within}} \text{Storage}_{ij} + \nu_{ij}$$
- **Sample:** The subset of records where `device_id` has multiple configurations ($N = 609$ listings across 483 multi-variant models).
- **$\alpha_i$:** Unobserved device fixed effect representing chassis build, display panel, camera sensor, processor, brand prestige, and acoustic engineering.
- **Econometric Superiority:** By differencing out $\alpha_i$, this model achieves clean identification of memory upgrade pricing without omitted variable bias:
  $$(\ln(\text{Price}_{ij}) - \overline{\ln(\text{Price}_i)}) = \beta_{\text{RAM}}^{\text{within}} (\text{RAM}_{ij} - \overline{\text{RAM}}_i) + \beta_{\text{Storage}}^{\text{within}} (\text{Storage}_{ij} - \overline{\text{Storage}}_i) + (\nu_{ij} - \bar{\nu}_i)$$

### Model 5: Extended Feature Specification (Fast Charging & Refresh Rate Sub-Sample)
Evaluates premium feature returns on the modern sub-sample ($N \approx 1,050$) where fast charging and high refresh rates are explicitly marketed.
$$\ln(\text{Price}_i) = \beta_0 + \mathbf{X}_{i, \text{core}}' \boldsymbol{\beta} + \beta_7 \text{ChargingWatts}_i + \beta_8 \text{RefreshRate}_i + \mathbf{D}_{\text{SoC}}' \boldsymbol{\gamma} + \mathbf{D}_{\text{Brand}}' \boldsymbol{\theta} + \epsilon_i$$
- **Purpose:** Quantifies the marginal association of fast charging speed ($W$) and refresh rate ($\text{Hz}$) while monitoring sample selection bias against Model 3.

### Model 6: Quantile Regression Specification (Heterogeneous Returns Across Price Brackets)
Models conditional price quantiles to evaluate whether specification returns differ at the 10th, 25th, 50th, 75th, and 90th percentiles of the market.
$$Q_\tau(\ln(\text{Price}_i) \mid \mathbf{Z}_i) = \mathbf{Z}_i' \boldsymbol{\beta}(\tau) \quad \text{for } \tau \in \{0.10, 0.25, 0.50, 0.75, 0.90\}$$
- **Purpose:** Directly answers whether RAM or storage expansion yields steeper price markups in luxury flagship devices ($\tau = 0.90$) compared to budget devices ($\tau = 0.10$).

---

## 08. Variable Selection & Transformation Strategy

### Why Log-Price ($\ln(\text{Price})$) is Econometrically Mandatory
Inspection of `original_listed_price_inr` demonstrates severe non-normality:
- **Raw Price Skewness:** **3.36** | **Raw Price Kurtosis:** **14.05** (extreme right tail up to ₹200,999)
- **Log Price Skewness:** **0.80** | **Log Price Kurtosis:** **0.31** (stabilized, near-Gaussian bell shape)

Modeling price in linear INR levels would violate homoskedasticity assumptions, cause high-priced flagships to exert extreme statistical leverage, and yield model residuals that severely violate standard regression assumptions. Log-transforming price delivers proportional (percentage) markups, which align directly with how hardware upgrades are priced by consumers and OEMs.

### Level vs. Log Specification of Regressors
- **RAM and Storage:** Retained in **linear Gigabytes (GB)**. Physical memory is manufactured in discrete quantitative capacities (e.g., +4GB RAM, +128GB flash). A linear regressor yields the intuitive semi-elasticity: *"each additional 128GB of storage is associated with a $(128 \times \beta_{\text{storage}})\%$ increase in price."*
- **Battery Capacity:** Scaled in **thousands of mAh** ($\text{Battery} / 1000.0$) to avoid minuscule coefficients with four leading zeros.
- **Charging Wattage:** Scaled in **Watts (W)**.
- **Screen Size:** Scaled in **Inches**.

### Device-Level Clustering Protocol
Because 609 listings represent secondary configurations of existing smartphone models, observation errors within the same `device_id` are correlated ($E[\epsilon_{ij} \epsilon_{ik}] \ne 0$). Standard OLS variance formulas would underestimate standard errors and inflate $t$-statistics. All cross-sectional models must compute **cluster-robust standard errors clustered on `device_id`**:
$$\mathbf{V}_{\text{cluster}} = (\mathbf{X}'\mathbf{X})^{-1} \left( \sum_{g=1}^G \mathbf{X}_g' \hat{\mathbf{e}}_g \hat{\mathbf{e}}_g' \mathbf{X}_g \right) (\mathbf{X}'\mathbf{X})^{-1}$$

### Missingness & Censoring Handling
- **Zero Imputation Policy:** In accordance with Project Governance, no missing specification will be replaced with sample means or modes.
- **Core Variables Complete-Case Filter:** Restricting Core Models (Models 1–3) to rows with non-null values across Core Hardware Regressors retains $N = 2,246$ records (**99.56% sample retention**), minimizing any risk of sample selection distortion.
- **Extended Variables Sub-Sample Modeling:** Regressors with structural historical missingness (`charging_wattage` missing in 41.5%, `refresh_rate_hz` missing in 49.8%) will be evaluated in Model 5 as a dedicated modern cohort specification, accompanied by explicit sample comparisons.

---

## 09. External Benchmark Evidence Framework (Pillar 02: Ownership Value)

External research benchmarks must remain strictly separated from the empirical MySmartPrice dataset. They will be maintained in a standalone JSON ledger (`Data/processed/external_ownership_benchmarks.json`) and must satisfy the following documentation schema:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 EXTERNAL BENCHMARK SOURCE ATTRIBUTION SCHEMA                │
├──────────────────────┬──────────────────────────────────────────────────────┤
│ Attribute            │ Standard / Requirement                               │
├──────────────────────┼──────────────────────────────────────────────────────┤
│ Metric Name          │ Standardized research variable name                  │
│ Metric Definition    │ Exact mathematical and conceptual meaning           │
│ Publishing Org       │ Official authoritative entity (OEM, Gov, Lab)       │
│ Source URL           │ Canonical direct link to official policy / paper     │
│ Publication Date     │ ISO 8601 release date (e.g., 2024-01-17)            │
│ Observation Window   │ Time period or product generation covered            │
│ Geographic Scope     │ Global vs. Regional (India specific where available) │
│ Unit of Measurement  │ Years, percentage, index score (0–10)                │
│ Methodology Summary  │ How the benchmark was generated                      │
│ Reliability Tier     │ Verified Primary / Standard Industry Benchmark       │
│ Research Application │ Exact chapter/chart in product where used            │
│ Known Limitations    │ Scope exclusions, caveats, and boundary conditions   │
└──────────────────────┴──────────────────────────────────────────────────────┘
```

### Approved Benchmark Components for Pillar 02

1. **Guaranteed Software Support Lifecycles:**
   - *Sources:* Official OEM policy announcements (Apple Support Document HT201222; Google Tensor Update Commitment Policy; Samsung Newsroom Galaxy S24 Support Release).
   - *Data:* Apple iOS (5–7 years historical); Google Pixel 8/9 series (7 years OS + security); Samsung Galaxy S24 series (7 years OS + security); Samsung Galaxy A-series (4 years OS + 5 years security); Xiaomi / Realme budget tiers (1–2 years OS + 3 years security).
2. **Standardized Physical Repairability Indices:**
   - *Sources:* French Ministry of Ecological Transition (*Indice de réparabilité* official public database) and iFixit Smartphone Repairability Scorecards.
   - *Data:* Normalized repairability scores on a 1.0–10.0 scale reflecting documentation availability, disassembly ease, parts availability, and parts pricing.
3. **Lithium-Ion Battery Degradation Physics:**
   - *Sources:* Standard battery electrochemistry standards (IEEE 1725 / IEC 61960).
   - *Data:* Standard capacity retention decay model assuming 80% remaining capacity after 500 equivalent full cycles (standard budget pouch cells) to 1,000 cycles (modern dual-cell silicon-carbon batteries).
4. **Total Cost of Ownership (TCO) Amortization Simulation:**
   - *Model:* Purely researcher-defined mathematical simulation:
     $$\text{Amortized Cost Per Day} = \frac{\text{Initial Purchase Price} + \text{Estimated Maintenance Costs} - \text{Expected Resale Value}}{\text{Ownership Lifespan (Days)}}$$
   - *Governance:* Must be explicitly labeled in UI as an **Interactive Economic Hypothesis Simulator**, never conflated with observed dataset transactions.

> [!CAUTION]
> **Currency Conversion Remains DEFERRED:** Currency conversion to USD and IDR remains strictly inactive until primary-source historical central bank reference time-series rates are verified and logged. Base analytical operations will be conducted exclusively in INR.

---

## 10. Statistical Diagnostics & Validation Plan

Every econometric model must undergo automated diagnostic profiling prior to interpreting coefficients:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         STATISTICAL DIAGNOSTIC PIPELINE                     │
├─────────────────────────┬───────────────────────────┬───────────────────────┤
│ Diagnostic Check        │ Statistical Test          │ Action Threshold      │
├─────────────────────────┼───────────────────────────┼───────────────────────┤
│ Multicollinearity       │ Variance Inflation Factor │ VIF > 5.0 (Review)    │
│                         │ (VIF) on Regressors       │ VIF > 10.0 (Collinear)│
├─────────────────────────┼───────────────────────────┼───────────────────────┤
│ Heteroskedasticity      │ Breusch-Pagan & White Test│ p < 0.05 -> Mandatory │
│                         │                           │ Cluster-Robust SEs    │
├─────────────────────────┼───────────────────────────┼───────────────────────┤
│ Residual Normality      │ Jarque-Bera & Q-Q Plot    │ Large-sample asymptotic│
│                         │                           │ inference validation  │
├─────────────────────────┼───────────────────────────┼───────────────────────┤
│ Influential Observations│ Cook's Distance ($D_i$)   │ $D_i > 4/N \approx 0.0018$   │
│                         │ DFBETAS                   │ Report with/without   │
├─────────────────────────┼───────────────────────────┼───────────────────────┤
│ Specification Error     │ Ramsey RESET Test         │ Test for omitted      │
│                         │ (powers of fitted values) │ non-linear terms      │
└─────────────────────────┴───────────────────────────┴───────────────────────┘
```

### Protocol for Diagnostic Violations:
1. **Severe Multicollinearity ($VIF > 10$):** If RAM and Storage or Screen Size and Lens Count exhibit severe collinearity, regressors will be evaluated via orthogonalization or composite dimensionality tests rather than dropping variables arbitrarily.
2. **Influential Outliers:** Top-leverage observations (e.g., luxury foldables above ₹150,000) will be flagged. Models will be re-estimated excluding the top 1% of prices to confirm that coefficient signs and magnitudes are not driven by extreme tail outliers.
3. **Explanatory vs. Predictive Modeling Distinction:** Models will be evaluated on coefficient stability, economic plausibility, and cluster-robust confidence intervals, **not solely on out-of-sample prediction metrics** ($R^2$, RMSE).

---

## 11. Robustness & Sensitivity Plan

To guarantee that analytical conclusions are robust and not artifacts of specific functional forms, we will conduct six systematic sensitivity tests:

1. **Functional Form Robustness:** Compare linear spec models against polynomial specifications ($\text{RAM}^2$, $\text{Storage}^2$) and log-log specifications ($\ln(\text{RAM})$, $\ln(\text{Storage})$).
2. **Sub-Sample Price Tier Stability:** Re-estimate Model 3 across the five editorial tiers to test whether spec markups remain stable across market brackets.
3. **Brand Aggregation Sensitivity:** Compare estimates under three brand grouping strategies:
   - All 63 canonical brands.
   - Top 29 established brands ($\ge 20$ listings) + pooled niche group.
   - Corporate holding provenance groups (BBK Electronics, Xiaomi Group, Transsion Holdings, Lenovo/Motorola, Independent).
4. **Temporal Cohort Sensitivity:** Estimate models separately on legacy models (2011–2019) vs. modern smartphones (2020–2024) to evaluate historical spec inflation.
5. **Cross-Sectional vs. Within-Device Contrast:** Directly compare the cross-sectional storage markup ($\hat{\beta}_{\text{storage}}$ from Model 3) with the within-device storage upgrade markup ($\hat{\beta}_{\text{storage}}^{\text{within}}$ from Model 4).
6. **Outlier Truncation:** Re-estimate models trimming the top 1% and bottom 1% of prices ($₹5,324 < \text{Price} < ₹138,675$).

---

## 12. Research Limitations & Explicit Boundaries

1. **Observational Cross-Section:** Regression coefficients represent conditional correlations in a retail catalog, not causal effects. We cannot conclude that adding 4GB of RAM costs an OEM a specific dollar amount to manufacture.
2. **Geographic Market Specificity:** All pricing data originates from the Indian smartphone retail market, incorporating local Goods and Services Tax (18% GST) and import tariffs on completely built units (CBUs). Converted figures cannot be interpreted as US or European MSRPs.
3. **Temporal Cutoff:** The empirical dataset concludes in mid-2024. Late-2024 flagships (Apple iPhone 16 series, Google Pixel 9 series, Snapdragon 8 Elite, Dimensity 9400) are post-dataset developments.
4. **Catalog Listings vs. Market Share:** The dataset represents the diversity of models available for retail purchase in India, not consumer sales volumes. A model with 1 listing may have sold 5 million units, while another sold 5,000 units.
5. **Omitted Quality Variables:** Key dimensions of modern smartphone value—such as software optimization, optical image stabilization (OIS), display color calibration ($\Delta E$), haptic motor quality, and post-purchase customer support—are unobserved in web-scraped spec sheets.
6. **Brand Coefficient Interpretation:** Brand fixed effects capture the sum of brand equity, unobserved hardware quality, and distribution costs. They must not be labeled as pure "prestige markup."

---

## 13. Research Integrity Checklist

Before transitioning to analytical code implementation, the methodology satisfies all project governance rules:
- [x] Ground truth currency strictly maintained in Indian Rupees (INR, ₹).
- [x] Currency conversion deferred until historical rates are verified.
- [x] Zero arbitrary missing-data imputation.
- [x] No causal claims from observational regressions.
- [x] Cluster-robust standard errors mandated for multi-variant devices.
- [x] Within-device identification designed to isolate memory markups cleanly.
- [x] Clear separation between dataset-observed specs and external longevity benchmarks.
- [x] Explicit prohibition of conflating catalog listing counts with sales volumes.
- [x] Strict preservation of all raw data and historical notebooks.

---

## 14. Proposed Implementation Sequence (Phase 04 Stage 04)

Upon receiving stakeholder approval for this methodology, analytical execution will proceed in eight modular steps:

1. **Stage 04.1 (Sample Preparation & Matrices):** Create `scripts/analysis/prepare_matrices.py` to extract regression arrays, log transformations, and dummy variables.
2. **Stage 04.2 (Diagnostic Profiling):** Execute VIF multicollinearity and Cook's distance diagnostics.
3. **Stage 04.3 (Core Hedonic Models):** Fit Models 1, 2, and 3 with cluster-robust standard errors via `statsmodels`.
4. **Stage 04.4 (Within-Device Model):** Fit Model 4 on the multi-variant sub-sample.
5. **Stage 04.5 (Extended Feature & Quantile Regressions):** Fit Models 5 and 6.
6. **Stage 04.6 (Sensitivity Suite):** Execute the six robustness checks.
7. **Stage 04.7 (External Benchmark Ledger Serialization):** Compile `external_ownership_benchmarks.json`.
8. **Stage 04.8 (Automated Regression Tests & Verification):** Implement regression test suites in `tests/test_econometric_models.py`.

---

## 15. Open Questions Requiring Project Owner Approval

The following four methodological questions require explicit review and formal decision before implementation begins:

1. **Brand Fixed Effects Reference Baseline:**  
   *Proposal:* Use **Xiaomi** (including Redmi) as the omitted reference category because it represents the highest-volume, value-oriented Android baseline in the Indian market.  
   *Alternative:* Use a grand mean (deviation coding) where brand coefficients reflect differences from the market average.  
   *Question:* Does the project owner approve Xiaomi as the baseline reference brand?

2. **Niche Brand Aggregation Threshold:**  
   *Proposal:* Brands with fewer than 20 model listings (34 brands covering 136 records, ~6% of catalog) will be pooled into a single `Niche_Other` indicator in cross-sectional brand models to prevent unstable coefficients from sample sizes of $N=1$ or $N=2$.  
   *Question:* Is the $N < 20$ pooling threshold approved?

3. **Extended Feature Sub-Sample Strategy:**  
   *Proposal:* For fast charging wattage (missing in 41.5%) and refresh rate (missing in 49.8%), keep them out of Core Models 1–3 to preserve $N = 2,246$ (99.56% complete-case sample), and evaluate them exclusively in a dedicated Model 5 modern sub-sample.  
   *Question:* Does the project owner approve keeping Core Models 1–3 free of charging and refresh rate variables to avoid sample truncation?

4. **Primary Public Editorial Specification:**  
   *Proposal:* Feature **Model 3** (Hedonic Brand Fixed Effects) for overall market comparisons and **Model 4** (Within-Device Fixed Effects) for consumer memory upgrade discussions on the website.  
   *Question:* Does the project owner approve this dual presentation approach?

---

*End of Methodology Design Document — Awaiting Project Owner Review & Approval.*
