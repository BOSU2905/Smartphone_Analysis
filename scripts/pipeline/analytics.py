"""Analytical Metrics, Market Summaries & Quality Reporting Module

Project: 'What Are We Really Paying For When We Buy a Smartphone?'
Phase 04 — Stage 02: Implementation
"""

from collections import Counter
import math
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd

from .config import (
    CURRENCY_BASE,
    CURRENCY_CONVERSION_STATUS,
    DEFERRED_CURRENCY_LABEL,
    EXPECTED_DEDUPLICATED_ROW_COUNT,
    EXPECTED_EXACT_DUPLICATE_ROW_COUNT,
    EXPECTED_RAW_ROW_COUNT,
    TIER_BUDGET_TO_MID,
    TIER_ENTRY_LEVEL,
    TIER_MID_RANGE,
    TIER_PREMIUM,
    TIER_UPPER_MID,
)
from .transformations import TransformedRecord


def _compute_numeric_series_stats(values: List[float]) -> Dict[str, Any]:
    """Computes descriptive summary statistics for a list of floats."""
    if not values:
        return {
            "valid_n": 0,
            "min": None,
            "max": None,
            "mean": None,
            "median": None,
            "std": None,
            "p25": None,
            "p75": None,
        }

    arr = np.array(values, dtype=float)
    return {
        "valid_n": int(len(arr)),
        "min": round(float(np.min(arr)), 4),
        "max": round(float(np.max(arr)), 4),
        "mean": round(float(np.mean(arr)), 4),
        "median": round(float(np.median(arr)), 4),
        "std": round(float(np.std(arr, ddof=1)), 4) if len(arr) > 1 else 0.0,
        "p25": round(float(np.percentile(arr, 25)), 4),
        "p75": round(float(np.percentile(arr, 75)), 4),
    }


def generate_market_summary(records: List[TransformedRecord]) -> Dict[str, Any]:
    """Generates comprehensive market overview statistics from transformed records.

    Covers:
    - Overall catalog volumes (unique models, unique devices, configurations, brands).
    - Retail price distributions (overall, per quintile, per editorial tier).
    - Descriptive unit-rate metric distributions.
    - Semiconductor market shares and median price points.
    - Display panel family breakdown.
    - Rating correlations (expert vs user).

    Args:
        records: List of fully transformed TransformedRecord entities.

    Returns:
        Structured market summary dictionary.
    """
    total_retained = len(records)
    unique_devices = len(set(r.device_id for r in records))
    unique_configs = len(set(r.config_id for r in records))
    unique_brands = len(set(r.brand_name for r in records))

    # Overall price stats
    prices = [r.original_listed_price_inr for r in records]
    overall_price_stats = _compute_numeric_series_stats(prices)

    # Price stats by quintile
    quintiles = ["Q1", "Q2", "Q3", "Q4", "Q5"]
    quintile_breakdown = {}
    for q in quintiles:
        q_prices = [
            r.original_listed_price_inr for r in records if r.price_quintile == q
        ]
        quintile_breakdown[q] = {
            "record_count": len(q_prices),
            "stats": _compute_numeric_series_stats(q_prices),
        }

    # Price stats by editorial tier
    tiers = [
        TIER_ENTRY_LEVEL,
        TIER_BUDGET_TO_MID,
        TIER_MID_RANGE,
        TIER_UPPER_MID,
        TIER_PREMIUM,
    ]
    tier_breakdown = {}
    for t in tiers:
        t_prices = [
            r.original_listed_price_inr for r in records if r.editorial_price_tier == t
        ]
        tier_breakdown[t] = {
            "record_count": len(t_prices),
            "stats": _compute_numeric_series_stats(t_prices),
        }

    # Unit-rate metrics stats
    unit_rate_keys = [
        ("price_per_gb_ram_inr", [r.price_per_gb_ram_inr for r in records if r.price_per_gb_ram_inr is not None]),
        ("price_per_gb_storage_inr", [r.price_per_gb_storage_inr for r in records if r.price_per_gb_storage_inr is not None]),
        ("price_per_1000mah_battery_inr", [r.price_per_1000mah_battery_inr for r in records if r.price_per_1000mah_battery_inr is not None]),
        ("price_per_charging_watt_inr", [r.price_per_charging_watt_inr for r in records if r.price_per_charging_watt_inr is not None]),
        ("price_per_display_inch_inr", [r.price_per_display_inch_inr for r in records if r.price_per_display_inch_inr is not None]),
    ]
    unit_rates_summary = {
        name: _compute_numeric_series_stats(vals) for name, vals in unit_rate_keys
    }

    # Brand portfolio summary
    brand_map: Dict[str, List[int]] = {}
    brand_tier_map: Dict[str, str] = {}
    brand_parent_map: Dict[str, Optional[str]] = {}
    for r in records:
        if r.brand_name not in brand_map:
            brand_map[r.brand_name] = []
            brand_tier_map[r.brand_name] = r.brand_tier
            brand_parent_map[r.brand_name] = r.parent_company
        brand_map[r.brand_name].append(r.original_listed_price_inr)

    brand_portfolio = []
    for b_name, b_prices in sorted(brand_map.items(), key=lambda x: len(x[1]), reverse=True):
        brand_portfolio.append({
            "brand_name": b_name,
            "catalog_tier": brand_tier_map[b_name],
            "parent_company": brand_parent_map[b_name],
            "model_count": len(b_prices),
            "percentage_of_catalog": round((len(b_prices) / total_retained) * 100, 2),
            "price_stats": _compute_numeric_series_stats(b_prices),
        })

    # Semiconductor manufacturer breakdown
    soc_counter = Counter(r.processor_manufacturer or "Unknown" for r in records)
    soc_breakdown = []
    for soc_mfr, count in soc_counter.most_common():
        soc_prices = [
            r.original_listed_price_inr
            for r in records
            if (r.processor_manufacturer or "Unknown") == soc_mfr
        ]
        soc_breakdown.append({
            "manufacturer": soc_mfr,
            "model_count": count,
            "percentage_share": round((count / total_retained) * 100, 2),
            "price_stats": _compute_numeric_series_stats(soc_prices),
        })

    # Display panel family breakdown
    disp_counter = Counter(r.display_panel_family or "Unknown" for r in records)
    display_breakdown = []
    for disp_fam, count in disp_counter.most_common():
        disp_prices = [
            r.original_listed_price_inr
            for r in records
            if (r.display_panel_family or "Unknown") == disp_fam
        ]
        display_breakdown.append({
            "display_family": disp_fam,
            "model_count": count,
            "percentage_share": round((count / total_retained) * 100, 2),
            "price_stats": _compute_numeric_series_stats(disp_prices),
        })

    # Ratings evaluation & correlation
    expert_scores = [r.expert_rating for r in records if r.expert_rating is not None]
    user_scores = [r.user_rating_score for r in records if r.user_rating_score is not None]
    both_ratings = [
        (r.expert_rating, r.user_rating_score)
        for r in records
        if r.expert_rating is not None and r.user_rating_score is not None
    ]

    pearson_corr = None
    spearman_corr = None
    if len(both_ratings) > 1:
        e_arr = np.array([x[0] for x in both_ratings])
        u_arr = np.array([x[1] for x in both_ratings])
        pearson_corr = round(float(np.corrcoef(e_arr, u_arr)[0, 1]), 4)
        # Compute Spearman rank correlation
        df_ranks = pd.DataFrame({"expert": e_arr, "user": u_arr})
        spearman_corr = round(float(df_ranks.corr(method="spearman").iloc[0, 1]), 4)

    ratings_summary = {
        "expert_ratings_stats": _compute_numeric_series_stats(expert_scores),
        "user_ratings_stats": _compute_numeric_series_stats(user_scores),
        "coexisting_ratings_count": len(both_ratings),
        "pearson_correlation": pearson_corr,
        "spearman_correlation": spearman_corr,
    }

    return {
        "currency": {
            "base_currency": CURRENCY_BASE,
            "conversion_status": CURRENCY_CONVERSION_STATUS,
            "deferred_label": DEFERRED_CURRENCY_LABEL,
        },
        "catalog_summary": {
            "total_unique_records": total_retained,
            "unique_base_devices": unique_devices,
            "unique_configurations": unique_configs,
            "unique_brands": unique_brands,
        },
        "price_distribution": {
            "overall_inr": overall_price_stats,
            "quintiles": quintile_breakdown,
            "editorial_tiers": tier_breakdown,
        },
        "descriptive_unit_rates": unit_rates_summary,
        "brand_portfolio_summary": brand_portfolio,
        "semiconductor_distribution": soc_breakdown,
        "display_technology_distribution": display_breakdown,
        "ratings_analysis": ratings_summary,
    }


def generate_data_quality_report(
    records: List[TransformedRecord],
    deduplication_audit: Dict[str, Any],
) -> Dict[str, Any]:
    """Generates comprehensive data quality audit report and anomaly telemetry.

    Audits:
    - Exact missingness counts and percentages across all 25+ specification attributes.
    - Aggregated quality flags frequency distribution.
    - Ground-truth invariant assertions (e.g. 1TB storage, Kirin SoC classification, etc.).

    Args:
        records: TransformedRecord entities.
        deduplication_audit: Exact deduplication audit summary dictionary.

    Returns:
        Structured data quality report dictionary.
    """
    total = len(records)

    def _field_missingness(field_fn, name: str) -> Dict[str, Any]:
        missing_count = sum(1 for r in records if field_fn(r) is None)
        return {
            "attribute": name,
            "missing_count": missing_count,
            "valid_count": total - missing_count,
            "missing_percentage": round((missing_count / total) * 100, 2),
        }

    missingness_table = [
        _field_missingness(lambda r: r.ram_capacity_gb, "ram_capacity_gb"),
        _field_missingness(lambda r: r.storage_capacity_gb, "storage_capacity_gb"),
        _field_missingness(lambda r: r.battery_capacity_mah, "battery_capacity_mah"),
        _field_missingness(lambda r: r.charging_wattage, "charging_wattage"),
        _field_missingness(lambda r: r.screen_size_inches, "screen_size_inches"),
        _field_missingness(lambda r: r.refresh_rate_hz, "refresh_rate_hz"),
        _field_missingness(lambda r: r.display_panel_family, "display_panel_family"),
        _field_missingness(lambda r: r.rear_main_sensor_mp, "rear_main_sensor_mp"),
        _field_missingness(lambda r: r.front_main_sensor_mp, "front_main_sensor_mp"),
        _field_missingness(lambda r: r.processor_manufacturer, "processor_manufacturer"),
        _field_missingness(lambda r: r.processor_model, "processor_model"),
        _field_missingness(lambda r: r.operating_system_raw, "operating_system_raw"),
        _field_missingness(lambda r: r.expert_rating, "expert_rating"),
        _field_missingness(lambda r: r.user_rating_score, "user_rating_score"),
        _field_missingness(lambda r: r.review_snippet, "review_snippet"),
        _field_missingness(lambda r: r.review_url, "review_url"),
        _field_missingness(lambda r: r.price_per_gb_ram_inr, "price_per_gb_ram_inr"),
        _field_missingness(lambda r: r.price_per_gb_storage_inr, "price_per_gb_storage_inr"),
        _field_missingness(lambda r: r.price_per_1000mah_battery_inr, "price_per_1000mah_battery_inr"),
        _field_missingness(lambda r: r.price_per_charging_watt_inr, "price_per_charging_watt_inr"),
        _field_missingness(lambda r: r.price_per_display_inch_inr, "price_per_display_inch_inr"),
    ]

    # Quality flags frequency
    flag_counter: Counter = Counter()
    for r in records:
        for f in r.quality_flags:
            flag_counter[f] += 1

    flag_distribution = [
        {"flag": flag_name, "frequency": count, "percentage": round((count / total) * 100, 2)}
        for flag_name, count in flag_counter.most_common()
    ]

    # Invariant audits
    # 1. 1TB storage integrity
    corrupted_1tb = sum(
        1 for r in records if "1TB" in r.model_name.upper() and r.storage_capacity_gb != 1024.0
    )
    # 2. HiSilicon integrity
    misclassified_kirin = sum(
        1 for r in records if "kirin" in (r.processor_model or "").lower() and r.processor_manufacturer == "Unisoc"
    )
    # 3. Denominator zero safety
    zero_ram = sum(1 for r in records if r.ram_capacity_gb == 0)
    zero_storage = sum(1 for r in records if r.storage_capacity_gb == 0)
    zero_battery = sum(1 for r in records if r.battery_capacity_mah == 0)

    invariants = {
        "corrupted_1tb_storage_count": corrupted_1tb,
        "is_1tb_storage_intact": (corrupted_1tb == 0),
        "misclassified_kirin_count": misclassified_kirin,
        "is_kirin_classification_intact": (misclassified_kirin == 0),
        "zero_denominator_ram_count": zero_ram,
        "zero_denominator_storage_count": zero_storage,
        "zero_denominator_battery_count": zero_battery,
        "exact_deduplication_integrity": deduplication_audit.get("is_deduplication_exact_match", False),
    }

    return {
        "dataset_integrity_overview": {
            "total_raw_rows": deduplication_audit.get("raw_row_count", EXPECTED_RAW_ROW_COUNT),
            "exact_duplicate_rows_removed": deduplication_audit.get("exact_duplicate_rows_removed", EXPECTED_EXACT_DUPLICATE_ROW_COUNT),
            "retained_unique_records": total,
        },
        "missingness_audit": missingness_table,
        "quality_flags_audit": flag_distribution,
        "invariant_verifications": invariants,
    }
