"""Unit and Integration Tests for Artifact Export and Serialization

Project: 'What Are We Really Paying For When We Buy a Smartphone?'
Phase 04 — Stage 02: Implementation
"""

import json
from pathlib import Path
import sys
import tempfile
import unittest
import pandas as pd

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
    OUTPUT_CLEANED_CSV,
    OUTPUT_CLEANED_JSON,
    OUTPUT_DATA_QUALITY_REPORT_JSON,
    OUTPUT_DEDUPLICATION_AUDIT_JSON,
    OUTPUT_MARKET_SUMMARY_JSON,
)
from scripts.pipeline.export import (
    export_cleaned_csv,
    export_cleaned_json,
    export_json_report,
    run_full_pipeline_export,
)
from scripts.pipeline.ingestion import load_raw_dataset
from scripts.pipeline.transformations import transform_dataset


class TestPipelineExport(unittest.TestCase):
    """Verifies artifact serialization, file integrity, and schema compliance."""

    @classmethod
    def setUpClass(cls):
        ingestion = load_raw_dataset()
        cls.records, cls.audit = transform_dataset(ingestion.raw_dataframe)
        cls.market_summary = generate_market_summary(cls.records)
        cls.quality_report = generate_data_quality_report(cls.records, cls.audit)

    def test_export_to_temporary_directory(self):
        """Asserts all five files are exported cleanly to a temporary directory."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            summary = run_full_pipeline_export(
                records=self.records,
                market_summary=self.market_summary,
                deduplication_audit=self.audit,
                data_quality_report=self.quality_report,
                output_dir=tmp_path,
            )

            self.assertTrue(summary.all_files_valid)
            self.assertTrue((tmp_path / "smartphones_cleaned.csv").exists())
            self.assertTrue((tmp_path / "smartphones_cleaned.json").exists())
            self.assertTrue((tmp_path / "market_summary.json").exists())
            self.assertTrue((tmp_path / "deduplication_audit.json").exists())
            self.assertTrue((tmp_path / "data_quality_report.json").exists())

            # Verify CSV row count
            df_csv = pd.read_csv(tmp_path / "smartphones_cleaned.csv")
            self.assertEqual(len(df_csv), EXPECTED_DEDUPLICATED_ROW_COUNT)
            self.assertIn("original_listed_price_inr", df_csv.columns)
            self.assertIn("price_quintile", df_csv.columns)
            self.assertIn("editorial_price_tier", df_csv.columns)
            self.assertIn("device_id", df_csv.columns)
            self.assertIn("config_id", df_csv.columns)

            # Verify JSON catalog parsing
            with open(tmp_path / "smartphones_cleaned.json", "r", encoding="utf-8") as f:
                json_data = json.load(f)
            self.assertEqual(len(json_data), EXPECTED_DEDUPLICATED_ROW_COUNT)
            self.assertEqual(json_data[0]["listing_id"], "rec_0001")
            self.assertIsInstance(json_data[0]["duplicate_listing_ids"], list)

            # Verify deduplication audit JSON
            with open(tmp_path / "deduplication_audit.json", "r", encoding="utf-8") as f:
                dedup_json = json.load(f)
            self.assertEqual(dedup_json["raw_row_count"], EXPECTED_RAW_ROW_COUNT)
            self.assertEqual(
                dedup_json["exact_duplicate_rows_removed"],
                EXPECTED_EXACT_DUPLICATE_ROW_COUNT,
            )
            self.assertEqual(
                dedup_json["unique_retained_records"],
                EXPECTED_DEDUPLICATED_ROW_COUNT,
            )

            # Verify data quality report JSON
            with open(tmp_path / "data_quality_report.json", "r", encoding="utf-8") as f:
                qual_json = json.load(f)
            self.assertTrue(qual_json["invariant_verifications"]["is_1tb_storage_intact"])
            self.assertTrue(qual_json["invariant_verifications"]["is_kirin_classification_intact"])

    def test_canonical_processed_files_exist_and_match(self):
        """Asserts canonical output files in Data/processed/ exist and have valid structure."""
        self.assertTrue(OUTPUT_CLEANED_CSV.exists())
        self.assertTrue(OUTPUT_CLEANED_JSON.exists())
        self.assertTrue(OUTPUT_MARKET_SUMMARY_JSON.exists())
        self.assertTrue(OUTPUT_DEDUPLICATION_AUDIT_JSON.exists())
        self.assertTrue(OUTPUT_DATA_QUALITY_REPORT_JSON.exists())

        # Assert non-empty file sizes
        self.assertGreater(OUTPUT_CLEANED_CSV.stat().st_size, 1_000_000)
        self.assertGreater(OUTPUT_CLEANED_JSON.stat().st_size, 3_000_000)
        self.assertGreater(OUTPUT_MARKET_SUMMARY_JSON.stat().st_size, 20_000)
        self.assertGreater(OUTPUT_DEDUPLICATION_AUDIT_JSON.stat().st_size, 100_000)
        self.assertGreater(OUTPUT_DATA_QUALITY_REPORT_JSON.stat().st_size, 3_000)


if __name__ == "__main__":
    unittest.main()
