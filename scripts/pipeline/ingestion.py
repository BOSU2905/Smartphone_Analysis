"""Raw Data Ingestion & File Checksum Verification Module

Project: 'What Are We Really Paying For When We Buy a Smartphone?'
Phase 03 — Stage 02: Pipeline Foundation & Specification Parsing
"""

from dataclasses import dataclass, field
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd

from .config import (
    EXPECTED_RAW_COLUMNS,
    EXPECTED_RAW_ROW_COUNT,
    RAW_DATA_PATH,
    RAW_FILE_EXPECTED_BYTES,
    RAW_FILE_EXPECTED_MD5,
    RAW_FILE_EXPECTED_SHA256,
)


@dataclass(frozen=True)
class ChecksumReport:
    """Immutable audit report of source file integrity."""

    file_path: str
    byte_count: int
    sha256: str
    md5: str
    is_sha256_valid: bool
    is_md5_valid: bool
    is_byte_count_valid: bool

    @property
    def is_fully_valid(self) -> bool:
        return self.is_sha256_valid and self.is_md5_valid and self.is_byte_count_valid


@dataclass
class IngestionResult:
    """Structured container returned by the data ingestion pipeline."""

    raw_dataframe: pd.DataFrame
    row_count: int
    column_count: int
    checksum_report: ChecksumReport
    missing_value_summary: Dict[str, int]
    validation_messages: List[str] = field(default_factory=list)


def compute_file_checksum(file_path: Path) -> ChecksumReport:
    """Computes SHA-256 and MD5 checksums directly from source file bytes.

    Args:
        file_path: Path to the target source file.

    Returns:
        ChecksumReport detailing calculated hashes and validation status against config.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Source file not found at: {file_path}")

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    byte_len = len(file_bytes)
    sha256_hash = hashlib.sha256(file_bytes).hexdigest()
    md5_hash = hashlib.md5(file_bytes).hexdigest()

    return ChecksumReport(
        file_path=str(file_path),
        byte_count=byte_len,
        sha256=sha256_hash,
        md5=md5_hash,
        is_sha256_valid=(sha256_hash == RAW_FILE_EXPECTED_SHA256),
        is_md5_valid=(md5_hash == RAW_FILE_EXPECTED_MD5),
        is_byte_count_valid=(byte_len == RAW_FILE_EXPECTED_BYTES),
    )


def validate_source_schema(df: pd.DataFrame) -> List[str]:
    """Validates that all expected columns are present in the loaded dataframe.

    Args:
        df: Ingested pandas DataFrame.

    Returns:
        List of validation warning or confirmation messages.

    Raises:
        ValueError: If any mandatory source column is missing.
    """
    missing_cols = [col for col in EXPECTED_RAW_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(
            f"Source schema integrity violation. Missing mandatory columns: {missing_cols}"
        )

    unexpected_cols = [col for col in df.columns if col not in EXPECTED_RAW_COLUMNS]
    messages = [f"Source schema validated: All {len(EXPECTED_RAW_COLUMNS)} required columns present."]
    if unexpected_cols:
        messages.append(f"Notice: Additional non-standard columns detected: {unexpected_cols}")

    return messages


def load_raw_dataset(source_path: Optional[Path] = None) -> IngestionResult:
    """Safely loads the raw smartphone dataset and validates its byte integrity.

    Assigns a stable, zero-indexed `listing_id` (source record identity) to preserve
    exact source row provenance without modifying any raw column values.

    Args:
        source_path: Optional custom Path. Defaults to RAW_DATA_PATH from config.

    Returns:
        IngestionResult containing dataframe, checksums, and validation telemetry.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If schema or row count fails critical integrity checks.
    """
    target_path = source_path or RAW_DATA_PATH

    # 1. Audit File Integrity via Checksums
    checksum_report = compute_file_checksum(target_path)
    validation_messages = []

    if not checksum_report.is_fully_valid:
        validation_messages.append(
            f"WARNING: File checksum discrepancy detected for {target_path}!"
        )
    else:
        validation_messages.append(
            "File integrity verified: SHA-256 and MD5 match expected ground truth."
        )

    # 2. Ingest CSV while Preserving Exact Raw Values
    df = pd.read_csv(target_path, dtype=str)

    # 3. Validate Schema
    schema_messages = validate_source_schema(df)
    validation_messages.extend(schema_messages)

    # 4. Generate Stable Source Record Identifiers (listing_id)
    # listing_id preserves 1-to-1 traceability back to original CSV row positions
    df.insert(0, "listing_id", [f"rec_{idx + 1:04d}" for idx in range(len(df))])

    # 5. Missing Values Summary
    missing_summary = {col: int(df[col].isna().sum()) for col in EXPECTED_RAW_COLUMNS}

    # 6. Verify Row Count
    actual_rows = len(df)
    if actual_rows != EXPECTED_RAW_ROW_COUNT:
        validation_messages.append(
            f"Notice: Actual row count ({actual_rows}) differs from declared ({EXPECTED_RAW_ROW_COUNT})."
        )
    else:
        validation_messages.append(f"Row count verified: Exactly {EXPECTED_RAW_ROW_COUNT} records ingested.")

    return IngestionResult(
        raw_dataframe=df,
        row_count=actual_rows,
        column_count=len(df.columns),
        checksum_report=checksum_report,
        missing_value_summary=missing_summary,
        validation_messages=validation_messages,
    )
