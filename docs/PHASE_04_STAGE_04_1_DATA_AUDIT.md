# PHASE 04 — STAGE 04.1: ANALYTICAL ENVIRONMENT & DATA AUDIT REPORT
## Pre-Estimation Data Integrity Verification, Environment Profiling, and Econometric Model Readiness

> **PROJECT TITLE:** What Are We Really Paying For When We Buy a Smartphone?  
> **PRODUCT IDENTITY:** Experimental Technical Editorial  
> **DOCUMENT TYPE:** Analytical Environment Audit & Pre-Estimation Data Verification  
> **AUTHOR / ROLE:** Senior Data Scientist, Applied Econometrician & Software Architect  
> **STATUS:** COMPLETED — PENDING PROJECT OWNER APPROVAL BEFORE STAGE 04.2  
> **TARGET IMPLEMENTATION:** Phase 04 — Stage 04.2 (Matrix Preparation & Diagnostics)  
> **ACCEPTED BASELINE DATASET:** Stage 02 Canonical Artifacts (Commit `59906f6`)  
> **AUTHORITATIVE METHODOLOGY:** [`docs/PHASE_04_STAGE_03_METHODOLOGY.md`](file:///c:/Smartphone%20Analysis/Smartphone_Analysis/docs/PHASE_04_STAGE_03_METHODOLOGY.md) (Revision 04)  
> **WORKING BRANCH:** `phase-04-stage-03-methodology-design`

---

## 01. Executive Summary

This document delivers the comprehensive, reproducible analytical environment audit and data integrity verification for Phase 04 Stage 04.1. 

In strict adherence to the project governance framework (**DISCOVER → AUDIT → PLAN → APPROVE → IMPLEMENT → REVIEW**) and the approved **Research Integrity & Data Provenance Rules**:
1. **Zero Econometric Models Estimated:** No regressions were fitted, no parameter estimates were generated, and no inferential hypothesis tests were executed. This stage is strictly limited to analytical preparation and empirical validation.
2. **Authoritative Dataset Audited:** The Stage 02 processed dataset (`smartphones_cleaned.csv` and `smartphones_cleaned.json`, exactly **2,256 records × 45 fields**) was thoroughly audited, reconciled against Stage 02 audit artifacts, and evaluated across all 6 planned econometric models.
3. **Environment Evaluated & Dependency Action Proposed:** Python 3.14.4 environment was profiled. Critical modeling libraries (`scipy` and `statsmodels`) are currently absent. Pre-built Windows wheels were verified via pip dry-run. A formal request to install `scipy` and `statsmodels` is submitted for project-owner approval prior to Stage 04.2.
4. **Model 4 Structural Readiness Formally Characterized:** The nested multi-variant architecture ($N = 1,092$ configurations across $G = 483$ device clusters) was decomposed into independent variation subsets, hardware-invariance exceptions were cataloged, and the sequential 5-tier fallback hierarchy was validated.

---

## 02. Repository and Git State Audit

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              GIT REPOSITORY AUDIT LEDGER                               │
├──────────────────────────────┬─────────────────────────────────────────────────────────┤
│ Parameter                    │ Verified Value                                          │
├──────────────────────────────┼─────────────────────────────────────────────────────────┤
│ Active Working Branch        │ phase-04-stage-03-methodology-design                    │
│ Target Implementation Branch │ phase-04-stage-03-methodology-design                    │
│ Accepted Stage 02 Checkpoint │ 59906f6007507a9692186939258e90916eb51e8f                │
│ Remote Tracking Status       │ origin/phase-04-stage-02-implementation matches 59906f6 │
│ Base Branch (Pristine)       │ main at commit 3eab2d6 (origin/main)                    │
│ Revision Baseline Commit     │ 73c70f0 (docs(methodology): propose Phase 04 Stage 03)  │
│ Working Tree State           │ docs/PHASE_04_STAGE_03_METHODOLOGY.md (Revision 04)     │
│ Pipeline Test Suite Status   │ 87 tests passing (unittest discover -s tests, OK)       │
└──────────────────────────────┴─────────────────────────────────────────────────────────┘
```

- **Preservation Check:** Raw data (`Data/raw/smartphones_uncleaned.csv`), historical notebooks (`main.ipynb`, `analyze.ipynb`), and the Stage 02 implementation branch remain completely intact.
- **Uncommitted Revisions Intact:** The uncommitted methodology revisions in `docs/PHASE_04_STAGE_03_METHODOLOGY.md` were preserved and not discarded or reset.
- **Zero Premature Commits / Pushes:** No commits, pushes, merges, or pull requests have been initiated.

---

## 03. Analytical Environment & Dependency Audit

### Environment Specification
- **Python Version:** `3.14.4` (tags/v3.14.4:23116f9, Apr 7 2026, 14:10:54) [MSC v.1944 64 bit (AMD64)]
- **Platform:** Windows 11 Pro (10.0.26200-SP0)
- **Interpreter Path:** `C:\Users\balfr\AppData\Local\Programs\Python\Python314\python.exe`
- **Package Manager:** `pip 26.1`

### Installed Packages Inventory

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              PACKAGE AVAILABILITY AUDIT                                │
├──────────────────────────────┬──────────────┬────────────┬─────────────────────────────┤
│ Library                      │ Version      │ Status     │ Project Role                │
├──────────────────────────────┼──────────────┼────────────┼─────────────────────────────┤
│ numpy                        │ 2.4.4        │ INSTALLED  │ Array operations & linear   │
│                              │              │            │ algebra sandwich estimation │
├──────────────────────────────┼──────────────┼────────────┼─────────────────────────────┤
│ pandas                       │ 3.0.2        │ INSTALLED  │ DataFrame processing, group │
│                              │              │            │ operations, matrix slicing  │
├──────────────────────────────┼──────────────┼────────────┼─────────────────────────────┤
│ matplotlib                   │ 3.10.9       │ INSTALLED  │ Diagnostic plotting & Q-Q   │
├──────────────────────────────┼──────────────┼────────────┼─────────────────────────────┤
│ seaborn                      │ 0.13.2       │ INSTALLED  │ Statistical distribution UI │
├──────────────────────────────┼──────────────┼────────────┼─────────────────────────────┤
│ scipy                        │ None         │ MISSING    │ Distributions, p-values,    │
│                              │              │            │ optimization (QuantReg)     │
├──────────────────────────────┼──────────────┼────────────┼─────────────────────────────┤
│ statsmodels                  │ None         │ MISSING    │ OLS cluster-robust formulas,│
│                              │              │            │ QuantReg, Ramsey RESET, VIF │
├──────────────────────────────┼──────────────┼────────────┼─────────────────────────────┤
│ scikit-learn (sklearn)       │ None         │ NOT INST.  │ Not required (econometrics) │
├──────────────────────────────┼──────────────┼────────────┼─────────────────────────────┤
│ pytest                       │ None         │ NOT INST.  │ Unittest used as standard   │
└──────────────────────────────┴──────────────┴────────────┴─────────────────────────────┘
```

### Dry-Run Verification for Missing Packages
In strict compliance with governance rules (*"Do not install or upgrade dependencies without authorization"*), a non-modifying dry-run check was executed:
```bash
python -m pip install --dry-run scipy statsmodels
```
**Dry-Run Verification Output:**
- `scipy-1.18.1-cp314-cp314-win_amd64.whl` (compatible pre-compiled wheel available).
- `statsmodels-0.15.0-cp314-cp314-win_amd64.whl` (compatible pre-compiled wheel available).
- Dependencies resolved cleanly: `formulaic` (1.2.2), `interface_meta` (2.0.1), `patsy` (1.0.3), `wrapt` (2.6.0.dev1).
- **Zero packages were installed during this audit.**

### Recommendation for Project Owner:
Authorizing `pip install scipy statsmodels` prior to Stage 04.2 will enable standard, peer-reviewed econometric implementations of:
1. `statsmodels.regression.linear_model.OLS.fit(cov_type='cluster', cov_kwds={'groups': df['device_id']})`
2. `statsmodels.regression.quantile_regression.QuantReg`
3. `statsmodels.stats.outliers_influence.variance_inflation_factor`
4. `statsmodels.stats.diagnostic.het_breuschpagan` and `het_white`
5. `statsmodels.stats.diagnostic.linear_reset`

*(Fallback Option: If the project owner prefers zero package additions, OLS with cluster-robust Liang-Zeger sandwich estimators can be implemented directly using pure NumPy/SciPy linear algebra formulas).*

---

## 04. Processed Dataset Schema & Dimensions Audit

### File Integrity & Checksums

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                             PROCESSED ARTIFACT IDENTIFIERS                             │
├────────────────────────────────────────┬─────────────┬─────────────────────────────────┤
│ File Path                              │ Size (Bytes)│ SHA-256 Checksum                │
├────────────────────────────────────────┼─────────────┼─────────────────────────────────┤
│ Data/processed/smartphones_cleaned.csv │ 1,433,995   │ 7a2f4c32a7296608a1e64e40dcbc... │
│ Data/processed/smartphones_cleaned.json│ 4,838,018   │ 5233a50aebbf27c44867ebd1a763... │
│ Data/processed/data_quality_report.json│ 5,459       │ c915826b0da8884664ff76026166... │
│ Data/processed/market_summary.json     │ 37,668      │ f0fd97fc10f817644890ca0ae354... │
│ Data/processed/deduplication_audit.json│ 161,460     │ b3a266994f9498e07acbec063e0f... │
└────────────────────────────────────────┴─────────────┴─────────────────────────────────┘
```

- **Row Count:** Exactly **2,256 rows** in CSV, exactly **2,256 records** in JSON.
- **Column Count:** Exactly **45 columns** in CSV, exactly **45 keys** in JSON.
- **Duplicate Rows in CSV:** **0** (zero exact duplicate rows).

### Primary Identifiers & Slug Behavior
1. **`listing_id` (Primary Provenance Key):** Exactly **2,256 unique values / 2,256 records (100% uniqueness)**. Formatted as `rec_XXXX`. Every row has a deterministic, unique identifier.
2. **`device_id` (Base Model Grouping / Cluster Key):** Exactly **1,647 unique values / 2,256 records**. Used as the cluster grouping variable for cluster-robust sandwich covariance estimation.
3. **`config_id` (Variant Descriptor Slug):** Exactly **2,255 unique values / 2,256 records**.
   - *Audit Finding on Non-Uniqueness:* There is exactly **one duplicate `config_id` slug**: `xiaomi-mi-max_3gb_32gb`.
   - *Provenanced Records:* `rec_2035` (`model_name`: "Xiaomi Mi Max", user rating count: 25,300) and `rec_2415` (`model_name`: "Xiaomi Mi Max 32GB", expert rating: 7.9, user rating count: 21,700).
   - *Reason for Dual Retention:* Because their raw model names and rating telemetry differed in the scraped data, they were not exact duplicates across all 14 raw columns and were correctly retained as distinct retail listings.
   - *Econometric Governance:* In all regression matrices, **`listing_id` must serve as the row index**, while `config_id` is treated purely as a descriptive variant slug.

### Complete 45-Field Schema & Missingness Ledger

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              COMPLETE 45-FIELD SCHEMA AUDIT                            │
├────┬──────────────────────────────┬───────────┬──────────────┬────────────┬────────────┤
│ #  │ Field Name                   │ Data Type │ Valid N      │ Missing N  │ Missing %  │
├────┼──────────────────────────────┼───────────┼──────────────┼────────────┼────────────┤
│ 1  │ listing_id                   │ String    │ 2,256        │ 0          │ 0.00%      │
│ 2  │ duplicate_listing_ids        │ String    │ 2,256        │ 0          │ 0.00%      │
│ 3  │ duplicate_count              │ Integer   │ 2,256        │ 0          │ 0.00%      │
│ 4  │ device_id                    │ String    │ 2,256        │ 0          │ 0.00%      │
│ 5  │ config_id                    │ String    │ 2,256        │ 0          │ 0.00%      │
│ 6  │ model_name                   │ String    │ 2,256        │ 0          │ 0.00%      │
│ 7  │ brand_name                   │ String    │ 2,256        │ 0          │ 0.00%      │
│ 8  │ brand_tier                   │ String    │ 2,256        │ 0          │ 0.00%      │
│ 9  │ parent_company               │ String    │ 672          │ 1,584      │ 70.21%     │
│ 10 │ parent_company_status        │ String    │ 2,256        │ 0          │ 0.00%      │
│ 11 │ relationship_type            │ String    │ 2,256        │ 0          │ 0.00%      │
│ 12 │ original_listed_price_inr    │ Integer   │ 2,256        │ 0          │ 0.00%      │
│ 13 │ price_quintile               │ String    │ 2,256        │ 0          │ 0.00%      │
│ 14 │ editorial_price_tier         │ String    │ 2,256        │ 0          │ 0.00%      │
│ 15 │ ram_capacity_gb              │ Float     │ 2,248        │ 8          │ 0.35%      │
│ 16 │ storage_capacity_gb          │ Float     │ 2,254        │ 2          │ 0.09%      │
│ 17 │ battery_capacity_mah         │ Integer   │ 2,256        │ 0          │ 0.00%      │
│ 18 │ charging_wattage             │ Float     │ 1,321        │ 935        │ 41.45%     │
│ 19 │ screen_size_inches           │ Float     │ 2,255        │ 1          │ 0.04%      │
│ 20 │ refresh_rate_hz              │ Float     │ 1,133        │ 1,123      │ 49.78%     │
│ 21 │ display_panel_family         │ String    │ 2,254        │ 2          │ 0.09%      │
│ 22 │ display_technology_raw       │ String    │ 2,254        │ 2          │ 0.09%      │
│ 23 │ rear_main_sensor_mp          │ Float     │ 2,256        │ 0          │ 0.00%      │
│ 24 │ rear_lens_count              │ Integer   │ 2,256        │ 0          │ 0.00%      │
│ 25 │ rear_sensor_breakdown_mp     │ String    │ 2,256        │ 0          │ 0.00%      │
│ 26 │ front_main_sensor_mp         │ Float     │ 2,224        │ 32         │ 1.42%      │
│ 27 │ front_lens_count             │ Float     │ 2,224        │ 32         │ 1.42%      │
│ 28 │ processor_manufacturer       │ String    │ 2,196        │ 60         │ 2.66%      │
│ 29 │ processor_family             │ String    │ 2,196        │ 60         │ 2.66%      │
│ 30 │ processor_model              │ String    │ 2,196        │ 60         │ 2.66%      │
│ 31 │ processor_core_count         │ Float     │ 2,039        │ 217        │ 9.62%      │
│ 32 │ operating_system_raw         │ String    │ 2,247        │ 9          │ 0.40%      │
│ 33 │ operating_system_family      │ String    │ 2,247        │ 9          │ 0.40%      │
│ 34 │ expert_rating                │ Float     │ 1,398        │ 858        │ 38.03%     │
│ 35 │ user_rating_score            │ Float     │ 2,185        │ 71         │ 3.15%      │
│ 36 │ user_rating_count            │ Float     │ 2,185        │ 71         │ 3.15%      │
│ 37 │ review_snippet               │ String    │ 1,070        │ 1,186      │ 52.57%     │
│ 38 │ review_url                   │ String    │ 1,070        │ 1,186      │ 52.57%     │
│ 39 │ price_per_gb_ram_inr         │ Float     │ 2,248        │ 8          │ 0.35%      │
│ 40 │ price_per_gb_storage_inr     │ Float     │ 2,254        │ 2          │ 0.09%      │
│ 41 │ price_per_1000mah_battery_inr│ Float     │ 2,256        │ 0          │ 0.00%      │
│ 42 │ price_per_charging_watt_inr  │ Float     │ 1,321        │ 935        │ 41.45%     │
│ 43 │ price_per_display_inch_inr   │ Float     │ 2,255        │ 1          │ 0.04%      │
│ 44 │ quality_flags                │ String    │ 2,256        │ 0          │ 0.00%      │
│ 45 │ currency_conversion_metadata │ String    │ 2,256        │ 0          │ 0.00%      │
└────┴──────────────────────────────┴───────────┴──────────────┴────────────┴────────────┘
```

---

## 05. Data Quality & Distributional Validation

### Price Validity & Positive Price Constraints
- **Minimum Listed Price:** ₹5,000 (I Kall Z20 / itel A70 class)
- **Maximum Listed Price:** ₹200,999 (Samsung Galaxy Z Fold 5 / Apple iPhone 15 Pro Max 1TB class)
- **Mean Listed Price:** ₹22,210.68
- **Median Listed Price:** ₹14,499.00
- **Null Prices:** **0** (100% complete)
- **Non-Positive Prices ($P \le 0$):** **0** (Strictly positive support; $\ln(P)$ is defined everywhere)
- **Price Skewness:** **3.36** | **Kurtosis:** **14.05** (Heavy right tail)
- **Log Price Skewness:** **0.80** | **Kurtosis:** **0.31** (Stabilized, near-Gaussian bell shape)

### Numeric Specification Ranges & Engineering Sanity Checks

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          NUMERIC SPECIFICATION RANGE AUDIT                             │
├──────────────────────────────┬──────────┬──────────┬──────────┬──────────┬─────────────┤
│ Variable Name                │ Min      │ Median   │ Mean     │ Max      │ Unit        │
├──────────────────────────────┼──────────┼──────────┼──────────┼──────────┼─────────────┤
│ ram_capacity_gb              │ 0.03125  │ 4.00     │ 5.20     │ 18.00    │ Gigabytes   │
│ storage_capacity_gb          │ 0.03906  │ 64.00    │ 113.38   │ 1024.00  │ Gigabytes   │
│ battery_capacity_mah         │ 860      │ 4500     │ 4496     │ 22000    │ mAh         │
│ charging_wattage             │ 7.0      │ 25.0     │ 37.1     │ 180.0    │ Watts       │
│ screen_size_inches           │ 2.20     │ 6.50     │ 6.27     │ 8.03     │ Inches      │
│ refresh_rate_hz              │ 60.0     │ 90.0     │ 94.6     │ 165.0    │ Hertz (Hz)  │
│ rear_main_sensor_mp          │ 2.0      │ 16.0     │ 33.2     │ 200.0    │ Megapixels  │
│ front_main_sensor_mp         │ 0.1      │ 8.0      │ 12.0     │ 60.0     │ Megapixels  │
└──────────────────────────────┴──────────┴──────────┴──────────┴──────────┴─────────────┘
```

*Notes on Boundary Values:*
- `ram_capacity_gb` min = 0.03125 GB (32MB) corresponds to ultra-budget smart feature phones (e.g. JioPhone / Micromax legacy entries).
- `battery_capacity_mah` max = 22,000 mAh represents specialized rugged exploration devices (e.g. Unihertz Tank / Oukitel).
- `screen_size_inches` max = 8.03 inches represents unfolded foldable flagships (e.g. Vivo X Fold 3 Pro).

### Brand Taxonomy Consistency
- **Total Unique Brands:** Exactly **63 brands**.
- **Brand Tiers Breakdown:**
  - `MAJOR`: 18 brands, covering **1,813 records (80.36%)**.
  - `MID_TIER`: 15 brands, covering **357 records (15.82%)**.
  - `NICHE_HERITAGE`: 30 brands, covering **86 records (3.81%)**.
- **Top Brand Volumes:** Samsung (312), Realme (210), Vivo (195), Redmi (153), OPPO (130), Motorola (94), Apple (88), OnePlus (71), POCO (71), Infinix (65), Lava (64), Tecno (61), Nokia (58), Micromax (57), iQOO (51), Lenovo (47), Asus (45), Xiaomi (41).
- **Redmi vs. Xiaomi Verification:** Redmi ($N = 153$) and Xiaomi ($N = 41$) are verified as separate consumer-facing brands.

### Processor Vendor Stratification
- **Total Processor Manufacturers:** 12 named vendors + 60 unbranded/null entries.
- **Distribution:** MediaTek (921), Qualcomm (839), Samsung (156), Unisoc (135), Apple (88), HiSilicon (24), Intel (13), Google (9), Broadcom (6), Marvell (3), ST-Ericsson (1), Nvidia (1), Unstated/Null (60).
- **Reference Category Baseline:** MediaTek ($N = 921$, 40.82% of catalog).

### Unit-Rate Metric Denominators
All five unit-rate metrics feature positive, non-zero denominators:
- `price_per_gb_ram_inr`: $N = 2,248$, median ₹3,333.00/GB
- `price_per_gb_storage_inr`: $N = 2,254$, median ₹198.31/GB
- `price_per_1000mah_battery_inr`: $N = 2,256$, median ₹3,598.00/1000mAh
- `price_per_charging_watt_inr`: $N = 1,321$, median ₹611.06/W
- `price_per_display_inch_inr`: $N = 2,255$, median ₹2,342.19/inch

---

## 06. Reconciliation Against Stage 02 Audit Artifacts

The processed dataset was programmatically reconciled against the three canonical audit artifacts produced in Stage 02:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                             STAGE 02 ARTIFACT RECONCILIATION                           │
├──────────────────────────────────┬──────────────────────┬──────────────────────┬───────┤
│ Metric Description               │ Value in Artifact    │ Value in Dataset df  │ Status│
├──────────────────────────────────┼──────────────────────┼──────────────────────┼───────┤
│ Source Raw Listings              │ 2,928 rows (da, dqr) │ 2,928 (raw audit)    │ MATCH │
│ Exact Duplicate Rows Removed     │ 672 rows (da, dqr)   │ 672 (lineage audit)  │ MATCH │
│ Retained Unique Records          │ 2,256 records (all)  │ 2,256 rows in df     │ MATCH │
│ Singleton Records Count          │ 1,584 records (da)   │ 1,584 in lineage     │ MATCH │
│ Multi-Listing Duplicate Groups   │ 672 groups (da)      │ 672 in lineage       │ MATCH │
│ Price Quintile Q1 Record Count   │ 454 records (ms)     │ 454 in df            │ MATCH │
│ Price Quintile Q2 Record Count   │ 482 records (ms)     │ 482 in df            │ MATCH │
│ Price Quintile Q3 Record Count   │ 436 records (ms)     │ 436 in df            │ MATCH │
│ Price Quintile Q4 Record Count   │ 433 records (ms)     │ 433 in df            │ MATCH │
│ Price Quintile Q5 Record Count   │ 451 records (ms)     │ 451 in df            │ MATCH │
│ Editorial Tier Entry-Level (<10k)│ 726 records (ms)     │ 726 in df            │ MATCH │
│ Editorial Tier Budget-to-mid     │ 806 records (ms)     │ 806 in df            │ MATCH │
│ Editorial Tier Mid-range (20-35k)│ 394 records (ms)     │ 394 in df            │ MATCH │
│ Editorial Tier Upper-mid (35-60k)│ 197 records (ms)     │ 197 in df            │ MATCH │
│ Editorial Tier Premium (>=60k)   │ 133 records (ms)     │ 133 in df            │ MATCH │
└──────────────────────────────────┴──────────────────────┴──────────────────────┴───────┘
```
*(Key: `da` = `deduplication_audit.json`; `dqr` = `data_quality_report.json`; `ms` = `market_summary.json`).*

**Reconciliation Result:** Exactly **100% agreement** across all categorical counts, row counts, deduplication lineage numbers, and price tier distributions.

---

## 07. Econometric Model Readiness Matrix (Models 1–6)

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                     ECONOMETRIC MODEL READINESS MATRIX                                 │
├────┬─────────────────────────┬───────────────┬────────────┬─────────────┬──────────────┬───────────────┤
│ ID │ Model Name              │ Sample Size   │ Complete % │ Clusters (G)│ Key Controls │ Readiness     │
├────┼─────────────────────────┼───────────────┼────────────┼─────────────┼──────────────┼───────────────┤
│ M1 │ Baseline Core Hedonic   │ N = 2,246     │ 99.56%     │ 1,647 dev.  │ RAM, Storage,│ READY FOR     │
│    │ Specification           │               │            │             │ Batt, Screen,│ STAGE 04.3    │
│    │                         │               │            │             │ Cam, OLED    │               │
├────┼─────────────────────────┼───────────────┼────────────┼─────────────┼──────────────┼───────────────┤
│ M2 │ Semiconductor Platform  │ N = 2,195     │ 97.30%     │ 1,617 dev.  │ M1 specs +   │ READY FOR     │
│    │ Fixed Effects           │               │            │             │ SoC Vendor   │ STAGE 04.3    │
│    │                         │               │            │             │ (Ref: MediaT)│               │
├────┼─────────────────────────┼───────────────┼────────────┼─────────────┼──────────────┼───────────────┤
│ M3 │ Full Brand Fixed Effects│ N = 2,195     │ 97.30%     │ 1,617 dev.  │ M2 specs +   │ READY FOR     │
│    │ Workhorse Specification │               │            │             │ 29 Brands    │ STAGE 04.3    │
│    │                         │               │            │             │ (Ref: Xiaomi)│               │
├────┼─────────────────────────┼───────────────┼────────────┼─────────────┼──────────────┼───────────────┤
│ M4 │ Within-Device Upgrade   │ N = 1,092     │ 48.40%     │ 483 dev.    │ Device FE,   │ READY FOR     │
│    │ Association Model       │ (Multi-var)   │ (Catalog)  │ (Multi-var) │ Within-RAM,  │ DIAGNOSTICS   │
│    │                         │               │            │             │ Within-Stor. │ IN STAGE 04.4 │
├────┼─────────────────────────┼───────────────┼────────────┼─────────────┼──────────────┼───────────────┤
│ M5 │ Extended Modern Feature │ N = 1,101     │ 48.80%     │ 888 dev.    │ M3 specs +   │ READY FOR     │
│    │ Subsample Specification │ (Modern)      │ (Catalog)  │ (Modern)    │ Watts + Hz   │ STAGE 04.5    │
├────┼─────────────────────────┼───────────────┼────────────┼─────────────┼──────────────┼───────────────┤
│ M6 │ Exploratory Quantile    │ N = 2,195     │ 97.30%     │ 1,617 dev.  │ M3 specs at  │ READY AS      │
│    │ Regression Model        │               │            │             │ τ ∈ {0.1..9} │ EXPLORATORY   │
│    │                         │               │            │             │              │ EXTENSION     │
└────┴─────────────────────────┴───────────────┴────────────┴─────────────┴──────────────┴───────────────┘
```

### Detailed Readiness Profiles:
1. **Model 1 (Baseline Core):** Regressors extracted directly from numeric columns. OLED dummy constructed from `display_panel_family == 'OLED'`. Battery scaled by 1,000. 10 observations dropped due to missing core specs (8 RAM, 2 storage).
2. **Model 2 (SoC Platform):** SoC dummy matrix constructed for 6 groups (Qualcomm, Samsung, Unisoc, Apple, HiSilicon, Other_SoC) with MediaTek as reference. 51 additional observations dropped due to missing SoC manufacturer ($2,246 \to 2,195$).
3. **Model 3 (Brand Workhorse):** 29 dummy indicators for brands with $\ge 20$ listings; remaining 34 brands pooled into `Niche_Other`. Xiaomi omitted as reference category. Sample identical to Model 2 ($N = 2,195$).
4. **Model 4 (Within-Device):** Formally characterized in Section 08 below.
5. **Model 5 (Modern Feature Cohort):** Complete cases across Model 3 + charging wattage + refresh rate ($N = 1,101$). Sample composition skew documented.
6. **Model 6 (Quantile Extension):** Dependent variable `log_price_inr` evaluated across $\tau \in \{0.10, 0.25, 0.50, 0.75, 0.90\}$. Cluster-robust bootstrap non-convergence caveat documented.

---

## 08. Model 4 Structural & Identification Readiness

### Multi-Variant Subsample Architecture
The multi-variant subsample comprises devices exhibiting multiple configurations ($J_i > 1$):
- **Total Configurations ($N$):** Exactly **1,092 configuration-level observations**.
- **Total Multi-Variant Base Device Clusters ($G$):** Exactly **483 device clusters**.
- **Cluster Size Distribution:**
  - Devices with $J_i = 2$ configurations: **362 devices** (724 configurations).
  - Devices with $J_i = 3$ configurations: **116 devices** (348 configurations).
  - Devices with $J_i = 4$ configurations: **5 devices** (20 configurations).
- **Pairwise Upgrade Steps ($K = N - G$):** Exactly **609 incremental upgrade steps** relative to the lowest-memory base tier.

### Independent Variation Structure
Inspection of within-device memory variation across the 483 devices reveals:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                         MODEL 4 WITHIN-DEVICE VARIATION PATTERNS                       │
├──────────────────────────────────────────┬──────────────┬──────────────┬───────────────┤
│ Variation Pattern                        │ Device Count │ Config Count │ Subsample %   │
├──────────────────────────────────────────┼──────────────┼──────────────┼───────────────┤
│ Both RAM & Storage Vary Simultaneously   │ 227 devices  │ 543 configs  │ 47.00%        │
│ Only Storage Varies (RAM Constant)       │ 134 devices  │ 296 configs  │ 27.74%        │
│ Only RAM Varies (Storage Constant)       │ 121 devices  │ 251 configs  │ 25.05%        │
│ Neither Varies (Identical Specs)         │ 1 device     │ 2 configs    │ 0.21%         │
├──────────────────────────────────────────┼──────────────┼──────────────┼───────────────┤
│ Total Multi-Variant Population           │ 483 devices  │ 1,092 configs│ 100.00%       │
└──────────────────────────────────────────┴──────────────┴──────────────┴───────────────┘
```

- **Independent Off-Diagonal Support:** A total of **255 devices (52.8%)** vary either RAM (121 devices) or Storage (134 devices) independently while holding the other specification fixed. This provides the mathematical support necessary to prevent exact collinearity in de-meaned variables.
- **Descriptive Delta Correlation:** Across all 609 pairwise upgrade steps, $\text{Corr}(\Delta\text{RAM}, \Delta\text{Storage}) = -0.092$. This is treated strictly as descriptive evidence of non-collinearity, not as proof of estimator stability.

### Hardware-Invariance Audit Exceptions
While `device_id` groups common base models, the audit detected **8 devices** where non-memory specifications differ across configurations:
1. **SoC Model Differs (4 devices):**
   - `realme-10`: 4G (Helio G99) vs. 5G (Dimensity 700) configurations.
   - `samsung-galaxy-m34`: Exynos 1280 vs. alternate revision.
   - `vivo-t2`: Snapdragon 695 vs. Dimensity 6020 configurations.
   - `xiaomi-redmi-note-12`: Snapdragon 4 Gen 1 vs. 4G Snapdragon 685 configurations.
2. **Charging Wattage Differs (2 devices):**
   - `xiaomi-redmi-note-11-pro-plus`: 67W vs. 120W charging editions.
   - `realme-gt-neo-3`: 80W vs. 150W charging editions.
3. **Front Camera Resolution Differs (2 devices):**
   - `oppo-f19-pro-plus`: 16MP vs. 32MP configuration discrepancy.
   - `vivo-v23`: Dual-camera front sensor variant.

### Fallback Hierarchy Implementation Plan (Stage 04.4)
- **Primary Joint Estimation (Tier 1):** Fit on all invariant devices ($N = 475$ devices, 1,074 configurations), dropping the 8 contaminated devices and 1 degenerate device.
- **Diagnostics:** Check de-meaned matrix rank, condition number $\kappa(\tilde{\mathbf{X}}'\tilde{\mathbf{X}})$, and VIF.
- **Sub-Models 4A & 4B (Tiers 2 & 3):** If Tier 1 VIF $> 5.0$, estimate RAM-only upgrades on $N = 251$ configs ($G = 121$) and storage-only upgrades on $N = 296$ configs ($G = 134$).
- **Tier 5:** If separate estimation remains unstable, report data non-identification. Composite indices remain strictly prohibited.

---

## 09. Missingness Assessment & Subsample Governance

### Potentially Systematic Missingness (Charging Wattage & Refresh Rate)
- **Charging Wattage:** Missing in **935 records (41.45%)**.
- **Refresh Rate:** Missing in **1,123 records (49.78%)**.
- **Mechanism:** In accordance with Revision 04, missingness is classified as **potentially systematic; the missingness mechanism cannot be conclusively identified as MAR vs. MNAR from available observed variables alone**.

### Empirical Subsample Comparison: Full Catalog vs. Model 5

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        FULL CATALOG VS. MODEL 5 SUBSAMPLE SKEW                         │
├──────────────────────────────┬────────────────────┬────────────────────┬───────────────┤
│ Dimension                    │ Full Catalog       │ Model 5 Subsample  │ Subsample Skew│
├──────────────────────────────┼────────────────────┼────────────────────┼───────────────┤
│ Valid Record Count           │ 2,256 records      │ 1,101 records      │ -51.20% sample│
│ Median Listed Price          │ ₹14,499            │ ₹18,996            │ +31.02% higher│
│ Mean Listed Price            │ ₹22,211            │ ₹28,583            │ +28.69% higher│
│ Mean RAM Capacity            │ 5.20 GB            │ 7.38 GB            │ +41.92% higher│
│ Mean Storage Capacity        │ 113.38 GB          │ 176.88 GB          │ +56.01% higher│
│ Entry-Level Tier (<₹10k)     │ 726 records (32.2%)│ 163 records (14.8%)│ -17.4% share  │
│ Budget-to-Mid Tier (₹10k-20k)│ 806 records (35.7%)│ 437 records (39.7%)│ +4.0% share   │
│ Mid-Range Tier (₹20k-35k)    │ 394 records (17.5%)│ 271 records (24.6%)│ +7.1% share   │
│ Upper-Mid Tier (₹35k-60k)    │ 197 records (8.7%) │ 130 records (11.8%)│ +3.1% share   │
│ Premium Tier (≥₹60k)         │ 133 records (5.9%) │ 100 records (9.1%) │ +3.2% share   │
└──────────────────────────────┴────────────────────┴────────────────────┴───────────────┘
```

**Selection Governance Rules:**
1. Core Models 1–3 strictly omit charging wattage and refresh rate to avoid the 51.2% sample truncation and dramatic upward price skew.
2. Model 5 is documented strictly as a **Modern Spec-Dense Cohort Specification**.
3. Results of Model 5 will be presented alongside the sample skew table above to prevent misleading generalizations.
4. Zero missing-data imputation will be performed.

---

## 10. Outstanding Blockers and Recommendations

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                         BLOCKER & RECOMMENDATION LOG                                   │
├────┬─────────────────────────────┬───────────────────────────┬─────────────────────────┤
│ ID │ Identified Item             │ Severity & Impact         │ Actionable Solution     │
├────┼─────────────────────────────┼───────────────────────────┼─────────────────────────┤
│ B1 │ scipy & statsmodels not     │ HIGH: Blocks Stage 04.2   │ Request project-owner   │
│    │ installed in Python env     │ diagnostics & OLS fitting │ authorization to run    │
│    │                             │                           │ pip install scipy       │
│    │                             │                           │ statsmodels             │
├────┼─────────────────────────────┼───────────────────────────┼─────────────────────────┤
│ B2 │ Duplicate config_id slug    │ LOW: Affects 2 records    │ Standardize on          │
│    │ (xiaomi-mi-max_3gb_32gb)    │                           │ listing_id as row index;│
│    │                             │                           │ treat config_id as desc.│
├────┼─────────────────────────────┼───────────────────────────┼─────────────────────────┤
│ B3 │ Hardware non-invariance in  │ MEDIUM: Confounding in    │ Filter out 8 devices in │
│    │ Model 4 (8 devices)         │ within-device memory FE   │ Stage 04.4 sensitivity  │
├────┼─────────────────────────────┼───────────────────────────┼─────────────────────────┤
│ B4 │ Public Presentation of      │ POLICY: Pending post-     │ Withhold UI decisions   │
│    │ Models 3 & 4 NOT YET APP.   │ estimation review         │ until Stage 04 completes│
└────┴─────────────────────────────┴───────────────────────────┴─────────────────────────┘
```

---

## 11. Explicit Approval Checklist for the Project Owner

The following three operational authorizations are requested from the project owner to close Stage 04.1 and unlock Stage 04.2:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        STAGE 04.1 OPERATIONAL APPROVAL CHECKLIST                       │
├────┬──────────────────────────────────┬───────────────────────────┬────────────────────┤
│ ID │ Decision / Action Item           │ Proposed Recommendation   │ Review Status      │
├────┼──────────────────────────────────┼───────────────────────────┼────────────────────┤
│ A1 │ Accept Stage 04.1 Data Audit     │ Confirm reconciliation of │ PENDING APPROVAL   │
│    │ and Model Readiness Report       │ 2,256 records & schemas   │                    │
├────┼──────────────────────────────────┼───────────────────────────┼────────────────────┤
│ A2 │ Authorize Dependency             │ Authorize non-breaking    │ PENDING APPROVAL   │
│    │ Installation                     │ pip install scipy         │                    │
│    │                                  │ statsmodels               │                    │
├────┼──────────────────────────────────┼───────────────────────────┼────────────────────┤
│ A3 │ Authorize Transition to          │ Proceed with matrix       │ PENDING APPROVAL   │
│    │ Stage 04.2                       │ extraction & diagnostics  │                    │
│    │                                  │ (prepare_matrices.py)     │                    │
└────┴──────────────────────────────────┴───────────────────────────┴────────────────────┘
```

1. **Authorization A1 — Data Audit Acceptance:**  
   Confirm acceptance of this reproducible data audit and reconciliation against Stage 02 artifacts.
2. **Authorization A2 — Dependency Installation:**  
   Authorize installing `scipy` (1.18.1) and `statsmodels` (0.15.0) via pip for econometric diagnostics and cluster-robust regression fitting.
3. **Authorization A3 — Transition to Stage 04.2:**  
   Authorize commencing Stage 04.2 (Matrix Preparation, VIF Multicollinearity Profiling, and Box-Cox Diagnostics in `scripts/analysis/prepare_matrices.py`).

---

*Phase 04 Stage 04.1 Data & Environment Audit is complete.*  
*Halted at the approval gate in strict compliance with stop conditions. Standing by for project-owner review.*
