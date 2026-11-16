"""Deterministic, Unit-Aware Specification Parsers

Project: 'What Are We Really Paying For When We Buy a Smartphone?'
Phase 03 — Stage 02: Pipeline Foundation & Specification Parsing
"""

from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Optional

from .config import (
    FLAG_1TB_STORAGE_UNIT,
    FLAG_FRACTIONAL_MEMORY_MB,
    FLAG_FRACTIONAL_STORAGE_MB,
    FLAG_MISSING_BATTERY,
    FLAG_MISSING_CHARGING,
    FLAG_MISSING_DISPLAY_SIZE,
    FLAG_MISSING_FRONT_CAMERAS,
    FLAG_MISSING_PROCESSOR,
    FLAG_MISSING_RAM,
    FLAG_MISSING_REAR_CAMERAS,
    FLAG_MISSING_REFRESH_RATE,
    FLAG_MISSING_STORAGE,
    FLAG_UNKNOWN_DISPLAY_TECH,
    FLAG_UNPARSEABLE_FORMAT,
    FLAG_UNRESOLVED_PROCESSOR,
    GB_PER_TB,
    LCD_PANEL_KEYWORDS,
    MB_PER_GB,
    OLED_PANEL_KEYWORDS,
)


@dataclass(frozen=True)
class RamResult:
    """Parsed RAM specification and telemetry."""

    ram_capacity_gb: Optional[float]
    raw_input: Optional[str]
    quality_flags: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class StorageResult:
    """Parsed Internal Storage specification and telemetry."""

    storage_capacity_gb: Optional[float]
    raw_input: Optional[str]
    quality_flags: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class BatteryResult:
    """Parsed Battery capacity and fast-charging wattage."""

    battery_capacity_mah: Optional[int]
    charging_wattage: Optional[int]
    raw_input: Optional[str]
    quality_flags: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class DisplayResult:
    """Parsed Display specifications and technology taxonomy."""

    screen_size_inches: Optional[float]
    refresh_rate_hz: Optional[int]
    display_panel_family: Optional[str]
    display_technology_raw: Optional[str]
    raw_input: Optional[str]
    quality_flags: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class RearCameraResult:
    """Parsed Rear Camera array specifications."""

    rear_main_sensor_mp: Optional[float]
    rear_lens_count: Optional[int]
    sensor_breakdown_mp: List[float]
    raw_input: Optional[str]
    quality_flags: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class FrontCameraResult:
    """Parsed Front Camera specifications."""

    front_main_sensor_mp: Optional[float]
    front_lens_count: Optional[int]
    sensor_breakdown_mp: List[float]
    raw_input: Optional[str]
    quality_flags: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class ProcessorResult:
    """Parsed Processor specifications and component taxonomy."""

    manufacturer: Optional[str]
    family: Optional[str]
    model: Optional[str]
    core_count: Optional[int]
    cores_raw: Optional[str]
    raw_input: Optional[str]
    quality_flags: List[str] = field(default_factory=list)


@dataclass
class ParsedSpecifications:
    """Unified container for all normalized hardware specifications of a record."""

    listing_id: str
    device_id: str
    config_id: str
    ram: RamResult
    storage: StorageResult
    battery: BatteryResult
    display: DisplayResult
    rear_cameras: RearCameraResult
    front_cameras: FrontCameraResult
    processor: ProcessorResult
    all_quality_flags: List[str] = field(default_factory=list)


def parse_ram(raw_text: Optional[str]) -> RamResult:
    """Deterministic, unit-aware parser for RAM capacity.

    Converts GB to float GB (e.g., '8 GB' -> 8.0) and MB to fractional GB
    (e.g., '512 MB' -> 0.5, '32 MB' -> 0.03125). If RAM token is missing,
    returns None without attempting naive imputation.

    Args:
        raw_text: Raw string, e.g., '8 GB RAM | 128 GB Storage' or '512 MB RAM'.

    Returns:
        RamResult with normalized float in GB and quality flags.
    """
    if raw_text is None or not str(raw_text).strip():
        return RamResult(
            ram_capacity_gb=None, raw_input=raw_text, quality_flags=[FLAG_MISSING_RAM]
        )

    s = str(raw_text).strip()
    flags: List[str] = []

    # Match numbers specifically associated with RAM unit
    ram_match = re.search(r"(\d+(?:\.\d+)?)\s*(GB|MB)\s*RAM", s, re.IGNORECASE)

    if not ram_match:
        # Edge case: String has only storage (e.g. '256 MB Storage')
        return RamResult(
            ram_capacity_gb=None, raw_input=s, quality_flags=[FLAG_MISSING_RAM]
        )

    val_num = float(ram_match.group(1))
    unit = ram_match.group(2).upper()

    if unit == "GB":
        norm_val = val_num
    elif unit == "MB":
        norm_val = val_num / MB_PER_GB
        flags.append(FLAG_FRACTIONAL_MEMORY_MB)
    else:
        flags.append(FLAG_UNPARSEABLE_FORMAT)
        return RamResult(ram_capacity_gb=None, raw_input=s, quality_flags=flags)

    return RamResult(ram_capacity_gb=norm_val, raw_input=s, quality_flags=flags)


def parse_storage(raw_text: Optional[str]) -> StorageResult:
    """Deterministic, unit-aware parser for Internal Storage capacity.

    Handles TB (1 TB = 1024 GB), GB, and MB (MB / 1024 GB). Prevents the historical
    truncation bug where '1 TB Storage' was parsed as 1 GB.

    Args:
        raw_text: Raw string, e.g., '12 GB RAM | 1 TB Storage' or '256 MB Storage'.

    Returns:
        StorageResult with normalized float in GB and quality flags.
    """
    if raw_text is None or not str(raw_text).strip():
        return StorageResult(
            storage_capacity_gb=None,
            raw_input=raw_text,
            quality_flags=[FLAG_MISSING_STORAGE],
        )

    s = str(raw_text).strip()
    flags: List[str] = []

    # Match numbers associated with Storage or ROM
    stor_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(TB|GB|MB)\s*(?:Storage|ROM)", s, re.IGNORECASE
    )

    if not stor_match:
        # Fallback: check if second element of pipe exists with unit
        if "|" in s:
            parts = s.split("|")
            sec = parts[1].strip()
            fb_match = re.search(r"(\d+(?:\.\d+)?)\s*(TB|GB|MB)", sec, re.IGNORECASE)
            if fb_match:
                stor_match = fb_match

    if not stor_match:
        return StorageResult(
            storage_capacity_gb=None,
            raw_input=s,
            quality_flags=[FLAG_MISSING_STORAGE],
        )

    val_num = float(stor_match.group(1))
    unit = stor_match.group(2).upper()

    if unit == "TB":
        norm_val = val_num * GB_PER_TB
        flags.append(FLAG_1TB_STORAGE_UNIT)
    elif unit == "GB":
        norm_val = val_num
    elif unit == "MB":
        norm_val = val_num / MB_PER_GB
        flags.append(FLAG_FRACTIONAL_STORAGE_MB)
    else:
        flags.append(FLAG_UNPARSEABLE_FORMAT)
        return StorageResult(
            storage_capacity_gb=None, raw_input=s, quality_flags=flags
        )

    return StorageResult(
        storage_capacity_gb=norm_val, raw_input=s, quality_flags=flags
    )


def parse_battery(raw_text: Optional[str]) -> BatteryResult:
    """Parses Battery capacity (mAh) and Fast Charging Wattage (W) independently.

    Args:
        raw_text: Raw string, e.g., '5500 mAh | 80W Fast Charging' or '5000 mAh'.

    Returns:
        BatteryResult with capacity integer and charging wattage integer.
    """
    if raw_text is None or not str(raw_text).strip():
        return BatteryResult(
            battery_capacity_mah=None,
            charging_wattage=None,
            raw_input=raw_text,
            quality_flags=[FLAG_MISSING_BATTERY, FLAG_MISSING_CHARGING],
        )

    s = str(raw_text).strip()
    flags: List[str] = []

    # 1. Capacity in mAh
    bat_match = re.search(r"(\d+)\s*mAh", s, re.IGNORECASE)
    if bat_match:
        capacity_mah = int(bat_match.group(1))
    else:
        capacity_mah = None
        flags.append(FLAG_MISSING_BATTERY)

    # 2. Charging Wattage in W
    chg_match = re.search(
        r"(\d+(?:\.\d+)?)\s*W(?:\s+Fast\s+Charging|\s+charging|\s+wired)?",
        s,
        re.IGNORECASE,
    )
    if chg_match:
        charging_w = int(float(chg_match.group(1)))
    else:
        charging_w = None
        flags.append(FLAG_MISSING_CHARGING)

    return BatteryResult(
        battery_capacity_mah=capacity_mah,
        charging_wattage=charging_w,
        raw_input=s,
        quality_flags=flags,
    )


def parse_display(raw_text: Optional[str]) -> DisplayResult:
    """Parses Screen Size (inches), explicit Refresh Rate (Hz), and Panel Family.

    MANDATORY RULE (D03): If refresh rate is missing from the raw string,
    refresh_rate_hz strictly returns None. Never infers 60Hz.

    Args:
        raw_text: Raw string, e.g., '6.78″ (17.22 cm) 120Hz AMOLED Display'.

    Returns:
        DisplayResult with screen size, refresh rate, and panel classification.
    """
    if raw_text is None or not str(raw_text).strip():
        return DisplayResult(
            screen_size_inches=None,
            refresh_rate_hz=None,
            display_panel_family=None,
            display_technology_raw=None,
            raw_input=raw_text,
            quality_flags=[
                FLAG_MISSING_DISPLAY_SIZE,
                FLAG_MISSING_REFRESH_RATE,
                FLAG_UNKNOWN_DISPLAY_TECH,
            ],
        )

    s = str(raw_text).strip()
    flags: List[str] = []

    # 1. Screen Size in inches
    size_match = re.search(r"(\d+(?:\.\d+)?)\s*[″\"\'\u2033]", s)
    if size_match:
        size_inches = float(size_match.group(1))
    else:
        size_inches = None
        flags.append(FLAG_MISSING_DISPLAY_SIZE)

    # 2. Refresh Rate in Hz (Strict: Never infer 60Hz)
    hz_match = re.search(r"(\d+)\s*Hz", s, re.IGNORECASE)
    if hz_match:
        refresh_hz = int(hz_match.group(1))
    else:
        refresh_hz = None
        flags.append(FLAG_MISSING_REFRESH_RATE)

    # 3. Display Technology & Panel Family
    tech_match = re.search(
        r"(Dynamic AMOLED 2X|Dynamic AMOLED|Super AMOLED|AMOLED|P-OLED|OLED|IPS LCD|IPS|TFT LCD|TFT|LCD)",
        s,
        re.IGNORECASE,
    )
    if tech_match:
        tech_raw = tech_match.group(1)
        tech_lower = tech_raw.lower()

        if any(kw in tech_lower for kw in OLED_PANEL_KEYWORDS):
            panel_family = "OLED"
        elif any(kw in tech_lower for kw in LCD_PANEL_KEYWORDS):
            panel_family = "LCD"
        else:
            panel_family = "Other"
            flags.append(FLAG_UNKNOWN_DISPLAY_TECH)
    else:
        tech_raw = None
        panel_family = None
        flags.append(FLAG_UNKNOWN_DISPLAY_TECH)

    return DisplayResult(
        screen_size_inches=size_inches,
        refresh_rate_hz=refresh_hz,
        display_panel_family=panel_family,
        display_technology_raw=tech_raw,
        raw_input=s,
        quality_flags=flags,
    )


def parse_rear_cameras(raw_text: Optional[str]) -> RearCameraResult:
    """Parses Rear Camera array into main sensor MP, lens count, and breakdown.

    Preserves the original raw camera string intact.

    Args:
        raw_text: Raw string, e.g., '200+12+10+50 MP Rear Camera' or '16 MP Rear Camera'.

    Returns:
        RearCameraResult detailing main sensor, lens count, and individual sensors.
    """
    if raw_text is None or not str(raw_text).strip():
        return RearCameraResult(
            rear_main_sensor_mp=None,
            rear_lens_count=None,
            sensor_breakdown_mp=[],
            raw_input=raw_text,
            quality_flags=[FLAG_MISSING_REAR_CAMERAS],
        )

    s = str(raw_text).strip()
    flags: List[str] = []

    # Extract all numerical sensors before MP
    # Example '50+50+50 MP' -> ['50', '50', '50']
    prefix = re.split(r"\s*MP", s, flags=re.IGNORECASE)[0].strip()
    sensor_tokens = [tok.strip() for tok in prefix.split("+") if tok.strip()]

    sensors: List[float] = []
    for token in sensor_tokens:
        num_m = re.search(r"(\d+(?:\.\d+)?)", token)
        if num_m:
            sensors.append(float(num_m.group(1)))

    if not sensors:
        return RearCameraResult(
            rear_main_sensor_mp=None,
            rear_lens_count=None,
            sensor_breakdown_mp=[],
            raw_input=s,
            quality_flags=[FLAG_MISSING_REAR_CAMERAS, FLAG_UNPARSEABLE_FORMAT],
        )

    main_sensor = sensors[0]
    lens_count = len(sensors)

    return RearCameraResult(
        rear_main_sensor_mp=main_sensor,
        rear_lens_count=lens_count,
        sensor_breakdown_mp=sensors,
        raw_input=s,
        quality_flags=flags,
    )


def parse_front_cameras(raw_text: Optional[str]) -> FrontCameraResult:
    """Parses Front Camera specification into main selfie sensor MP and lens count.

    Args:
        raw_text: Raw string, e.g., '50 MP Front Camera' or '32+8 MP Front Camera'.

    Returns:
        FrontCameraResult detailing selfie sensor MP and lens count.
    """
    if raw_text is None or not str(raw_text).strip():
        return FrontCameraResult(
            front_main_sensor_mp=None,
            front_lens_count=None,
            sensor_breakdown_mp=[],
            raw_input=raw_text,
            quality_flags=[FLAG_MISSING_FRONT_CAMERAS],
        )

    s = str(raw_text).strip()
    flags: List[str] = []

    prefix = re.split(r"\s*MP", s, flags=re.IGNORECASE)[0].strip()
    sensor_tokens = [tok.strip() for tok in prefix.split("+") if tok.strip()]

    sensors: List[float] = []
    for token in sensor_tokens:
        num_m = re.search(r"(\d+(?:\.\d+)?)", token)
        if num_m:
            sensors.append(float(num_m.group(1)))

    if not sensors:
        return FrontCameraResult(
            front_main_sensor_mp=None,
            front_lens_count=None,
            sensor_breakdown_mp=[],
            raw_input=s,
            quality_flags=[FLAG_MISSING_FRONT_CAMERAS, FLAG_UNPARSEABLE_FORMAT],
        )

    main_sensor = sensors[0]
    lens_count = len(sensors)

    return FrontCameraResult(
        front_main_sensor_mp=main_sensor,
        front_lens_count=lens_count,
        sensor_breakdown_mp=sensors,
        raw_input=s,
        quality_flags=flags,
    )


def parse_processor(raw_text: Optional[str]) -> ProcessorResult:
    """Extracts semiconductor manufacturer, family, model text, and core count.

    Preserves raw processor string. HiSilicon is preserved separately from Unisoc.

    Args:
        raw_text: Raw string, e.g., 'Snapdragon 8 Gen 3 Octa core', 'Apple A17 Pro Hexa Core'.

    Returns:
        ProcessorResult detailing manufacturer, family, model, and core architecture.
    """
    if raw_text is None or not str(raw_text).strip():
        return ProcessorResult(
            manufacturer=None,
            family=None,
            model=None,
            core_count=None,
            cores_raw=None,
            raw_input=raw_text,
            quality_flags=[FLAG_MISSING_PROCESSOR],
        )

    s = str(raw_text).strip()
    flags: List[str] = []

    # 1. Cores detection
    core_match = re.search(
        r"(Deca|Octa|Hexa|Quad|Dual|Single)\s*core", s, re.IGNORECASE
    )
    if core_match:
        cores_raw = core_match.group(0)
        c_map = {
            "deca": 10,
            "octa": 8,
            "hexa": 6,
            "quad": 4,
            "dual": 2,
            "single": 1,
        }
        core_count = c_map.get(core_match.group(1).lower())
    else:
        core_count = None
        cores_raw = None

    # 2. Model text without core suffix
    cleaned_model = re.sub(
        r"\s*(Deca|Octa|Hexa|Quad|Dual|Single)\s*core", "", s, flags=re.IGNORECASE
    ).strip()

    # 3. Manufacturer & Family
    low = s.lower()
    if "snapdragon" in low or "qualcomm" in low:
        mfg = "Qualcomm"
        fam = "Snapdragon"
    elif "dimensity" in low:
        mfg = "MediaTek"
        fam = "Dimensity"
    elif "helio" in low:
        mfg = "MediaTek"
        fam = "Helio"
    elif "mediatek" in low or "mtk" in low:
        mfg = "MediaTek"
        fam = "MediaTek"
    elif "exynos" in low:
        mfg = "Samsung"
        fam = "Exynos"
    elif "apple" in low or "bionic" in low or re.search(r"\bA\d+\b", s):
        mfg = "Apple"
        fam = "Apple Silicon"
    elif "tensor" in low:
        mfg = "Google"
        fam = "Tensor"
    elif "kirin" in low or "hisilicon" in low:
        mfg = "HiSilicon"
        fam = "Kirin"
    elif "k3v2" in low:
        mfg = "HiSilicon"
        fam = "K3V2"
    elif "unisoc" in low or "spreadtrum" in low or "sc9" in low or "sc7" in low:
        mfg = "Unisoc"
        fam = "Unisoc"
    elif "intel" in low or "atom" in low:
        mfg = "Intel"
        fam = "Atom"
    elif "broadcom" in low:
        mfg = "Broadcom"
        fam = "Broadcom"
    elif "tegra" in low or "nvidia" in low:
        mfg = "Nvidia"
        fam = "Tegra"
    elif "novathor" in low or "st-ericsson" in low:
        mfg = "ST-Ericsson"
        fam = "NovaThor"
    elif "marvell" in low:
        mfg = "Marvell"
        fam = "PXA"
    else:
        # Crucial Requirement: Do not invent 'Other' manufacturer when unknown.
        # Strings that only state core count (e.g. 'Quad core', 'Tru-Octa Core')
        # strictly return manufacturer: None and family: None.
        mfg = None
        fam = None
        flags.append(FLAG_UNRESOLVED_PROCESSOR)

    return ProcessorResult(
        manufacturer=mfg,
        family=fam,
        model=cleaned_model if cleaned_model else s,
        core_count=core_count,
        cores_raw=cores_raw,
        raw_input=s,
        quality_flags=flags,
    )


def generate_device_id(model_name: str) -> str:
    """Generates canonical device model slug by stripping only memory variant tokens.

    Preserves all meaningful commercial tier and series identifiers:
    - Preserves: Pro, Plus, Ultra, 5G, Max, Lite, Fusion, Neo, GT, Prime, FE, etc.
    - Strips strictly: memory capacity tokens (e.g., '128GB', '256GB', '1TB', '8GB RAM').

    Examples from actual dataset:
    - 'Samsung Galaxy S24 Ultra 1TB'        -> 'samsung-galaxy-s24-ultra'
    - 'Samsung Galaxy S24 Plus 5G'          -> 'samsung-galaxy-s24-plus-5g'
    - 'Apple iPhone 15 Pro Max 1TB'         -> 'apple-iphone-15-pro-max'
    - 'OnePlus Nord CE 4 Lite 5G'           -> 'oneplus-nord-ce-4-lite-5g'
    - 'Xiaomi Redmi Note 13 Pro Plus 5G'    -> 'xiaomi-redmi-note-13-pro-plus-5g'
    - 'Xiaomi Mi Max 32GB'                  -> 'xiaomi-mi-max'

    Args:
        model_name: Raw model name string.

    Returns:
        Canonical slug representing the base smartphone model.
    """
    s = str(model_name).strip()
    # Strip common memory variant tokens (standalone or with RAM/Storage)
    variant_pattern = r"\s+(?:\d+GB(?:\s+RAM)?|\d+TB|\d+MB(?:\s+RAM)?|\(\d+GB\))\b"
    base = re.sub(variant_pattern, "", s, flags=re.IGNORECASE).strip()

    # Preserve plus signs semantically as 'plus' to prevent tier collisions (e.g. Reno10 Pro+ vs Reno10 Pro)
    base = re.sub(r"\+", " plus ", base)

    # Convert to lowercase slug with hyphens
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", base).strip("-").lower()
    return slug


def generate_config_id(
    device_id: str,
    ram_gb: Optional[float],
    storage_gb: Optional[float],
) -> str:
    """Generates memory-configuration identity slug (device_id + RAM + Storage).

    CRITICAL ARCHITECTURAL GUARANTEES & LIMITATIONS:
    1. Memory-Configuration Identity, Not Complete Hardware Identity:
       config_id represents strictly the observable triplet:
       (device_id, ram_capacity_gb, storage_capacity_gb).
       It does NOT assert complete hardware identity across unobserved internal
       attributes, such as board revisions, cellular modem bands, camera sensor
       lot revisions, or regional chassis colorways.
    2. Model Variant Normalization:
       Records with identical base device identity and identical observable physical
       memory specifications (such as 'Xiaomi Mi Max' and 'Xiaomi Mi Max 32GB') produce
       the exact same memory-configuration config_id while preserving distinct
       source listing_id values.
    3. Distinct Configuration Preservation:
       Hardware tiers differing in RAM or internal storage capacity (e.g., 8GB/256GB vs
       12GB/512GB) strictly receive distinct config_id values and are never merged.

    Args:
        device_id: Canonical base device slug.
        ram_gb: Normalized RAM in GB (float or None).
        storage_gb: Normalized Storage in GB (float or None).

    Returns:
        Deterministic memory-configuration slug (e.g., 'xiaomi-mi-max_3gb_32gb').
    """
    ram_str = (
        f"{ram_gb:g}gb" if ram_gb is not None and ram_gb >= 1.0
        else f"{int(ram_gb * 1024)}mb" if ram_gb is not None
        else "noram"
    )

    stor_str = (
        f"{int(storage_gb)}gb" if storage_gb is not None and storage_gb >= 1.0
        else f"{int(storage_gb * 1024)}mb" if storage_gb is not None
        else "nostorage"
    )

    return f"{device_id}_{ram_str}_{stor_str}"


def parse_all_specifications(
    row_dict: Dict[str, Any], listing_id: str
) -> ParsedSpecifications:
    """Unified entry point parsing all hardware specifications for a raw row.

    Combines independent parsers and aggregates quality flags into an immutable structure.

    Args:
        row_dict: Dictionary containing raw dataset columns.
        listing_id: Stable source record identifier.

    Returns:
        ParsedSpecifications dataclass with complete normalized attributes.
    """
    model_name = row_dict.get("model_name", "")
    device_id = generate_device_id(str(model_name))

    mem_raw = row_dict.get("ram_internal_memory")
    ram_res = parse_ram(mem_raw)
    stor_res = parse_storage(mem_raw)

    config_id = generate_config_id(
        device_id=device_id,
        ram_gb=ram_res.ram_capacity_gb,
        storage_gb=stor_res.storage_capacity_gb,
    )

    battery_res = parse_battery(row_dict.get("battery"))
    display_res = parse_display(row_dict.get("display"))
    rear_cam_res = parse_rear_cameras(row_dict.get("rear_cameras"))
    front_cam_res = parse_front_cameras(row_dict.get("front_cameras"))
    proc_res = parse_processor(row_dict.get("processor"))

    # Aggregate quality flags
    all_flags = (
        ram_res.quality_flags
        + stor_res.quality_flags
        + battery_res.quality_flags
        + display_res.quality_flags
        + rear_cam_res.quality_flags
        + front_cam_res.quality_flags
        + proc_res.quality_flags
    )

    return ParsedSpecifications(
        listing_id=listing_id,
        device_id=device_id,
        config_id=config_id,
        ram=ram_res,
        storage=stor_res,
        battery=battery_res,
        display=display_res,
        rear_cameras=rear_cam_res,
        front_cameras=front_cam_res,
        processor=proc_res,
        all_quality_flags=all_flags,
    )
