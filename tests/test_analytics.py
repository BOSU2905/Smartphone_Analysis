"""Unit and Integration Tests for Market Summary and Data Quality Analytics

Project: 'What Are We Really Paying For When We Buy a Smartphone?'
Phase 04 — Stage 02: Implementation
"""

from pathlib import Path
import sys
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.pipeline.analytics import (
    generate_data_quality_report,
    generate_market_summary,
)
from scripts.pipeline.config import (
    EXPECTED_DEDUPLICATED_ROW_COUNT,
    EXPECTED_EXACT_DUPLICATE_ROW_COUNT,
    EXPECTED_RAW_ROW_COUNT,
)
from scripts.pipeline.ingestion import load_raw_dataset
from scripts.pipeline.transformations import transform_dataset


class TestAnalyticsAndMarketSummary(unittest.TestCase):
    """Verifies market summary calculations, catalog counts, and price statistics."""

    @classmethod
    def setUpClass(cls):
        ingestion = load_raw_dataset()
        cls.records, cls.audit = transform_dataset(ingestion.raw_dataframe)
        cls.summary = generate_market_summary(cls.records)
        cls.quality = generate_data_quality_report(cls.records, cls.audit)

    def test_catalog_summary_counts(self):
        """Asserts catalog volumes across devices, configurations, and brands."""
        cat = self.summary["catalog_summary"]
        self.assertEqual(cat["total_unique_records"], EXPECTED_DEDUPLICATED_ROW_COUNT)
        self.assertEqual(cat["unique_base_devices"], 1647)
        self.assertEqual(cat["unique_configurations"], 2255)
        self.assertEqual(cat["unique_brands"], 63)

    def test_overall_price_statistics(self):
        """Asserts overall INR price statistics are within verified bounds."""
        p = self.summary["price_distribution"]["overall_inr"]
        self.assertEqual(p["valid_n"], 2256)
        self.assertEqual(p["min"], 5000.0)
        self.assertEqual(p["max"], 200999.0)
        self.assertEqual(p["median"], 14499.0)
        self.assertAlmostEqual(p["mean"], 22210.6751, places=3)

    def test_quintile_summary_structure(self):
        """Asserts all five quintiles are represented with correct counts."""
        q_dict = self.summary["price_distribution"]["quintiles"]
        self.assertEqual(len(q_dict), 5)
        self.assertEqual(q_dict["Q1"]["record_count"], 454)
        self.assertEqual(q_dict["Q2"]["record_count"], 482)
        self.assertEqual(q_dict["Q3"]["record_count"], 436)
        self.assertEqual(q_dict["Q4"]["record_count"], 433)
        self.assertEqual(q_dict["Q5"]["record_count"], 451)

    def test_editorial_tiers_summary_structure(self):
        """Asserts all five editorial tiers are represented with correct counts."""
        t_dict = self.summary["price_distribution"]["editorial_tiers"]
        self.assertEqual(len(t_dict), 5)
        self.assertEqual(t_dict["Entry-level"]["record_count"], 726)
        self.assertEqual(t_dict["Budget-to-mid"]["record_count"], 806)
        self.assertEqual(t_dict["Mid-range"]["record_count"], 394)
        self.assertEqual(t_dict["Upper-mid"]["record_count"], 197)
        self.assertEqual(t_dict["Premium"]["record_count"], 133)

    def test_semiconductor_distribution(self):
        """Asserts MediaTek and Qualcomm dominate catalog and Kirin is separate."""
        socs = self.summary["semiconductor_distribution"]
        soc_map = {item["manufacturer"]: item["model_count"] for item in socs}

        self.assertGreater(soc_map.get("MediaTek", 0), 900)
        self.assertGreater(soc_map.get("Qualcomm", 0), 800)
        self.assertIn("HiSilicon", soc_map)
        self.assertNotIn("Kirin", soc_map)  # Kirin is family/model, HiSilicon is mfr

    def test_display_family_distribution(self):
        """Asserts LCD and OLED distributions."""
        disp = self.summary["display_technology_distribution"]
        disp_map = {item["display_family"]: item["model_count"] for item in disp}
        self.assertEqual(disp_map.get("LCD", 0), 1395)
        self.assertEqual(disp_map.get("OLED", 0), 859)

    def test_ratings_correlation(self):
        """Asserts correlation calculation between expert and user ratings."""
        ratings = self.summary["ratings_analysis"]
        self.assertEqual(ratings["coexisting_ratings_count"], 1384)
        self.assertIsNotNone(ratings["pearson_correlation"])
        self.assertIsNotNone(ratings["spearman_correlation"])
        # Both should reflect weak positive correlation around ~0.25
        self.assertAlmostEqual(ratings["pearson_correlation"], 0.2486, places=2)


class TestDataQualityReport(unittest.TestCase):
    """Verifies missingness audit, quality flags distribution, and invariant assertions."""

    @classmethod
    def setUpClass(cls):
        ingestion = load_raw_dataset()
        cls.records, cls.audit = transform_dataset(ingestion.raw_dataframe)
        cls.quality = generate_data_quality_report(cls.records, cls.audit)

    def test_invariant_verifications(self):
        """Asserts all ground-truth pipeline invariants hold True."""
        invariants = self.quality["invariant_verifications"]
        self.assertTrue(invariants["is_1tb_storage_intact"])
        self.assertEqual(invariants["corrupted_1tb_storage_count"], 0)
        self.assertTrue(invariants["is_kirin_classification_intact"])
        self.assertEqual(invariants["misclassified_kirin_count"], 0)
        self.assertEqual(invariants["zero_denominator_ram_count"], 0)
        self.assertEqual(invariants["zero_denominator_storage_count"], 0)
        self.assertEqual(invariants["zero_denominator_battery_count"], 0)
        self.assertTrue(invariants["exact_deduplication_integrity"])

    def test_missingness_table(self):
        """Asserts missingness metrics for critical fields."""
        table = self.quality["missingness_audit"]
        m_map = {item["attribute"]: item["missing_count"] for item in table}

        self.assertEqual(m_map["ram_capacity_gb"], 8)
        self.assertEqual(m_map["storage_capacity_gb"], 2)
        self.assertEqual(m_map["battery_capacity_mah"], 0)
        self.assertEqual(m_map["charging_wattage"], 2256 - 1321)  # 935
        self.assertEqual(m_map["screen_size_inches"], 1)
        self.assertEqual(m_map["expert_rating"], 858)
        self.assertEqual(m_map["user_rating_score"], 71)


if __name__ == "__main__":
    unittest.main()
