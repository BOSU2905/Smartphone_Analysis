"""Unit and Integration Tests for Transformations, Deduplication, and Segmentation

Project: 'What Are We Really Paying For When We Buy a Smartphone?'
Phase 04 — Stage 02: Implementation
"""

from pathlib import Path
import sys
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.pipeline.config import (
    CURRENCY_BASE,
    CURRENCY_CONVERSION_STATUS,
    DEFERRED_CURRENCY_LABEL,
    EXPECTED_DEDUPLICATED_ROW_COUNT,
    EXPECTED_EXACT_DUPLICATE_ROW_COUNT,
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
from scripts.pipeline.ingestion import load_raw_dataset
from scripts.pipeline.parsers import generate_config_id, generate_device_id
from scripts.pipeline.transformations import (
    assign_editorial_tier,
    assign_price_quintile,
    calculate_unit_rates,
    clean_price_inr,
    exact_deduplicate,
    parse_operating_system_family,
    transform_dataset,
)


class TestExactDeduplication(unittest.TestCase):
    """Verifies deterministic exact deduplication across all 14 source columns."""

    @classmethod
    def setUpClass(cls):
        cls.ingestion_res = load_raw_dataset()

    def test_exact_deduplication_counts(self):
        """Asserts exactly 672 duplicate rows removed and 2,256 unique records retained."""
        records, audit = exact_deduplicate(self.ingestion_res.raw_dataframe)
        self.assertEqual(len(records), EXPECTED_DEDUPLICATED_ROW_COUNT)
        self.assertEqual(audit["raw_row_count"], EXPECTED_RAW_ROW_COUNT)
        self.assertEqual(
            audit["exact_duplicate_rows_removed"], EXPECTED_EXACT_DUPLICATE_ROW_COUNT
        )
        self.assertEqual(
            audit["unique_retained_records"], EXPECTED_DEDUPLICATED_ROW_COUNT
        )
        self.assertTrue(audit["is_deduplication_exact_match"])

    def test_duplicate_lineage_preservation(self):
        """Asserts each record preserves duplicate_listing_ids and representative identity."""
        records, audit = exact_deduplicate(self.ingestion_res.raw_dataframe)
        multi_listing_records = [r for r in records if r.duplicate_count > 1]
        self.assertGreater(len(multi_listing_records), 0)

        for r in multi_listing_records:
            self.assertEqual(r.duplicate_count, len(r.duplicate_listing_ids))
            self.assertEqual(r.representative_listing_id, r.duplicate_listing_ids[0])
            self.assertIn(r.representative_listing_id, r.duplicate_listing_ids)

    def test_deterministic_deduplication_sorting(self):
        """Asserts deduplication output is stably ordered by representative listing ID."""
        records1, _ = exact_deduplicate(self.ingestion_res.raw_dataframe)
        records2, _ = exact_deduplicate(self.ingestion_res.raw_dataframe)
        rep_ids1 = [r.representative_listing_id for r in records1]
        rep_ids2 = [r.representative_listing_id for r in records2]
        self.assertEqual(rep_ids1, rep_ids2)

    def test_deduplication_mathematical_reconciliation(self):
        """Asserts complete mathematical reconciliation of singletons, multi-listings, and raw rows."""
        records, audit = exact_deduplicate(self.ingestion_res.raw_dataframe)
        singletons = audit["singleton_records_count"]
        multi_groups = audit["multi_listing_duplicate_groups_count"]
        retained = audit["unique_retained_records"]
        removed = audit["exact_duplicate_rows_removed"]
        raw_total = audit["raw_row_count"]

        # Exactly 1,584 singletons and 672 multi-listing pairs
        self.assertEqual(singletons, 1584)
        self.assertEqual(multi_groups, 672)

        # 1,584 singletons + 672 multi-listing representative records = 2,256 retained
        self.assertEqual(singletons + multi_groups, retained)
        self.assertEqual(retained, 2256)

        # 1,584 * 1 + 672 * 2 = 2,928 total raw source listings
        self.assertEqual(singletons * 1 + multi_groups * 2, raw_total)
        self.assertEqual(raw_total, 2928)

        # Exactly 672 duplicate rows removed (2,928 - 2,256 = 672)
        self.assertEqual(raw_total - retained, removed)
        self.assertEqual(removed, 672)

    def test_lineage_exhaustive_coverage_zero_omissions(self):
        """Asserts every single raw listing_id (rec_0001..rec_2928) is accounted for exactly once."""
        raw_ids = set(self.ingestion_res.raw_dataframe["listing_id"])
        self.assertEqual(len(raw_ids), 2928)

        records, _ = exact_deduplicate(self.ingestion_res.raw_dataframe)
        accounted_ids = []
        for r in records:
            accounted_ids.extend(r.duplicate_listing_ids)

        self.assertEqual(len(accounted_ids), 2928)
        self.assertEqual(len(set(accounted_ids)), 2928)
        self.assertEqual(set(accounted_ids), raw_ids)


class TestIdentityResolution(unittest.TestCase):
    """Verifies deterministic ID generation, plus-sign preservation, and edge cases."""

    def test_plus_sign_identity_collision_prevention(self):
        """Asserts OPPO Reno10 Pro and OPPO Reno10 Pro+ produce distinct device and config IDs."""
        id_pro = generate_device_id("OPPO Reno10 Pro 5G")
        id_pro_plus = generate_device_id("OPPO Reno10 Pro+ 5G")
        self.assertEqual(id_pro, "oppo-reno10-pro-5g")
        self.assertEqual(id_pro_plus, "oppo-reno10-pro-plus-5g")
        self.assertNotEqual(id_pro, id_pro_plus)

        cfg_pro = generate_config_id(id_pro, 12.0, 256.0)
        cfg_pro_plus = generate_config_id(id_pro_plus, 12.0, 256.0)
        self.assertNotEqual(cfg_pro, cfg_pro_plus)

    def test_xiaomi_mi_max_edge_case(self):
        """Asserts two different source listings resolving to same device/config retain distinct listing_ids."""
        dev1 = generate_device_id("Xiaomi Mi Max")
        dev2 = generate_device_id("Xiaomi Mi Max 32GB")
        self.assertEqual(dev1, "xiaomi-mi-max")
        self.assertEqual(dev2, "xiaomi-mi-max")

        cfg1 = generate_config_id(dev1, 3.0, 32.0)
        cfg2 = generate_config_id(dev2, 3.0, 32.0)
        self.assertEqual(cfg1, cfg2)
        self.assertEqual(cfg1, "xiaomi-mi-max_3gb_32gb")


class TestPriceCleaningAndSegmentation(unittest.TestCase):
    """Verifies price parsing, right-closed statistical quintiles, and editorial tiers."""

    def test_clean_price_inr(self):
        """Asserts commas and spaces are stripped and positive integers returned."""
        self.assertEqual(clean_price_inr("34,999"), 34999)
        self.assertEqual(clean_price_inr(" 1,51,700 "), 151700)
        self.assertEqual(clean_price_inr(5000), 5000)

        with self.assertRaises(ValueError):
            clean_price_inr(None)
        with self.assertRaises(ValueError):
            clean_price_inr("0")
        with self.assertRaises(ValueError):
            clean_price_inr("-5000")

    def test_price_quintile_boundaries(self):
        """Asserts right-closed interval boundaries for Q1..Q5."""
        # Q1: <= 8299
        self.assertEqual(assign_price_quintile(5000), "Q1")
        self.assertEqual(assign_price_quintile(8299), "Q1")
        # Q2: (8299, 11999]
        self.assertEqual(assign_price_quintile(8300), "Q2")
        self.assertEqual(assign_price_quintile(11999), "Q2")
        # Q3: (11999, 16999]
        self.assertEqual(assign_price_quintile(12000), "Q3")
        self.assertEqual(assign_price_quintile(16999), "Q3")
        # Q4: (16999, 29495]
        self.assertEqual(assign_price_quintile(17000), "Q4")
        self.assertEqual(assign_price_quintile(29495), "Q4")
        # Q5: > 29495
        self.assertEqual(assign_price_quintile(29496), "Q5")
        self.assertEqual(assign_price_quintile(200999), "Q5")

    def test_editorial_tier_boundaries(self):
        """Asserts descriptive editorial price tier boundaries."""
        # Entry-level: < 10000
        self.assertEqual(assign_editorial_tier(5000), TIER_ENTRY_LEVEL)
        self.assertEqual(assign_editorial_tier(9999), TIER_ENTRY_LEVEL)
        # Budget-to-mid: 10000 – 19999
        self.assertEqual(assign_editorial_tier(10000), TIER_BUDGET_TO_MID)
        self.assertEqual(assign_editorial_tier(19999), TIER_BUDGET_TO_MID)
        # Mid-range: 20000 – 34999
        self.assertEqual(assign_editorial_tier(20000), TIER_MID_RANGE)
        self.assertEqual(assign_editorial_tier(34999), TIER_MID_RANGE)
        # Upper-mid: 35000 – 59999
        self.assertEqual(assign_editorial_tier(35000), TIER_UPPER_MID)
        self.assertEqual(assign_editorial_tier(59999), TIER_UPPER_MID)
        # Premium: >= 60000
        self.assertEqual(assign_editorial_tier(60000), TIER_PREMIUM)
        self.assertEqual(assign_editorial_tier(200999), TIER_PREMIUM)


class TestDescriptiveUnitRates(unittest.TestCase):
    """Verifies unit-rate calculations and strict denominator validations."""

    def test_unit_rate_calculations(self):
        """Asserts price per unit calculations when denominators are valid."""
        rates = calculate_unit_rates(
            price_inr=30000,
            ram_gb=8.0,
            storage_gb=128.0,
            battery_mah=5000,
            charging_watts=67,
            display_inches=6.67,
        )
        self.assertEqual(rates["price_per_gb_ram_inr"], round(30000 / 8.0, 4))
        self.assertEqual(rates["price_per_gb_storage_inr"], round(30000 / 128.0, 4))
        self.assertEqual(rates["price_per_1000mah_battery_inr"], round(30000 / 5.0, 4))
        self.assertEqual(rates["price_per_charging_watt_inr"], round(30000 / 67.0, 4))
        self.assertEqual(rates["price_per_display_inch_inr"], round(30000 / 6.67, 4))

    def test_unit_rates_null_or_zero_denominator_returns_none(self):
        """Asserts None is strictly returned when any denominator is null or non-positive."""
        rates_none = calculate_unit_rates(
            price_inr=30000,
            ram_gb=None,
            storage_gb=None,
            battery_mah=None,
            charging_watts=None,
            display_inches=None,
        )
        for k, v in rates_none.items():
            self.assertIsNone(v, f"{k} must be None when denominator is None")

        rates_zero = calculate_unit_rates(
            price_inr=30000,
            ram_gb=0,
            storage_gb=0,
            battery_mah=0,
            charging_watts=0,
            display_inches=0,
        )
        for k, v in rates_zero.items():
            self.assertIsNone(v, f"{k} must be None when denominator is zero")


class TestFullDatasetTransformation(unittest.TestCase):
    """Verifies end-to-end dataset transformation against Stage 01B expected figures."""

    @classmethod
    def setUpClass(cls):
        ingestion = load_raw_dataset()
        cls.records, cls.audit = transform_dataset(ingestion.raw_dataframe)

    def test_total_records_count(self):
        """Asserts transformed dataset has exactly 2,256 unique records."""
        self.assertEqual(len(self.records), EXPECTED_DEDUPLICATED_ROW_COUNT)

    def test_quintile_distribution_counts(self):
        """Asserts exact quintile distribution matches approved Stage 01B counts."""
        q_counts = {}
        for r in self.records:
            q_counts[r.price_quintile] = q_counts.get(r.price_quintile, 0) + 1

        self.assertEqual(q_counts["Q1"], 454)
        self.assertEqual(q_counts["Q2"], 482)
        self.assertEqual(q_counts["Q3"], 436)
        self.assertEqual(q_counts["Q4"], 433)
        self.assertEqual(q_counts["Q5"], 451)
        self.assertEqual(sum(q_counts.values()), 2256)

    def test_editorial_tier_distribution_counts(self):
        """Asserts exact editorial price tier distribution matches approved Stage 01B counts."""
        t_counts = {}
        for r in self.records:
            t_counts[r.editorial_price_tier] = t_counts.get(r.editorial_price_tier, 0) + 1

        self.assertEqual(t_counts[TIER_ENTRY_LEVEL], 726)
        self.assertEqual(t_counts[TIER_BUDGET_TO_MID], 806)
        self.assertEqual(t_counts[TIER_MID_RANGE], 394)
        self.assertEqual(t_counts[TIER_UPPER_MID], 197)
        self.assertEqual(t_counts[TIER_PREMIUM], 133)
        self.assertEqual(sum(t_counts.values()), 2256)

    def test_unit_rate_valid_denominators(self):
        """Asserts valid N for each unit-rate metric strictly matches Stage 01B targets."""
        n_ram = sum(1 for r in self.records if r.price_per_gb_ram_inr is not None)
        n_storage = sum(1 for r in self.records if r.price_per_gb_storage_inr is not None)
        n_battery = sum(1 for r in self.records if r.price_per_1000mah_battery_inr is not None)
        n_charging = sum(1 for r in self.records if r.price_per_charging_watt_inr is not None)
        n_display = sum(1 for r in self.records if r.price_per_display_inch_inr is not None)

        self.assertEqual(n_ram, 2248)
        self.assertEqual(n_storage, 2254)
        self.assertEqual(n_battery, 2256)
        self.assertEqual(n_charging, 1321)
        self.assertEqual(n_display, 2255)

    def test_deferred_currency_conversion_metadata(self):
        """Asserts base price remains INR and currency conversion is flagged as DEFERRED."""
        for r in self.records:
            self.assertEqual(r.currency_conversion_metadata["base"], CURRENCY_BASE)
            self.assertEqual(
                r.currency_conversion_metadata["status"], CURRENCY_CONVERSION_STATUS
            )
            self.assertEqual(
                r.currency_conversion_metadata["target_label"], DEFERRED_CURRENCY_LABEL
            )
            # Assert no converted price fields exist on record
            self.assertFalse(hasattr(r, "price_usd"))
            self.assertFalse(hasattr(r, "price_idr"))


if __name__ == "__main__":
    unittest.main()
