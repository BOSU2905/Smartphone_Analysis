"""Artifact Serialization & Export Module

Project: 'What Are We Really Paying For When We Buy a Smartphone?'
Phase 04 — Stage 02: Implementation
"""

import csv
from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd

from .config import (
    OUTPUT_CLEANED_CSV,
    OUTPUT_CLEANED_JSON,
    OUTPUT_DATA_QUALITY_REPORT_JSON,
    OUTPUT_DEDUPLICATION_AUDIT_JSON,
    OUTPUT_MARKET_SUMMARY_JSON,
    PROCESSED_DATA_DIR,
)
from .transformations import TransformedRecord


@dataclass(frozen=True)
class FileExportReport:
    """Metadata report for an exported artifact file."""

    file_name: str
    file_path: str
    byte_size: int
    record_count: Optional[int]
    is_valid_format: bool


@dataclass(frozen=True)
class PipelineExportSummary:
    """Consolidated summary of all pipeline export artifacts."""

    cleaned_csv: FileExportReport
    cleaned_json: FileExportReport
    market_summary_json: FileExportReport
    deduplication_audit_json: FileExportReport
    data_quality_report_json: FileExportReport

    @property
    def all_files_valid(self) -> bool:
        return (
            self.cleaned_csv.is_valid_format
            and self.cleaned_json.is_valid_format
            and self.market_summary_json.is_valid_format
            and self.deduplication_audit_json.is_valid_format
            and self.data_quality_report_json.is_valid_format
        )


def export_cleaned_csv(
    records: List[TransformedRecord],
    output_path: Path = OUTPUT_CLEANED_CSV,
) -> FileExportReport:
    """Exports transformed records to a canonical, clean CSV file.

    Lists and dict attributes are flattened to pipe-delimited strings to prevent
    corrupt CSV quoting and maintain clean column alignment.

    Args:
        records: List of TransformedRecord entities.
        output_path: Target Path for CSV output.

    Returns:
        FileExportReport detailing the exported CSV file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    flat_records = [r.to_flat_dict() for r in records]
    df = pd.DataFrame(flat_records)

    # Write CSV with deterministic ordering
    df.to_csv(output_path, index=False, encoding="utf-8")

    byte_size = os.path.getsize(output_path)

    # Verify CSV can be read back cleanly
    df_read = pd.read_csv(output_path)
    is_valid = (len(df_read) == len(records))

    return FileExportReport(
        file_name=output_path.name,
        file_path=str(output_path),
        byte_size=byte_size,
        record_count=len(df),
        is_valid_format=is_valid,
    )


def export_cleaned_json(
    records: List[TransformedRecord],
    output_path: Path = OUTPUT_CLEANED_JSON,
) -> FileExportReport:
    """Exports transformed records to a structured JSON catalog array.

    Args:
        records: List of TransformedRecord entities.
        output_path: Target Path for JSON output.

    Returns:
        FileExportReport detailing the exported JSON file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    json_records = [r.to_dict() for r in records]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(json_records, f, indent=2, ensure_ascii=False)

    byte_size = os.path.getsize(output_path)

    # Verify JSON can be parsed back
    with open(output_path, "r", encoding="utf-8") as f:
        parsed_back = json.load(f)
    is_valid = (isinstance(parsed_back, list) and len(parsed_back) == len(records))

    return FileExportReport(
        file_name=output_path.name,
        file_path=str(output_path),
        byte_size=byte_size,
        record_count=len(json_records),
        is_valid_format=is_valid,
    )


def export_json_report(
    data: Dict[str, Any],
    output_path: Path,
) -> FileExportReport:
    """Exports report or audit dictionary to a formatted JSON file.

    Args:
        data: Report dictionary.
        output_path: Target Path for JSON output.

    Returns:
        FileExportReport detailing the exported JSON file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    byte_size = os.path.getsize(output_path)

    # Verify JSON parseability
    with open(output_path, "r", encoding="utf-8") as f:
        parsed_back = json.load(f)
    is_valid = isinstance(parsed_back, dict)

    return FileExportReport(
        file_name=output_path.name,
        file_path=str(output_path),
        byte_size=byte_size,
        record_count=None,
        is_valid_format=is_valid,
    )


def run_full_pipeline_export(
    records: List[TransformedRecord],
    market_summary: Dict[str, Any],
    deduplication_audit: Dict[str, Any],
    data_quality_report: Dict[str, Any],
    output_dir: Path = PROCESSED_DATA_DIR,
) -> PipelineExportSummary:
    """Executes atomic export of all five required pipeline artifacts.

    Outputs:
    1. smartphones_cleaned.csv
    2. smartphones_cleaned.json
    3. market_summary.json
    4. deduplication_audit.json
    5. data_quality_report.json

    Args:
        records: TransformedRecord entities (2,256 unique models).
        market_summary: Market statistics dictionary.
        deduplication_audit: Exact deduplication audit dictionary.
        data_quality_report: Missingness and quality flags dictionary.
        output_dir: Directory where files will be created.

    Returns:
        PipelineExportSummary with verification status of all files.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_report = export_cleaned_csv(records, output_dir / "smartphones_cleaned.csv")
    json_report = export_cleaned_json(records, output_dir / "smartphones_cleaned.json")
    market_report = export_json_report(market_summary, output_dir / "market_summary.json")
    dedup_report = export_json_report(deduplication_audit, output_dir / "deduplication_audit.json")
    quality_report = export_json_report(data_quality_report, output_dir / "data_quality_report.json")

    return PipelineExportSummary(
        cleaned_csv=csv_report,
        cleaned_json=json_report,
        market_summary_json=market_report,
        deduplication_audit_json=dedup_report,
        data_quality_report_json=quality_report,
    )
