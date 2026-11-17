"""Main Command-Line Interface for the Smartphone Data Pipeline

Project: 'What Are We Really Paying For When We Buy a Smartphone?'
Phase 04 — Stage 02: Implementation

Usage:
    python -m scripts.pipeline
"""

import sys
import time

from .analytics import generate_data_quality_report, generate_market_summary
from .config import (
    EXPECTED_DEDUPLICATED_ROW_COUNT,
    EXPECTED_EXACT_DUPLICATE_ROW_COUNT,
    EXPECTED_RAW_ROW_COUNT,
)
from .export import run_full_pipeline_export
from .ingestion import load_raw_dataset
from .transformations import transform_dataset


def run_pipeline() -> int:
    """Executes the complete deterministic smartphone processing pipeline."""
    start_time = time.time()
    print("=" * 70)
    print("SMARTPHONE DATA PROCESSING PIPELINE — PHASE 04 STAGE 02")
    print("Project: 'What Are We Really Paying For When We Buy a Smartphone?'")
    print("=" * 70)

    # 1. Ingestion & Raw Integrity
    print("\n[STEP 1/5] Ingesting and validating raw dataset integrity...")
    try:
        ingestion_res = load_raw_dataset()
    except Exception as e:
        print(f"FATAL: Ingestion failed: {e}", file=sys.stderr)
        return 1

    cs = ingestion_res.checksum_report
    print(f"  • Source file: {cs.file_path}")
    print(f"  • Byte count:  {cs.byte_count:,} bytes (Valid: {cs.is_byte_count_valid})")
    print(f"  • SHA-256:     {cs.sha256} (Valid: {cs.is_sha256_valid})")
    print(f"  • MD5:         {cs.md5} (Valid: {cs.is_md5_valid})")
    print(f"  • Raw rows:    {ingestion_res.row_count} (Expected: {EXPECTED_RAW_ROW_COUNT})")
    print(f"  • Columns:     {ingestion_res.column_count} (14 raw + 1 listing_id)")

    if not cs.is_fully_valid or ingestion_res.row_count != EXPECTED_RAW_ROW_COUNT:
        print("FATAL: Raw dataset checksum or row count mismatch!", file=sys.stderr)
        return 1

    # 2. Deduplication & Transformation
    print("\n[STEP 2/5] Performing exact deduplication & specification parsing...")
    records, dedup_audit = transform_dataset(ingestion_res.raw_dataframe)

    print(f"  • Exact duplicates removed: {dedup_audit['exact_duplicate_rows_removed']} (Expected: {EXPECTED_EXACT_DUPLICATE_ROW_COUNT})")
    print(f"  • Unique records retained:  {len(records)} (Expected: {EXPECTED_DEDUPLICATED_ROW_COUNT})")
    print(f"  • Duplicate groups tracked: {dedup_audit['duplicate_groups_count']}")

    if (
        len(records) != EXPECTED_DEDUPLICATED_ROW_COUNT
        or dedup_audit["exact_duplicate_rows_removed"] != EXPECTED_EXACT_DUPLICATE_ROW_COUNT
    ):
        print("FATAL: Deduplication mismatch with verified ground truth!", file=sys.stderr)
        return 1

    # 3. Market Summary & Analytics
    print("\n[STEP 3/5] Generating market summary & price distribution statistics...")
    market_summary = generate_market_summary(records)

    p_stats = market_summary["price_distribution"]["overall_inr"]
    print(f"  • Price (INR): Min ₹{p_stats['min']:,} | Median ₹{p_stats['median']:,} | Mean ₹{p_stats['mean']:,} | Max ₹{p_stats['max']:,}")

    q_counts = {q: v["record_count"] for q, v in market_summary["price_distribution"]["quintiles"].items()}
    print(f"  • Quintiles:   {q_counts}")

    t_counts = {t: v["record_count"] for t, v in market_summary["price_distribution"]["editorial_tiers"].items()}
    print(f"  • Tiers:       {t_counts}")

    # Unit rate valid sample sizes
    ur_counts = {k: v["valid_n"] for k, v in market_summary["descriptive_unit_rates"].items()}
    print("  • Unit-rate denominators (valid N):")
    for k, v in ur_counts.items():
        print(f"      - {k}: {v}")

    # 4. Data Quality Report
    print("\n[STEP 4/5] Compiling data quality & invariant verification report...")
    quality_report = generate_data_quality_report(records, dedup_audit)

    invariants = quality_report["invariant_verifications"]
    print(f"  • 1TB Storage Integrity:      {invariants['is_1tb_storage_intact']} (Corrupt: {invariants['corrupted_1tb_storage_count']})")
    print(f"  • Kirin/Unisoc Classification:{invariants['is_kirin_classification_intact']} (Misclassified: {invariants['misclassified_kirin_count']})")
    print(f"  • Zero RAM Denominators:      {invariants['zero_denominator_ram_count']}")
    print(f"  • Zero Storage Denominators:  {invariants['zero_denominator_storage_count']}")
    print(f"  • Zero Battery Denominators:  {invariants['zero_denominator_battery_count']}")

    # 5. Serialization & Export
    print("\n[STEP 5/5] Exporting verified pipeline artifacts to Data/processed/...")
    export_summary = run_full_pipeline_export(
        records=records,
        market_summary=market_summary,
        deduplication_audit=dedup_audit,
        data_quality_report=quality_report,
    )

    print(f"  ✓ {export_summary.cleaned_csv.file_name:<30} ({export_summary.cleaned_csv.byte_size:>10,} bytes | {export_summary.cleaned_csv.record_count} records)")
    print(f"  ✓ {export_summary.cleaned_json.file_name:<30} ({export_summary.cleaned_json.byte_size:>10,} bytes | {export_summary.cleaned_json.record_count} records)")
    print(f"  ✓ {export_summary.market_summary_json.file_name:<30} ({export_summary.market_summary_json.byte_size:>10,} bytes)")
    print(f"  ✓ {export_summary.deduplication_audit_json.file_name:<30} ({export_summary.deduplication_audit_json.byte_size:>10,} bytes)")
    print(f"  ✓ {export_summary.data_quality_report_json.file_name:<30} ({export_summary.data_quality_report_json.byte_size:>10,} bytes)")

    elapsed = time.time() - start_time
    print("-" * 70)
    print(f"PIPELINE COMPLETED SUCCESSFULLY in {elapsed:.2f} seconds.")
    print(f"All 5 artifacts exported and verified: {export_summary.all_files_valid}")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(run_pipeline())
