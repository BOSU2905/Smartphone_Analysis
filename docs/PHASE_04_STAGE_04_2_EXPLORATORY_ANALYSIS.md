# PHASE 04 — STAGE 04.2: EXPLORATORY STATISTICAL ANALYSIS & DIAGNOSTIC PREPARATION REPORT (REVISION 02 FINAL)
## Pre-Estimation Distributional Analysis, Bivariate Profiling, and Econometric Design Matrix Diagnostics

> **PROJECT TITLE:** What Are We Really Paying For When We Buy a Smartphone?  
> **PRODUCT IDENTITY:** Experimental Technical Editorial  
> **DOCUMENT TYPE:** Exploratory Statistical Analysis & Pre-Estimation Diagnostic Report  
> **REVISION:** Revision 02 Final (Methodological Clarifications, Hardware-Invariance Reconciliation & Git Isolation)  
> **AUTHOR / ROLE:** Senior Data Scientist, Applied Econometrician & Software Architect  
> **STATUS:** COMPLETED — PENDING PROJECT OWNER APPROVAL BEFORE STAGE 04.3  
> **TARGET IMPLEMENTATION:** Phase 04 — Stage 04.3 (Core Models 1–3 Estimation)  
> **ACCEPTED BASELINE DATASET:** Stage 02 Canonical Artifacts (Commit `59906f6`)  
> **AUTHORITATIVE METHODOLOGY:** [`docs/PHASE_04_STAGE_03_METHODOLOGY.md`](file:///c:/Smartphone%20Analysis/Smartphone_Analysis/docs/PHASE_04_STAGE_03_METHODOLOGY.md) (Revision 04)  
> **PRE-ESTIMATION DATA AUDIT:** [`docs/PHASE_04_STAGE_04_1_DATA_AUDIT.md`](file:///c:/Smartphone%20Analysis/Smartphone_Analysis/docs/PHASE_04_STAGE_04_1_DATA_AUDIT.md)  
> **ANALYTICAL SCRIPT:** [`scripts/analysis/exploratory_analysis.py`](file:///c:/Smartphone%20Analysis/Smartphone_Analysis/scripts/analysis/exploratory_analysis.py)  
> **ARTIFACT DIRECTORY:** `Data/analytical/` (Dedicated Stage 04 isolation)

---

## 01. Environment, Dependency Manifest & Artifact Provenance

In accordance with project-owner authorization (Decision A2 from Stage 04.1), mathematical dependencies `scipy` and `statsmodels` were installed without upgrading or altering any pre-existing system packages:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              ENVIRONMENT & DEPENDENCY AUDIT                            │
├──────────────────────────────┬──────────────────────────┬──────────────────────────────┤
│ Component                    │ Version / Environment    │ Installation Provenance      │
├──────────────────────────────┼──────────────────────────┼──────────────────────────────┤
│ Python Interpreter           │ 3.14.4 (tags/v3.14.4)    │ Windows 11 Pro AMD64         │
│ numpy                        │ 2.4.4                    │ Pre-existing                 │
│ pandas                       │ 3.0.2                    │ Pre-existing                 │
│ scipy                        │ 1.18.1                   │ Authorized pip wheel install │
│ statsmodels                  │ 0.15.0                   │ Authorized pip wheel install │
│ patsy                        │ 1.0.3                    │ statsmodels dependency       │
│ formulaic                    │ 1.2.2                    │ statsmodels dependency       │
│ interface-meta               │ 2.0.1                    │ statsmodels dependency       │
│ wrapt                        │ 2.6.0.dev1               │ statsmodels dependency       │
│ matplotlib                   │ 3.10.9                   │ Pre-existing                 │
│ seaborn                      │ 0.13.2                   │ Pre-existing                 │
├──────────────────────────────┼──────────────────────────┼──────────────────────────────┤
│ Deterministic Random Seed    │ 42                       │ np.random.seed(42)           │
│ Analytical Output Directory  │ Data/analytical/         │ Dedicated Stage 04 isolation │
└──────────────────────────────┴──────────────────────────┴──────────────────────────────┘
```

### Reproducibility & Artifact Manifest
The exploratory script [`scripts/analysis/exploratory_analysis.py`](file:///c:/Smartphone%20Analysis/Smartphone_Analysis/scripts/analysis/exploratory_analysis.py) was executed deterministically, generating four structured JSON analytical outputs and a machine-readable manifest in `Data/analytical/`:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              STAGE 04.2 ARTIFACT MANIFEST                              │
├────────────────────────────────────────┬─────────────┬─────────────────────────────────┤
│ Artifact Path                          │ Size (Bytes)│ SHA-256 Checksum                │
├────────────────────────────────────────┼─────────────┼─────────────────────────────────┤
│ Data/analytical/exploratory_summary.json│ 13,448     │ 3b8cce796324e534f88c1e0097f2a... │
│ Data/analytical/vif_diagnostics.json   │ 4,014       │ 5011a5d59dde6e959d0587caf65c7... │
│ Data/analytical/model4_within_diagnostics.json│ 10,449│ 5a577860fce9c76a993b563a76155... │
│ Data/analytical/correlation_matrix.json│ 3,358       │ 770af3f3e0f2f50bbc8153de365fe... │
│ Data/analytical/artifact_manifest.json │ 1,334       │ 65a42febecbc14aba3631a6024620... │
└────────────────────────────────────────┴─────────────┴─────────────────────────────────┘
```
- **Source Dataset Verification:** Inputs verified against Stage 02 canonical artifacts:
  - `Data/processed/smartphones_cleaned.csv` (1,433,995 bytes, SHA-256: `7a2f4c32a7296608a1e64e40dcbc77e4de5e9d76454b3c2577c630bebccc09fa`).
  - `Data/processed/smartphones_cleaned.json` (4,838,018 bytes, SHA-256: `5233a50aebbf27c44867ebd1a763dbf96858f4a49ac9276caec03ada66d45ba5`).
- **Pipeline Baseline Health:** All 87 unit and integration tests passed cleanly (`OK`) in 16.913s.

---

## 02. Statistical Testing Terminology & Diagnostic Boundaries

To maintain rigorous scientific precision and avoid ambiguity, a clear methodological boundary is established between exploratory diagnostic tests and confirmatory research hypothesis testing:

1. **Exploratory Diagnostic Statistical Tests Were Performed:**
   - Distributional normality tests: Jarque-Bera test statistics and associated $p$-values computed for raw retail price ($JB = 17,985.4, p < 0.0001$) and log-price ($JB = 250.7, p < 0.0001$).
   - Profile log-likelihood ratio estimation: Box-Cox power transformation parameter estimated at $\hat{\lambda} = -0.4528$.
   - Bivariate association tests: Pearson correlation coefficients and two-tailed significance $p$-values calculated across continuous specifications.
   - Design matrix numerical diagnostics: Full column rank evaluations, condition numbers, and Variance Inflation Factors (VIF) computed to evaluate multicollinearity.
   - None of these diagnostic statistics have been concealed, truncated, or removed.

2. **Confirmatory Research Hypothesis Tests Were NOT Executed:**
   - **Zero confirmatory research hypothesis tests (H1 through H6)** were executed in Stage 04.2.
   - Confirmatory hypothesis testing requires estimating formal econometric regression parameters ($\hat{\beta}_k$, $\hat{\theta}_b$, $\hat{\tau}$-quantiles) with cluster-robust standard errors and evaluating pre-registered economic null hypotheses (e.g., brand premium persistence, battery premium attenuation, nonlinear RAM returns).
   - All confirmatory hypothesis tests are strictly deferred to Stages 04.3 through 04.6.

---

## 03. Price and Log-Price Distributional Analysis

### Comparative Distributional Profiling
The primary dependent variable was profiled on both linear INR levels and natural logarithm scales across all $N = 2,256$ catalog records:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        PRICE VS. LOG-PRICE MOMENT COMPARISON                           │
├──────────────────────────────┬──────────────────────────┬──────────────────────────────┤
│ Metric                       │ Raw Price (INR, ₹)       │ Log-Price (ln(INR))          │
├──────────────────────────────┼──────────────────────────┼──────────────────────────────┤
│ Valid Observations (N)       │ 2,256 (100.0%)           │ 2,256 (100.0%)               │
│ Minimum                      │ ₹5,000.00                │ 8.5172                       │
│ 25th Percentile (p25)        │ ₹8,999.00                │ 9.1049                       │
│ Median (50th Percentile)     │ ₹14,499.00               │ 9.5818                       │
│ Mean                         │ ₹22,210.68               │ 9.6967                       │
│ 75th Percentile (p75)        │ ₹25,499.00               │ 10.1464                      │
│ 90th Percentile (p90)        │ ₹44,999.00               │ 10.7144                      │
│ 99th Percentile (p99)        │ ₹138,675.00              │ 11.8399                      │
│ Maximum                      │ ₹200,999.00              │ 12.2110                      │
├──────────────────────────────┼──────────────────────────┼──────────────────────────────┤
│ Interquartile Range (IQR)    │ ₹16,500.00               │ 1.0415                       │
│ Standard Deviation           │ ₹23,178.69               │ 0.7431                       │
│ Skewness                     │ +3.3543 (Severe right)   │ +0.8005 (Moderately positive)│
│ Excess Kurtosis              │ +14.0177 (Leptokurtic)   │ +0.3114 (Near-mesokurtic)    │
│ Jarque-Bera Test Statistic   │ 17,985.4 (p < 0.0001)    │ 250.7 (p < 0.0001)           │
└──────────────────────────────┴──────────────────────────┴──────────────────────────────┘
```

### Exploratory Box-Cox Analysis & Methodological Justification of Log-Price
- **Estimated Power Parameter:** $\hat{\lambda}_{\text{Box-Cox}} = -0.4528$.
- **Mathematical Significance:** Under an assumption of independent, homoskedastic Gaussian disturbances, profile log-likelihood maximization identifies an inverse square-root transformation ($\approx P^{-0.5} = 1/\sqrt{P}$) as the power function that best eliminates skewness.
- **Methodological Distinction Between Box-Cox and Semi-Log Specification:**
  - The Box-Cox result ($\hat{\lambda} \approx -0.45$) and the selected semi-log specification ($\lambda = 0$) represent fundamentally different analytical considerations:
    1. *Box-Cox Objective:* Purely mathematical symmetry under homoskedasticity. However, hedonic price disturbances across 13 years of smartphones are inherently heteroskedastic. Furthermore, an inverse square-root price variable ($1/\sqrt{P}$) carries zero intuitive economic meaning for consumers, hardware engineers, or OEMs.
    2. *Semi-Log Objective:* Economic interpretability and structural alignment. Transforming price to natural logarithm $\ln(P)$ yields direct, policy-relevant percentage semi-elasticity markups ($100 \times (\exp(\hat{\beta}) - 1)\%$) and models feature premiums multiplicatively rather than additively.
- **Methodological Clarification on Variance Stabilization:**
  - Logarithmic transformation compresses extreme monetary scale disparities across market segments: in raw INR, the standard deviation expands by 23-fold from ₹1,462 in Entry-level to ₹34,613 in Premium, whereas in log-price, standard deviation remains within a bounded range (0.15 to 0.33).
  - **However, homoskedasticity cannot be inferred from skewness reduction or unconditional tier standard deviations alone.**
  - No post-estimation regression residual heteroskedasticity diagnostic (such as White's test or Breusch-Pagan test) can be performed prior to model estimation.
  - Furthermore, as revealed by the Jarque-Bera diagnostic ($JB = 250.7, p < 0.0001$, skewness $+0.8005$), **log-price remains statistically non-normal**. 
  - Standard OLS inference on log-price therefore relies on large-sample asymptotic normality ($N = 2,256$), not exact Gaussian homoskedastic disturbances.
- **Robustness Commitment:** Log-price is selected as the primary workhorse dependent variable strictly because of economic interpretability. Linear price specifications (in INR) will be estimated alongside semi-log specifications as formal robustness checks in Stage 04.3 to ensure that hedonic conclusions are not artifacts of the logarithmic transformation.

---

## 04. Hardware Specification Distribution & Bivariate Association

Every continuous specification was profiled for distributional parameters and bivariate linear association with both raw price and log-price across all valid listings:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              HARDWARE SPECIFICATION DISTRIBUTION PROFILING                            │
├──────────────────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────────────────────┤
│ Specification        │ Valid N  │ Mean     │ Median   │ Min      │ Max      │ Bivariate Correlation    │
│                      │ (%)      │          │          │          │          │ Pearson r (with ln(P))   │
├──────────────────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────────────────────┤
│ ram_capacity_gb      │ 2,248    │ 5.20 GB  │ 4.00 GB  │ 0.031 GB │ 18.00 GB │ r = +0.6477 (p < 0.0001) │
│ storage_capacity_gb  │ 2,254    │ 113.39 GB│ 64.00 GB │ 0.039 GB │ 1024.0 GB│ r = +0.6715 (p < 0.0001) │
│ battery_capacity_mah │ 2,256    │ 4,141 mAh│ 4,500 mAh│ 860 mAh  │ 22000 mAh│ r = +0.1804 (p < 0.0001) │
│ charging_wattage     │ 1,321    │ 36.62 W  │ 25.00 W  │ 7.00 W   │ 180.00 W │ r = +0.4493 (p < 0.0001) │
│ screen_size_inches   │ 2,255    │ 6.08 in  │ 6.50 in  │ 2.20 in  │ 8.03 in  │ r = +0.3429 (p < 0.0001) │
│ refresh_rate_hz      │ 1,133    │ 99.65 Hz │ 90.00 Hz │ 60.00 Hz │ 165.00 Hz│ r = +0.4397 (p < 0.0001) │
│ rear_main_sensor_mp  │ 2,256    │ 34.83 MP │ 16.00 MP │ 2.00 MP  │ 200.00 MP│ r = +0.3556 (p < 0.0001) │
│ front_main_sensor_mp │ 2,224    │ 12.97 MP │ 8.00 MP  │ 0.10 MP  │ 60.00 MP │ r = +0.4425 (p < 0.0001) │
└──────────────────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────────────────────┘
```

### Battery Capacity Empirical Association & Price-Tier Stratification
A rigorous empirical examination of battery capacity traces its relationship with retail price across market segments:

1. **Overall Bivariate Association:**
   - Across the full catalog ($N = 2,256$), battery capacity exhibits a modest positive linear correlation with log-price ($r = +0.1804, p = 6.01 \times 10^{-18}$) and an even weaker correlation with raw price ($r = +0.0776, p = 0.0002$).
2. **Stratified Bivariate Profiling by Price Tier (Artifact: `exploratory_summary.json`):**
   ```
   ┌────────────────────────────────────────────────────────────────────────────────────────┐
   │                     BATTERY CAPACITY STRATIFICATION BY PRICE BRACKET                   │
   ├──────────────────────┬─────────┬──────────────┬─────────────────────────┬──────────────┤
   │ Price Tier           │ Valid N │ Mean Battery │ Pearson r with ln(P)    │ p-value      │
   ├──────────────────────┼─────────┼──────────────┼─────────────────────────┼──────────────┤
   │ Entry-level (<₹10k)  │ 726     │ 3,682 mAh    │ r = +0.4014             │ p = 1.77e-29 │
   │ Budget-to-mid (10-20k│ 806     │ 4,390 mAh    │ r = +0.0460             │ p = 0.192    │
   │ Mid-range (20-35k)   │ 394     │ 4,346 mAh    │ r = -0.0371             │ p = 0.463    │
   │ Upper-mid (35-60k)   │ 197     │ 4,431 mAh    │ r = +0.1228             │ p = 0.086    │
   │ Premium (≥₹60k)      │ 133     │ 4,094 mAh    │ r = +0.0297             │ p = 0.734    │
   ├──────────────────────┼─────────┼──────────────┼─────────────────────────┼──────────────┤
   │ Pooled Sub-₹20,000   │ 1,534   │ 4,054 mAh    │ r = +0.3456             │ p < 0.0001   │
   │ Pooled Above-₹20,000 │ 722     │ 4,324 mAh    │ r = -0.0401             │ p = 0.281    │
   └──────────────────────┴─────────┴──────────────┴─────────────────────────┴──────────────┘
   ```
3. **Methodological Clarifications on Stratification and Significance:**
   - **Conditioning on the Dependent Variable:** Stratifying the catalog by price tier represents explicit selection/truncation on $Y$. In econometric theory, restricting the sample range of $Y$ mechanically reduces its variance and naturally attenuates bivariate correlation coefficients toward zero within narrow price bands.
   - **Not Adjusted Marginal Effects:** These stratified correlations are purely descriptive bivariate slices of raw data. **They must NOT be interpreted as multivariate partial correlations or adjusted marginal effects.** No regression controls were performed in Stage 04.2.
   - **Exploratory Diagnostic p-values:** The reported $p$-values are exploratory diagnostics calculated under naive independent and identically distributed (i.i.d.) assumptions. They do not account for within-device clustering (multiple listings of the same device model) or multiple comparison corrections across slices.
   - **Research Question for Stage 04.3:** Whether battery capacity yields a zero or negative implicit marginal price after holding constant SoC tier, display technology, and RAM is an empirical research hypothesis (Hypothesis H3) to be formally evaluated with cluster-robust standard errors ($\text{CRVE}_1$) in Stage 04.3 multivariate hedonic regressions.

---

## 05. Missingness Analysis and Variable Completeness

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              MISSINGNESS MECHANISM TAXONOMY                            │
├─────────────────────┬──────────────┬──────────────┬────────────────────────────────────┤
│ Variable Name       │ Missing N    │ Missing %    │ Econometric Mechanism / Status     │
├─────────────────────┼──────────────┼──────────────┼────────────────────────────────────┤
│ original_listed_price 0            │ 0.00%        │ Complete ground truth              │
│ battery_capacity_mah│ 0            │ 0.00%        │ Complete ground truth              │
│ rear_main_sensor_mp │ 0            │ 0.00%        │ Complete ground truth              │
│ rear_lens_count     │ 0            │ 0.00%        │ Complete ground truth              │
│ brand_name          │ 0            │ 0.00%        │ Complete ground truth              │
│ screen_size_inches  │ 1            │ 0.04%        │ Low-frequency parser drop (MCAR)   │
│ storage_capacity_gb │ 2            │ 0.09%        │ Low-frequency parser drop (MCAR)   │
│ display_panel_family│ 2            │ 0.09%        │ Unstated display panel (MCAR)      │
│ ram_capacity_gb     │ 8            │ 0.35%        │ Low-frequency parser drop (MCAR)   │
│ processor_mfg       │ 60           │ 2.66%        │ Unbranded legacy SoC (MAR)         │
├─────────────────────┼──────────────┼──────────────┼────────────────────────────────────┤
│ charging_wattage    │ 935          │ 41.45%       │ Potentially systematic (MNAR/MAR)  │
│ refresh_rate_hz     │ 1,123        │ 49.78%       │ Potentially systematic (MNAR/MAR)  │
└─────────────────────┴──────────────┴──────────────┴────────────────────────────────────┘
```

- **Core Spec Completeness:** Dropping records with missing core attributes retains $N = 2,246$ (99.56% of catalog) for Model 1.
- **SoC Completeness:** Dropping 60 unbranded/null processor entries yields $N = 2,195$ (97.30% of catalog) for Models 2, 3, and 6.
- **Zero Imputation Policy:** Zero missing values were imputed.

---

## 06. Brand & Semiconductor Distribution Profiling

### Brand Threshold Sensitivity (63 Total Brands)
- **Primary Threshold ($\ge 20$ listings):** **29 major brands covering 2,120 records (93.97%)**. Exactly 34 niche brands covering 136 records (6.03%) are pooled into `Niche_Other`.
- **Sensitivity Threshold A ($\ge 10$ listings):** **33 major brands covering 2,170 records (96.19%)**.
- **Sensitivity Threshold B ($\ge 30$ listings):** **23 major brands covering 1,982 records (87.85%)**.
- **Reference Brand Baseline:** `Xiaomi` ($N = 41$, Mean price: ₹33,829; Median price: ₹29,999) provisionally designated as reference baseline ($\theta_{\text{Xiaomi}} = 0$).
- **Redmi Entity Separation:** `Redmi` ($N = 153$, Mean price: ₹13,446; Median price: ₹11,999) verified as a separate categorical entity in accordance with approved methodology.

### Semiconductor Vendor Stratification
- **Reference Baseline:** `MediaTek` ($N = 921$, 40.82% of catalog; $\beta_{\text{SoC:MediaTek}} = 0$).
- **Major Categorical Dummies:** Qualcomm ($N = 839$), Samsung Exynos ($N = 156$), Unisoc ($N = 135$), HiSilicon Kirin ($N = 24$).
- **Pooled Low-Volume Group (`Other_SoC`):** Exactly **33 records (1.46%)** pooling Intel ($N = 13$), Google Tensor ($N = 9$), Broadcom ($N = 6$), Marvell ($N = 3$), ST-Ericsson ($N = 1$), Nvidia ($N = 1$).
- **Apple Silicon Structure:** Handled via structural collinearity resolution detailed in Section 08.

---

## 07. Preliminary Specification Correlation Matrix

Pairwise Pearson correlation matrix ($N = 2,222$ complete cases across continuous specifications; Artifact: `correlation_matrix.json`):

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              PAIRWISE PEARSON CORRELATION MATRIX                                       │
├──────────────────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬───────────────┤
│ Regressor            │ RAM (GB) │ Storage  │ Battery  │ Screen   │ Rear MP  │ Front MP │ ln(Price)     │
├──────────────────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼───────────────┤
│ ram_capacity_gb      │ 1.0000   │ 0.7367   │ 0.5407   │ 0.6840   │ 0.6421   │ 0.6566   │ +0.6477       │
│ storage_capacity_gb  │ 0.7367   │ 1.0000   │ 0.3567   │ 0.5126   │ 0.4843   │ 0.4734   │ +0.6715       │
│ battery_capacity_mah │ 0.5407   │ 0.3567   │ 1.0000   │ 0.7645   │ 0.4971   │ 0.3753   │ +0.1804       │
│ screen_size_inches   │ 0.6840   │ 0.5126   │ 0.7645   │ 1.0000   │ 0.5634   │ 0.5033   │ +0.3429       │
│ rear_main_sensor_mp  │ 0.6421   │ 0.4843   │ 0.4971   │ 0.5634   │ 1.0000   │ 0.5187   │ +0.3556       │
│ front_main_sensor_mp │ 0.6566   │ 0.4734   │ 0.3753   │ 0.5033   │ 0.5187   │ 1.0000   │ +0.4425       │
└──────────────────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴───────────────┘
```

- RAM and Storage exhibit substantial correlation ($r = 0.7367$), reflecting OEM component tier bundling.
- Screen size correlates heavily with Battery ($r = 0.7645$) and RAM ($r = 0.6840$), reflecting physical chassis scaling.
- These moderate-to-high correlations mandate formal Variance Inflation Factor (VIF) diagnostics to ensure multivariate parameter separability.

---

## 08. Model 1–3 Design Matrix Diagnostics & Apple Collinearity Resolution

### VIF Pre-Screening Summary

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              VIF PRE-SCREENING SUMMARY TABLE                           │
├────┬─────────────────────────┬───────────────┬────────────┬────────────────────────────┤
│ ID │ Model Specification     │ Sample Size   │ Max VIF    │ Design Matrix Stability    │
├────┼─────────────────────────┼───────────────┼────────────┼────────────────────────────┤
│ M1 │ Baseline Core Hedonic   │ N = 2,246     │ 4.07 (RAM) │ STABLE (All VIFs < 5.0)    │
│ M2 │ Core + SoC Dummies      │ N = 2,195     │ 4.31 (RAM) │ STABLE (All VIFs < 5.0)    │
│ M3 │ Core + SoC + Brand      │ N = 2,195     │ ~10^15     │ STRUCTURAL RANK DEFICIENCY │
│    │ (Unadjusted Design)     │               │            │ (Exact Apple Collinearity) │
├────┼─────────────────────────┼───────────────┼────────────┼────────────────────────────┤
│ M3 │ Core + SoC + Brand      │ N = 2,195     │ 8.37       │ FULL COLUMN RANK (41/41)   │
│ Adj│ (Adjusted: soc_Apple rm)│               │ (Samsung)  │ STABLE (All VIFs < 10.0)   │
└────┴─────────────────────────┴───────────────┴────────────┴────────────────────────────┘
```

### Detailed Feature VIF Breakdown:
- **Model 1 (Core Hedonic, $N = 2,246$):** `ram_capacity_gb` (**4.07**), `screen_size_inches` (**3.47**), `battery_thousands` (**2.69**), `storage_capacity_gb` (**2.25**), `rear_lens_count` (**2.19**), `rear_main_sensor_mp` (**1.97**), `is_oled` (**1.74**). All VIFs are strictly $< 5.0$.
- **Model 2 (Semiconductor Fixed Effects, $N = 2,195$):** `ram_capacity_gb` (**4.31**), `screen_size_inches` (**3.69**), `battery_thousands` (**2.71**), `storage_capacity_gb` (**2.54**), `rear_lens_count` (**2.30**), `rear_main_sensor_mp` (**2.01**), `is_oled` (**1.93**). Silicon dummies: Qualcomm (**1.30**), Apple (**1.31**), Samsung (**1.22**), Unisoc (**1.13**), Other_SoC (**1.06**), HiSilicon (**1.03**). All VIFs $< 5.0$.

### Apple Structural Collinearity Discovery & Econometric Analysis
When both brand dummies and semiconductor vendor dummies were included simultaneously in Model 3, `statsmodels` detected rank deficiency and triggered a `SingularMatrixWarning` with:
$$\text{VIF}(\text{soc\_Apple}) = 1.00 \times 10^{15}, \quad \text{VIF}(\text{brand\_Apple}) = 1.00 \times 10^{15}$$

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        STRUCTURAL REALITY: APPLE VERTICAL INTEGRATION                  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ In the smartphone industry, Apple Silicon (A-series bionic chips) is 100% proprietary  │
│ to Apple Inc. Zero non-Apple OEMs (Samsung, Xiaomi, Vivo, etc.) license Apple chips.   │
│ Conversely, 100% of Apple smartphones in the empirical dataset utilize Apple Silicon;  │
│ zero Apple devices utilize Qualcomm, MediaTek, Samsung Exynos, or Unisoc processors.  │
│                                                                                        │
│ Mathematically: 1{Brand = Apple} ≡ 1{SoC = Apple} for every single listing in the data.│
│                                                                                        │
│ Econometric Consequence: The design matrix possesses an exact linear column dependency.│
│ The parameters β_{SoC:Apple} and θ_{Brand:Apple} cannot be separately identified.      │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Approved Econometric Resolution for Model 3:
1. **Omitted Column:** `soc_Apple` is explicitly omitted from the semiconductor dummy block.
2. **Retained Column:** `brand_Apple` is retained in the brand dummy block.
3. **Identification Caveat & Scope of Parameter:**
   - **This adjustment does NOT separate the Apple Silicon hardware effect from the Apple brand effect.**
   - Because of 100% vertical integration, the two effects are fundamentally inseparable in observational retail data.
   - The estimated coefficient on `brand_Apple` must be explicitly interpreted as the **compound composite effect** of Apple brand equity, the proprietary iOS operating system ecosystem, and Apple's custom silicon platform.
4. **Reference Categories:**
   - Semiconductor baseline: `MediaTek` ($\beta_{\text{SoC:MediaTek}} = 0$). Remaining silicon dummies (Qualcomm, Samsung Exynos, Unisoc, HiSilicon Kirin, Other_SoC) measure the marginal pricing differential of third-party silicon relative to MediaTek across non-vertically integrated Android OEMs.
   - Brand baseline: `Xiaomi` ($\theta_{\text{Brand:Xiaomi}} = 0$).
5. **Rank and Condition Verification:**
   - The adjusted Model 3 design matrix contains exactly **41 columns** (Intercept + 7 Core Hardware Specs + 5 Third-Party SoC Dummies + 28 Major Brand Dummies).
   - The column rank of the adjusted design matrix is **exactly 41 (Full Column Rank)**.
   - Highest VIFs in Adjusted Model 3: Samsung (**8.37**, reflecting its 14% catalog dominance), Realme (**5.76**), Vivo (**5.43**), Screen size (**4.71**), RAM (**4.67**), Redmi (**4.52**), Niche_Other (**4.20**), OPPO (**4.12**), Apple (**3.59**), Motorola (**3.19**). All remaining 21 regressors have $\text{VIF} < 3.0$.

---

## 09. Model 4 Within-Device Diagnostics & Hardware-Invariance Reconciliation

### Multi-Variant Population & Variation Distribution
```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        MODEL 4 WITHIN-DEVICE POPULATION PROFILE                        │
├──────────────────────────────────────────┬─────────────────────────────────────────────┤
│ Diagnostic Dimension                     │ Verified Empirical Value                    │
├──────────────────────────────────────────┼─────────────────────────────────────────────┤
│ Total Multi-Variant Configurations (N)   │ Exactly 1,092 observations                  │
│ Total Device Clusters (G)                │ Exactly 483 base device models              │
│ Available Degrees of Freedom (K = N - G) │ Exactly 609 incremental upgrade steps       │
├──────────────────────────────────────────┼─────────────────────────────────────────────┤
│ Both RAM & Storage Vary Simultaneously   │ 227 devices (543 configs, 47.00%)           │
│ Only Storage Varies (RAM Constant)       │ 134 devices (296 configs, 27.74%)           │
│ Only RAM Varies (Storage Constant)       │ 121 devices (251 configs, 25.05%)           │
│ Neither Varies (Zero Variation)          │ 1 device (2 configs, 0.21%, Xiaomi Mi Max)  │
└──────────────────────────────────────────┴─────────────────────────────────────────────┘
```

### Complete 9-Device Exclusion Reconciliation Audit
A forensic cross-check across `docs/PHASE_04_STAGE_03_METHODOLOGY.md`, `scripts/analysis/exploratory_analysis.py`, and `Data/analytical/model4_within_diagnostics.json` reconciles all previously reported exclusion counts:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   CANDIDATE HARDWARE & MEMORY EXCLUSION TAXONOMY                                     │
├────┬─────────────────────────────┬──────┬─────────────────────────────┬────────────────────────────────┬─────────────┤
│ #  │ Device Model Slug           │ Confs│ Exclusion Category          │ Specific Observed Variation    │ Required by │
├────┼─────────────────────────────┼──────┼─────────────────────────────┼────────────────────────────────┼─────────────┤
│ 1  │ asus-zenfone-2-laser-ze550kl│ 2    │ Changing SoC Model          │ Snapdragon 410 vs. 615         │ Stage 03    │
│ 2  │ asus-zenfone-3-deluxe       │ 2    │ Changing SoC Model          │ Snapdragon 820 vs. 821         │ Stage 03    │
│ 3  │ samsung-galaxy-on-nxt       │ 3    │ Processor String Inconsist. │ Exynos 7 Octa vs. Octa Tru-    │ Stage 03    │
│ 4  │ vivo-y91                    │ 2    │ Changing SoC & Vendor       │ Snapdragon 439 vs. Helio P22   │ Stage 03    │
│ 5  │ panasonic-eluga-i2          │ 3    │ Changing Front Camera       │ 2.0 MP vs. 5.0 MP              │ Stage 03    │
│ 6  │ vivo-y91i                   │ 3    │ Changing Front Camera       │ 5.0 MP vs. 8.0 MP              │ Stage 03    │
├────┼─────────────────────────────┼──────┼─────────────────────────────┼────────────────────────────────┼─────────────┤
│ 7  │ xiaomi-redmi-k20-pro        │ 2    │ Charging Wattage Unstated   │ One NaN, one 27W (same phone)  │ Stage 03    │
│ 8  │ oneplus-7-pro               │ 3    │ Charging Wattage Unstated   │ One NaN, two 30W (same phone)  │ Stage 03    │
├────┼─────────────────────────────┼──────┼─────────────────────────────┼────────────────────────────────┼─────────────┤
│ 9  │ xiaomi-mi-max               │ 2    │ Degenerate Memory Tier      │ Zero variation (3GB/32GB both) │ Econometrics│
└────┴─────────────────────────────┴──────┴─────────────────────────────┴────────────────────────────────┴─────────────┘
```

### Explanation of Discrepancies Across Previous Revisions:
1. **The 4 Processor Devices (#1–#4):** Genuinely feature differing chipsets across configurations (or text string truncation artifacts in the scraper). Dropping these is required by Stage 03 methodology.
2. **The 2 Camera Devices (#5–#6):** Genuinely feature differing front camera sensors across configurations. Dropping these is required by Stage 03 methodology.
3. **The 2 Charging Wattage Devices (#7–#8):** In reality, physical charging hardware does not differ; rather, one listing per device has unstated/missing charging wattage (`NaN`), while the other has verified wattage (27W or 30W). In Stage 03 methodology, these were counted as "2 devices with different charging wattages" ($4 + 2 + 2 = 8$ devices). In `exploratory_analysis.py` under `.dropna().unique()`, their non-null wattage is consistent, so they were not flagged as conflicting hardware.
4. **The 1 Degenerate Memory Device (#9):** `xiaomi-mi-max` has identical RAM (3GB) and identical Storage (32GB) across both listings. It contributes zero variance to within-device de-meaning ($\Delta\text{RAM}=0, \Delta\text{Storage}=0$). While not flagged in Stage 03, dropping it is mathematically appropriate for within-device memory estimation.

### Subsample Options & Sensitivity Alignment (Artifact: `model4_within_diagnostics.json`):
```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                        MODEL 4 SUBSAMPLE DEFINITION & SENSITIVITY OPTIONS                              │
├──────┬────────────────────────────┬──────────────┬──────────────┬──────────┬───────────┬───────────────┤
│ Opt  │ Specification Definition   │ Excl Devices │ Invariant G  │ Invariant│ Within-r  │ Standardized  │
│      │                            │ (Configs)    │ (Clusters)   │ N (Confs)│ (r_RAM,St)│ Cond Number   │
├──────┼────────────────────────────┼──────────────┼──────────────┼──────────┼───────────┼───────────────┤
│ Tier1│ Full Multi-Variant Sample  │ 0 (0)        │ 483 devices  │ 1,092 cfg│ +0.3332   │ 2.00          │
│ Opt 1│ Stage 03 Baseline (8 devs) │ 8 devs (20)  │ 475 devices  │ 1,072 cfg│ +0.3321   │ 1.99          │
│ Opt 2│ Conflicting Hardware Only  │ 6 devs (15)  │ 477 devices  │ 1,077 cfg│ +0.3339   │ 2.00          │
│ Opt 3│ Revision 02 Specification  │ 7 devs (17)  │ 476 devices  │ 1,075 cfg│ +0.3339   │ 2.00          │
│ Opt 4│ Comprehensive Clean Sample │ 9 devs (22)  │ 474 devices  │ 1,070 cfg│ +0.3321   │ 1.99          │
└──────┴────────────────────────────┴──────────────┴──────────────┴──────────┴───────────┴───────────────┘
```
- Across all options, the within-device design matrix exhibits **full column rank (rank = 2)**, an exceptionally low **Within-VIF of 1.124 to 1.125**, and a standardized condition number of **1.99 to 2.00**.
- **Formal Recommendation:** Surface Options 1, 2, 3, and 4 for explicit project-owner decision before Stage 04.4 within-device modeling.

### Condition Number Interpretation & Regressor Scaling:
- **The Unscaled Condition Number (4,824.42) is Entirely Scale-Driven:**
  - RAM is measured in single-digit gigabytes (within-device variance $\sigma^2_{\text{RAM}} \approx 2.1$).
  - Storage is measured in tens or hundreds of gigabytes (within-device variance $\sigma^2_{\text{Storage}} \approx 10,780$).
  - The ~5,000-fold disparity in unit scale generates widely divergent eigenvalues ($\lambda_1 = 1,488.6$, $\lambda_2 = 7,181,615.2$), inflating the unscaled condition number ($\sqrt{\lambda_2 / \lambda_1} \approx 69.5$, or matrix ratio $\approx 4,824$).
- **Rescaled and Standardized Diagnostics:**
  - Measuring storage in 100 GB units reduces the condition number to **3.02**.
  - Standardizing both de-meaned regressors to unit variance yields a condition number of **2.00**.
  - The Within-VIF is **1.1249** ($R^2_{\text{within}} = 0.111$).
  - These diagnostics prove that the within-device design matrix is numerically stable and well-conditioned.

### Within-Device Association vs. Causal Identification Caveat:
- **Mathematical Invertibility is NOT Causal Proof:**
  - Having full column rank (rank = 2) and a low VIF confirms that $(X_{\text{within}}'X_{\text{within}})^{-1}$ exists and that OLS within-device coefficients can be stably computed.
  - However, full rank alone does **NOT** prove causal identification of OEM memory markup schedules.
  - Within-device estimates reflect observational retail pricing across variant tiers. While base chassis hardware (SoC, screen, chassis materials, cameras) is held fixed by device cluster de-meaning, variant pricing may reflect unobserved factors such as time-varying retail markdowns, channel promotions, or bundled accessories.
  - The Model 4 estimates will be reported strictly as **within-device hedonic upgrade price associations**, preserving journalistic and academic rigor.

---

## 10. Model 5 Modern-Feature Subsample Composition Skew

Restricting the estimation sample to records with complete charging wattage and refresh rate data drops the sample from $N = 2,256$ to $N = 1,101$, introducing severe structural selection skew:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        MODEL 5 SELECTION SKEW AUDIT TABLE                              │
├──────────────────────────────┬────────────────────┬────────────────────┬───────────────┤
│ Dimension                    │ Full Catalog       │ Model 5 Subsample  │ Subsample Skew│
├──────────────────────────────┼────────────────────┼────────────────────┼───────────────┤
│ Valid Record Count           │ 2,256 records      │ 1,101 records      │ -51.20% sample│
│ Median Listed Price          │ ₹14,499.00         │ ₹18,996.00         │ +31.03% higher│
│ Mean Listed Price            │ ₹22,210.68         │ ₹28,582.52         │ +28.69% higher│
│ Mean RAM Capacity            │ 5.20 GB            │ 7.38 GB            │ +41.92% higher│
│ Mean Storage Capacity        │ 113.39 GB          │ 176.88 GB          │ +55.99% higher│
│ Mean Battery Capacity        │ 4,141 mAh          │ 4,845 mAh          │ +17.00% higher│
├──────────────────────────────┼────────────────────┼────────────────────┼───────────────┤
│ Entry-Level Share (<₹10k)    │ 32.18% of catalog  │ 14.80% of sample   │ -17.38% drop  │
│ Budget-to-Mid Share (₹10-20k)│ 35.73% of catalog  │ 39.69% of sample   │ +3.96% share  │
│ Mid-Range Share (₹20-35k)    │ 17.46% of catalog  │ 24.61% of sample   │ +7.15% share  │
│ Upper-Mid Share (₹35-60k)    │ 8.73% of catalog   │ 11.81% of sample   │ +3.08% share  │
│ Premium Share (≥₹60k)        │ 5.90% of catalog   │ 9.08% of sample    │ +3.18% share  │
└──────────────────────────────┴────────────────────┴────────────────────┴───────────────┘
```

- **Selection Governance:** Model 5 is strictly a modern-device subsample. Its estimated parameters cannot be generalized to the entire 2011–2024 retail landscape. This selection skew will be prominently disclosed in all Model 5 visualizations and text copy.

---

## 11. Model 6 Quantile Regression Readiness & Sparsity Audit

- **Complete Sample Size:** Exactly **$N = 2,195$ records across $G = 1,586$ unique device clusters**.
- **Quantile Cutoffs Evaluated:**
  - $\tau = 0.10$ (10th percentile): Listed price threshold = **₹6,999.00** ($N = 250$ devices).
  - $\tau = 0.90$ (90th percentile): Listed price threshold = **₹44,999.00** ($N = 227$ devices).
- **Categorical Cell Sparsity Finding (Artifact: `exploratory_summary.json`):**
  - In the bottom 10% ($\le ₹6,999$), exactly **43 of 63 brands have zero representation**.
  - In the top 10% ($\ge ₹44,999$), exactly **49 of 63 brands have zero representation**.
- **Reframing Clustered Bootstrap Singularity as a Diagnostic Risk:**
  - In a clustered block-bootstrap with 1,586 clusters, resampling clusters with replacement creates a substantial diagnostic risk that certain bootstrap replications will draw samples lacking any observations for several sparse brand categories.
  - Such draws can produce singular or ill-conditioned design matrices for quantile regressions at extreme percentiles ($\tau = 0.10$ or $\tau = 0.90$).
  - **Inference Strategy Formally Unresolved:**
    - Non-clustered standard errors are **NOT** automatically prescribed as the default solution.
    - Instead, this is cataloged as a known diagnostic risk.
    - The definitive standard error formulation for Model 6 (e.g., asymptotic Huber-sandwich standard errors, wild bootstrap, clustered bootstrap with cell pruning, or non-clustered robust SEs) remains **formally unresolved pending dedicated empirical evaluation in Stage 04.5/04.6**.

---

## 12. Summary of Limitations & Unresolved Decisions

1. **Model 6 Inference Strategy:** Remains **formally unresolved** pending empirical evaluation of bootstrap convergence and sparsity behavior in Stage 04.5/04.6.
2. **Public Presentation Strategy for Models 3 & 4:** Remains **NOT YET APPROVED**. Public web UI choices and visual integration will be decided after Stage 04 econometric modeling is fully complete and evaluated.
3. **Apple Silicon Effect Separability:** Confirmed as structurally inseparable from Apple brand equity in observational market data. The parameter on `brand_Apple` represents a composite brand-and-silicon premium.
4. **Unobserved Historical Launch Dates:** Confirmed zero temporal timestamp variables exist in the dataset. Specification inflation across the 2011–2024 period cannot be controlled via time fixed effects.

---

## 13. Explicit Approval Checklist for the Project Owner

The following four operational authorizations are submitted for project-owner review to finalize Stage 04.2 and authorize progression to Stage 04.3:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        STAGE 04.2 OPERATIONAL APPROVAL CHECKLIST                       │
├────┬──────────────────────────────────┬───────────────────────────┬────────────────────┤
│ ID │ Decision / Action Item           │ Proposed Recommendation   │ Review Status      │
├────┼──────────────────────────────────┼───────────────────────────┼────────────────────┤
│ D1 │ Accept Revised Stage 04.2        │ Confirm price, spec, VIF, │ PENDING APPROVAL   │
│    │ Exploratory Report & Artifacts   │ Model 4, and M6 audits    │                    │
├────┼──────────────────────────────────┼───────────────────────────┼────────────────────┤
│ D2 │ Approve Model 3 Apple            │ Omit soc_Apple from dummy │ PENDING APPROVAL   │
│    │ Collinearity Resolution          │ block; fold into brand_   │                    │
│    │                                  │ Apple to ensure full rank │                    │
├────┼──────────────────────────────────┼───────────────────────────┼────────────────────┤
│ D3 │ Select Model 4 Hardware-         │ Approve Option 1 (8 devs),│ PENDING APPROVAL   │
│    │ Invariant Sensitivity Subsample  │ Option 3 (7 devs), or     │                    │
│    │ Definition                       │ Option 4 (9 devs)         │                    │
├────┼──────────────────────────────────┼───────────────────────────┼────────────────────┤
│ D4 │ Authorize Transition to          │ Proceed with fitting      │ PENDING APPROVAL   │
│    │ Stage 04.3                       │ Models 1, 2, and 3 with   │                    │
│    │                                  │ cluster-robust SEs        │                    │
└────┴──────────────────────────────────┴───────────────────────────┴────────────────────┘
```

1. **Authorization D1 — Revised Exploratory Report Acceptance:** Confirm acceptance of this revised exploratory analysis, VIF pre-screening, Model 4 within-device reconciliation, and artifact manifest.
2. **Authorization D2 — Apple Collinearity Resolution:** Approve the econometric resolution of omitting `soc_Apple` in Model 3 to prevent structural rank deficiency caused by Apple's 100% vertical integration, interpreting `brand_Apple` as the composite brand-and-silicon effect.
3. **Authorization D3 — Model 4 Sensitivity Sample Definition:** Select the approved hardware-invariance exclusion definition:
   - *Option 1 (Stage 03 Baseline):* 8 devices excluded (4 SoC + 2 cam + 2 wattage unstated) $\to 475$ devices (1,072 configs).
   - *Option 3 (Revision 02 Empirical):* 7 devices excluded (6 hardware conflicts + 1 degenerate memory) $\to 476$ devices (1,075 configs).
   - *Option 4 (Comprehensive Clean):* 9 devices excluded (6 hardware conflicts + 2 wattage unstated + 1 degenerate memory) $\to 474$ devices (1,070 configs).
4. **Authorization D4 — Transition to Stage 04.3:** Authorize commencing Stage 04.3 (Core Econometric Modeling: estimating Models 1, 2, and 3 with cluster-robust standard errors clustered on `device_id`).

---

*Phase 04 Stage 04.2 Exploratory Analysis revision is complete. Artifacts serialized in `Data/analytical/`.*  
*Halted at the approval gate in strict compliance with stop conditions. Standing by for project-owner review.*
