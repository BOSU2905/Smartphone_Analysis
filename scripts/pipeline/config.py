"""Pipeline Configuration & Data Schema Constants

Project: 'What Are We Really Paying For When We Buy a Smartphone?'
Phase 03 — Stage 02: Pipeline Foundation & Specification Parsing
"""

from pathlib import Path
from typing import Final, List, Set

# Base Paths
REPO_ROOT: Final[Path] = Path(__file__).resolve().parents[2]
DATA_DIR: Final[Path] = REPO_ROOT / "Data"
RAW_DATA_PATH: Final[Path] = DATA_DIR / "raw" / "smartphones_uncleaned.csv"

# Immutable Raw File Checksums (Verified Ground Truth)
RAW_FILE_EXPECTED_BYTES: Final[int] = 1196334
RAW_FILE_EXPECTED_SHA256: Final[str] = (
    "ddee99b4f65d131e424027e3e4f91a112bffaaa124d59956a93f285bf14459ea"
)
RAW_FILE_EXPECTED_MD5: Final[str] = "47eaa10ce989ee22c659ffea142bfd1e"
EXPECTED_RAW_ROW_COUNT: Final[int] = 2928

# Expected Raw Dataset Schema
EXPECTED_RAW_COLUMNS: Final[List[str]] = [
    "model_name",
    "price",
    "expert_rating",
    "user_rating",
    "processor",
    "rear_cameras",
    "front_cameras",
    "display",
    "ram_internal_memory",
    "battery",
    "operating_system",
    "additional_features",
    "review",
    "review_link",
]

# Mathematical Unit Conversion Constants
MB_PER_GB: Final[float] = 1024.0
GB_PER_TB: Final[float] = 1024.0

# Data Quality Flags (Auditable Data Lineage)
FLAG_MISSING_RAM: Final[str] = "MISSING_RAM"
FLAG_MISSING_STORAGE: Final[str] = "MISSING_STORAGE"
FLAG_FRACTIONAL_MEMORY_MB: Final[str] = "FRACTIONAL_MEMORY_MB"
FLAG_FRACTIONAL_STORAGE_MB: Final[str] = "FRACTIONAL_STORAGE_MB"
FLAG_1TB_STORAGE_UNIT: Final[str] = "1TB_STORAGE_UNIT"
FLAG_MISSING_BATTERY: Final[str] = "MISSING_BATTERY"
FLAG_MISSING_CHARGING: Final[str] = "MISSING_CHARGING_WATTAGE"
FLAG_MISSING_DISPLAY_SIZE: Final[str] = "MISSING_DISPLAY_SIZE"
FLAG_MISSING_REFRESH_RATE: Final[str] = "MISSING_REFRESH_RATE"
FLAG_UNKNOWN_DISPLAY_TECH: Final[str] = "UNKNOWN_DISPLAY_TECH"
FLAG_MISSING_REAR_CAMERAS: Final[str] = "MISSING_REAR_CAMERAS"
FLAG_MISSING_FRONT_CAMERAS: Final[str] = "MISSING_FRONT_CAMERAS"
FLAG_MISSING_PROCESSOR: Final[str] = "MISSING_PROCESSOR"
FLAG_UNRESOLVED_PROCESSOR: Final[str] = "UNRESOLVED_PROCESSOR_MANUFACTURER"
FLAG_UNPARSEABLE_FORMAT: Final[str] = "UNPARSEABLE_FORMAT"
FLAG_ALIAS_CANDIDATE: Final[str] = "ALIAS_CANDIDATE_REVIEW"
FLAG_MISSING_EXPERT_RATING: Final[str] = "MISSING_EXPERT_RATING"
FLAG_INVALID_EXPERT_RATING: Final[str] = "INVALID_EXPERT_RATING"
FLAG_MISSING_USER_RATING: Final[str] = "MISSING_USER_RATING"
FLAG_INVALID_USER_RATING: Final[str] = "INVALID_USER_RATING"
FLAG_UNPARSEABLE_USER_RATING: Final[str] = "INVALID_USER_RATING"
FLAG_MISSING_REVIEW_SNIPPET: Final[str] = "MISSING_REVIEW_SNIPPET"
FLAG_MISSING_REVIEW_URL: Final[str] = "MISSING_REVIEW_URL"
FLAG_REVIEW_SNIPPET_WITHOUT_URL: Final[str] = "REVIEW_SNIPPET_WITHOUT_URL"
FLAG_REVIEW_URL_WITHOUT_SNIPPET: Final[str] = "REVIEW_URL_WITHOUT_SNIPPET"
FLAG_UNKNOWN_BRAND: Final[str] = "UNKNOWN_BRAND"
FLAG_UNKNOWN_PARENT_COMPANY: Final[str] = "UNKNOWN_PARENT_COMPANY"

# Display Technology Families
OLED_PANEL_KEYWORDS: Final[Set[str]] = {
    "dynamic amoled 2x",
    "dynamic amoled",
    "super amoled",
    "amoled",
    "p-oled",
    "oled",
}

LCD_PANEL_KEYWORDS: Final[Set[str]] = {
    "ips lcd",
    "ips",
    "tft lcd",
    "tft",
    "lcd",
}
