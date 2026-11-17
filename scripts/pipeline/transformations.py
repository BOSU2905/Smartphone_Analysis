"""Dataset Transformation, Exact Deduplication & Segmentation Module

Project: 'What Are We Really Paying For When We Buy a Smartphone?'
Phase 04 — Stage 02: Implementation
"""

from dataclasses import asdict, dataclass, field
import json
import re
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd

from .brand_taxonomy import BrandResult, parse_brand
from .config import (
    CURRENCY_BASE,
    CURRENCY_CONVERSION_STATUS,
    DEFERRED_CURRENCY_LABEL,
    EXPECTED_DEDUPLICATED_ROW_COUNT,
    EXPECTED_EXACT_DUPLICATE_ROW_COUNT,
    EXPECTED_RAW_COLUMNS,
    EXPECTED_RAW_ROW_COUNT,
    QUINTILE_Q1_MAX,
    QUINTILE_Q2_MAX,
    QUINTILE_Q3_MAX,
    QUINTILE_Q4_MAX,
    TIER_BUDGET_TO_MID,
    TIER_ENTRY_LEVEL,
    TIER_MID_RANGE,
    TIER_PREMIUM,
    TIER_UPPER_MID,
)
from .parsers import (
    ParsedSpecifications,
    generate_config_id,
    generate_device_id,
    parse_all_specifications,
)
from .ratings import RatingsMetadata, parse_all_ratings_and_reviews


@dataclass(frozen=True)
class DeduplicationRecord:
    """Represents a unique record with complete source duplicate group lineage."""

    representative_listing_id: str
    duplicate_listing_ids: List[str]
    duplicate_count: int
    source_row: Dict[str, Any]


@dataclass(frozen=True)
class TransformedRecord:
    """Fully parsed, validated, and segmented smartphone entity."""

    # Listing & Identity
    listing_id: str
    duplicate_listing_ids: List[str]
    duplicate_count: int
    device_id: str
    config_id: str
    model_name: str

    # Brand & Corporate Provenance
    brand_name: str
    brand_tier: str
    parent_company: Optional[str]
    parent_company_status: str
    relationship_type: str

    # Pricing & Segmentations
    original_listed_price_inr: int
    price_quintile: str
    editorial_price_tier: str

    # Hardware Specifications
    ram_capacity_gb: Optional[float]
    storage_capacity_gb: Optional[float]
    battery_capacity_mah: Optional[int]
    charging_wattage: Optional[int]
    screen_size_inches: Optional[float]
    refresh_rate_hz: Optional[int]
    display_panel_family: Optional[str]
    display_technology_raw: Optional[str]
    rear_main_sensor_mp: Optional[float]
    rear_lens_count: Optional[int]
    rear_sensor_breakdown_mp: List[float]
    front_main_sensor_mp: Optional[float]
    front_lens_count: Optional[int]
    processor_manufacturer: Optional[str]
    processor_family: Optional[str]
    processor_model: Optional[str]
    processor_core_count: Optional[int]
    operating_system_raw: Optional[str]
    operating_system_family: Optional[str]

    # Ratings & Reviews
    expert_rating: Optional[float]
    user_rating_score: Optional[float]
    user_rating_count: Optional[int]
    review_snippet: Optional[str]
    review_url: Optional[str]

    # Descriptive Unit-Rate Metrics
    price_per_gb_ram_inr: Optional[float]
    price_per_gb_storage_inr: Optional[float]
    price_per_1000mah_battery_inr: Optional[float]
    price_per_charging_watt_inr: Optional[float]
    price_per_display_inch_inr: Optional[float]

    # Lineage & Metadata
    quality_flags: List[str]
    currency_conversion_metadata: Dict[str, str]

    def to_dict(self) -> Dict[str, Any]:
        """Serializes entity to dictionary suitable for JSON serialization."""
        return asdict(self)

    def to_flat_dict(self) -> Dict[str, Any]:
        """Flattens nested attributes (lists/dicts) into pipe-delimited format for CSV."""
        d = self.to_dict()
        d["duplicate_listing_ids"] = "|".join(self.duplicate_listing_ids)
        d["rear_sensor_breakdown_mp"] = (
            "|".join(str(mp) for mp in self.rear_sensor_breakdown_mp)
            if self.rear_sensor_breakdown_mp
            else ""
        )
        d["quality_flags"] = "|".join(self.quality_flags)
        d["currency_conversion_metadata"] = (
            f"BASE:{self.currency_conversion_metadata.get('base')};"
            f"STATUS:{self.currency_conversion_metadata.get('status')};"
            f"LABEL:{self.currency_conversion_metadata.get('target_label')}"
        )
        return d


def clean_price_inr(raw_price: Any) -> int:
    """Parses Indian Rupee price string removing commas and whitespace.

    Args:
        raw_price: String or numeric price from source dataset.

    Returns:
        Integer price in INR.

    Raises:
        ValueError: If price cannot be parsed as positive integer.
    """
    if raw_price is None:
        raise ValueError("Missing price value.")

    cleaned_str = str(raw_price).replace(",", "").strip()
    val = int(cleaned_str)
    if val <= 0:
        raise ValueError(f"Invalid non-positive price: {val}")
    return val


def assign_price_quintile(price_inr: int) -> str:
    """Assigns statistical price quintile based on right-closed interval semantics.

    Boundaries (derived from empirical unique dataset):
    - Q1: <= ₹8,299
    - Q2: (₹8,299, ₹11,999]
    - Q3: (₹11,999, ₹16,999]
    - Q4: (₹16,999, ₹29,495]
    - Q5: > ₹29,495

    Tied prices on boundaries remain deterministic without artificial group splitting.

    Args:
        price_inr: Integer price in INR.

    Returns:
        Quintile identifier ('Q1', 'Q2', 'Q3', 'Q4', or 'Q5').
    """
    if price_inr <= QUINTILE_Q1_MAX:
        return "Q1"
    elif price_inr <= QUINTILE_Q2_MAX:
        return "Q2"
    elif price_inr <= QUINTILE_Q3_MAX:
        return "Q3"
    elif price_inr <= QUINTILE_Q4_MAX:
        return "Q4"
    else:
        return "Q5"


def assign_editorial_tier(price_inr: int) -> str:
    """Assigns descriptive editorial price tier based on agreed retail brackets.

    Brackets (INR):
    - Entry-level: < ₹10,000
    - Budget-to-mid: ₹10,000 – ₹19,999
    - Mid-range: ₹20,000 – ₹34,999
    - Upper-mid: ₹35,000 – ₹59,999
    - Premium: >= ₹60,000

    Args:
        price_inr: Integer price in INR.

    Returns:
        Tier label string.
    """
    if price_inr < 10000:
        return TIER_ENTRY_LEVEL
    elif price_inr < 20000:
        return TIER_BUDGET_TO_MID
    elif price_inr < 35000:
        return TIER_MID_RANGE
    elif price_inr < 60000:
        return TIER_UPPER_MID
    else:
        return TIER_PREMIUM


def calculate_unit_rates(
    price_inr: int,
    ram_gb: Optional[float],
    storage_gb: Optional[float],
    battery_mah: Optional[int],
    charging_watts: Optional[int],
    display_inches: Optional[float],
) -> Dict[str, Optional[float]]:
    """Calculates descriptive unit-rate ratios with strict denominator validation.

    Ratios:
    - price_per_gb_ram_inr = Price / RAM (GB)
    - price_per_gb_storage_inr = Price / Storage (GB)
    - price_per_1000mah_battery_inr = Price / (Battery mAh / 1000.0)
    - price_per_charging_watt_inr = Price / Charging Wattage (W)
    - price_per_display_inch_inr = Price / Display Diagonal (Inches)

    All ratios return None when the denominator is null or non-positive.
    These are purely descriptive unit rates, never composite specification scores.

    Args:
        price_inr: Integer retail price in INR.
        ram_gb: RAM capacity in GB.
        storage_gb: Internal storage capacity in GB.
        battery_mah: Battery capacity in mAh.
        charging_watts: Fast-charging wattage.
        display_inches: Screen diagonal size in inches.

    Returns:
        Dictionary of rounded unit-rate metrics (or None if uncomputable).
    """
    rate_ram = (
        round(price_inr / ram_gb, 4) if ram_gb is not None and ram_gb > 0 else None
    )
    rate_storage = (
        round(price_inr / storage_gb, 4)
        if storage_gb is not None and storage_gb > 0
        else None
    )
    rate_battery = (
        round(price_inr / (battery_mah / 1000.0), 4)
        if battery_mah is not None and battery_mah > 0
        else None
    )
    rate_charging = (
        round(price_inr / charging_watts, 4)
        if charging_watts is not None and charging_watts > 0
        else None
    )
    rate_display = (
        round(price_inr / display_inches, 4)
        if display_inches is not None and display_inches > 0
        else None
    )

    return {
        "price_per_gb_ram_inr": rate_ram,
        "price_per_gb_storage_inr": rate_storage,
        "price_per_1000mah_battery_inr": rate_battery,
        "price_per_charging_watt_inr": rate_charging,
        "price_per_display_inch_inr": rate_display,
    }


def parse_operating_system_family(raw_os: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """Extracts high-level OS family and preserves raw OS string.

    Args:
        raw_os: Raw operating system string (e.g. 'Android v14', 'iOS v17').

    Returns:
        Tuple of (os_family, os_raw).
    """
    if not raw_os or pd.isna(raw_os):
        return None, None
    s = str(raw_os).strip()
    s_lower = s.lower()
    if "android" in s_lower:
        return "Android", s
    elif "ios" in s_lower or "iphone" in s_lower:
        return "iOS", s
    elif "windows" in s_lower:
        return "Windows Phone", s
    elif "blackberry" in s_lower:
        return "BlackBerry", s
    elif "tizen" in s_lower:
        return "Tizen", s
    elif "sailfish" in s_lower:
        return "Sailfish", s
    else:
        return "Other", s


def exact_deduplicate(
    df: pd.DataFrame,
) -> Tuple[List[DeduplicationRecord], Dict[str, Any]]:
    """Performs exact deduplication across all 14 original source columns.

    Groups records that are identical in every source column (using dropna=False
    so null fields are treated as equal). Preserves full listing lineage by
    recording all member listing_ids in each duplicate group. Deterministically
    selects the first occurrence (lowest listing_id) as the representative record.

    Args:
        df: Ingested raw DataFrame with 'listing_id' and 14 source columns.

    Returns:
        Tuple of (deduplicated_records_list, deduplication_audit_dict).
    """
    source_cols = [c for c in df.columns if c != "listing_id"]

    # Verify all expected columns are present
    for col in EXPECTED_RAW_COLUMNS:
        if col not in source_cols:
            raise ValueError(f"Missing mandatory column for deduplication: {col}")

    # Group by all source columns with dropna=False
    grouped = df.groupby(source_cols, as_index=False, sort=False, dropna=False)

    deduped_records: List[DeduplicationRecord] = []
    audit_groups: List[Dict[str, Any]] = []

    total_exact_duplicate_rows = 0

    for _, group_df in grouped:
        listing_ids = group_df["listing_id"].tolist()
        group_size = len(listing_ids)
        rep_id = listing_ids[0]

        # Extract representative row dictionary
        rep_row = group_df.iloc[0].to_dict()

        if group_size > 1:
            total_exact_duplicate_rows += group_size - 1
            audit_groups.append(
                {
                    "representative_listing_id": rep_id,
                    "duplicate_listing_ids": listing_ids,
                    "group_size": group_size,
                    "model_name": str(rep_row.get("model_name", "")),
                    "price": str(rep_row.get("price", "")),
                }
            )

        deduped_records.append(
            DeduplicationRecord(
                representative_listing_id=rep_id,
                duplicate_listing_ids=listing_ids,
                duplicate_count=group_size,
                source_row=rep_row,
            )
        )

    # Sort deterministically by integer suffix of representative_listing_id
    deduped_records.sort(
        key=lambda r: int(re.sub(r"[^\d]", "", r.representative_listing_id))
    )

    audit_summary = {
        "raw_row_count": len(df),
        "exact_duplicate_rows_removed": total_exact_duplicate_rows,
        "unique_retained_records": len(deduped_records),
        "duplicate_groups_count": len(audit_groups),
        "expected_raw_rows": EXPECTED_RAW_ROW_COUNT,
        "expected_duplicate_rows": EXPECTED_EXACT_DUPLICATE_ROW_COUNT,
        "expected_unique_records": EXPECTED_DEDUPLICATED_ROW_COUNT,
        "is_deduplication_exact_match": (
            len(deduped_records) == EXPECTED_DEDUPLICATED_ROW_COUNT
            and total_exact_duplicate_rows == EXPECTED_EXACT_DUPLICATE_ROW_COUNT
        ),
        "duplicate_groups": audit_groups,
    }

    return deduped_records, audit_summary


def transform_dataset(
    df: pd.DataFrame,
) -> Tuple[List[TransformedRecord], Dict[str, Any]]:
    """Transforms raw ingested DataFrame into validated, segmented TransformedRecord entities.

    Steps:
    1. Exact deduplication with full duplicate group lineage.
    2. Specification parsing (RAM, Storage, Battery, Display, Camera, Processor).
    3. Brand resolution and corporate provenance assignment.
    4. Ratings and editorial review extraction.
    5. Price cleaning, statistical quintile, and editorial tier assignment.
    6. Descriptive unit-rate calculations.
    7. Quality flag aggregation.

    Args:
        df: Ingested raw DataFrame.

    Returns:
        Tuple of (transformed_records_list, deduplication_audit_dict).
    """
    deduped_records, audit_summary = exact_deduplicate(df)

    transformed: List[TransformedRecord] = []

    # Prepare deferred currency conversion metadata
    currency_meta = {
        "base": CURRENCY_BASE,
        "status": CURRENCY_CONVERSION_STATUS,
        "target_label": DEFERRED_CURRENCY_LABEL,
        "note": "Converted currency fields are deferred in Phase 04 Stage 02.",
    }

    for d_rec in deduped_records:
        row = d_rec.source_row
        rep_id = d_rec.representative_listing_id

        # 1. Price
        price_inr = clean_price_inr(row.get("price"))
        quintile = assign_price_quintile(price_inr)
        tier = assign_editorial_tier(price_inr)

        # 2. Specifications
        specs: ParsedSpecifications = parse_all_specifications(row, listing_id=rep_id)

        # 3. Brand & Corporate Provenance
        model_name = str(row.get("model_name", ""))
        brand: BrandResult = parse_brand(model_name)

        # 4. Ratings & Reviews
        ratings: RatingsMetadata = parse_all_ratings_and_reviews(row)

        # 5. Operating System Family
        os_family, os_raw = parse_operating_system_family(row.get("operating_system"))

        # 6. Descriptive Unit-Rate Metrics
        unit_rates = calculate_unit_rates(
            price_inr=price_inr,
            ram_gb=specs.ram.ram_capacity_gb,
            storage_gb=specs.storage.storage_capacity_gb,
            battery_mah=specs.battery.battery_capacity_mah,
            charging_watts=specs.battery.charging_wattage,
            display_inches=specs.display.screen_size_inches,
        )

        # 7. Aggregate Quality Flags
        all_flags = sorted(
            list(
                set(
                    specs.all_quality_flags
                    + brand.quality_flags
                    + ratings.all_quality_flags
                )
            )
        )

        rec = TransformedRecord(
            listing_id=rep_id,
            duplicate_listing_ids=d_rec.duplicate_listing_ids,
            duplicate_count=d_rec.duplicate_count,
            device_id=specs.device_id,
            config_id=specs.config_id,
            model_name=model_name,
            brand_name=brand.brand_name,
            brand_tier=brand.catalog_tier,
            parent_company=brand.parent_company,
            parent_company_status=brand.parent_company_status,
            relationship_type=brand.relationship_type,
            original_listed_price_inr=price_inr,
            price_quintile=quintile,
            editorial_price_tier=tier,
            ram_capacity_gb=specs.ram.ram_capacity_gb,
            storage_capacity_gb=specs.storage.storage_capacity_gb,
            battery_capacity_mah=specs.battery.battery_capacity_mah,
            charging_wattage=specs.battery.charging_wattage,
            screen_size_inches=specs.display.screen_size_inches,
            refresh_rate_hz=specs.display.refresh_rate_hz,
            display_panel_family=specs.display.display_panel_family,
            display_technology_raw=specs.display.display_technology_raw,
            rear_main_sensor_mp=specs.rear_cameras.rear_main_sensor_mp,
            rear_lens_count=specs.rear_cameras.rear_lens_count,
            rear_sensor_breakdown_mp=specs.rear_cameras.sensor_breakdown_mp,
            front_main_sensor_mp=specs.front_cameras.front_main_sensor_mp,
            front_lens_count=specs.front_cameras.front_lens_count,
            processor_manufacturer=specs.processor.manufacturer,
            processor_family=specs.processor.family,
            processor_model=specs.processor.model,
            processor_core_count=specs.processor.core_count,
            operating_system_raw=os_raw,
            operating_system_family=os_family,
            expert_rating=ratings.expert_rating,
            user_rating_score=ratings.user_rating.score,
            user_rating_count=ratings.user_rating.count,
            review_snippet=ratings.review.snippet,
            review_url=ratings.review.url,
            price_per_gb_ram_inr=unit_rates["price_per_gb_ram_inr"],
            price_per_gb_storage_inr=unit_rates["price_per_gb_storage_inr"],
            price_per_1000mah_battery_inr=unit_rates["price_per_1000mah_battery_inr"],
            price_per_charging_watt_inr=unit_rates["price_per_charging_watt_inr"],
            price_per_display_inch_inr=unit_rates["price_per_display_inch_inr"],
            quality_flags=all_flags,
            currency_conversion_metadata=currency_meta,
        )

        transformed.append(rec)

    return transformed, audit_summary
