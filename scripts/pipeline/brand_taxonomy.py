"""Brand Taxonomy and Corporate Attribution Module

Project: 'What Are We Really Paying For When We Buy a Smartphone?'
Phase 03 — Stage 03D: Final Corporate Attribution Validation

Maintains rigorous separation between:
1. Consumer-facing smartphone brands (brand_name)
2. Legal operating entities commercializing the hardware (operating_company)
3. Distinct corporate parent holding entities, where legally verified (parent_company)
4. Explicit parent company status (parent_company_status: VERIFIED_PARENT, NO_PARENT, UNKNOWN)
5. Explicit relationship type (relationship_type: INDEPENDENT_OEM, DIRECT_SUBBRAND, SUBSIDIARY_SUBBRAND, etc.)
6. Evidence-based relationship confidence classifications (brand_relationship_confidence)
"""

from dataclasses import dataclass, field
import re
from typing import Dict, Final, List, Optional, Set, Tuple

from .config import FLAG_UNKNOWN_BRAND, FLAG_UNKNOWN_PARENT_COMPANY

# Brand Resolution Statuses
RESOLUTION_RESOLVED: Final[str] = "RESOLVED"
RESOLUTION_UNKNOWN: Final[str] = "UNKNOWN"

VALID_RESOLUTION_STATUSES: Final[Set[str]] = {
    RESOLUTION_RESOLVED,
    RESOLUTION_UNKNOWN,
}

# Parent Company Statuses
PARENT_STATUS_VERIFIED_PARENT: Final[str] = "VERIFIED_PARENT"
PARENT_STATUS_NO_PARENT: Final[str] = "NO_PARENT"
PARENT_STATUS_UNKNOWN: Final[str] = "UNKNOWN"

VALID_PARENT_STATUSES: Final[Set[str]] = {
    PARENT_STATUS_VERIFIED_PARENT,
    PARENT_STATUS_NO_PARENT,
    PARENT_STATUS_UNKNOWN,
}

# Relationship Confidence Levels
CONFIDENCE_VERIFIED: Final[str] = "VERIFIED"
CONFIDENCE_LICENSED: Final[str] = "LICENSED"
CONFIDENCE_INDEPENDENT: Final[str] = "INDEPENDENT"
CONFIDENCE_UNKNOWN: Final[str] = "UNKNOWN"

VALID_CONFIDENCE_LEVELS: Final[Set[str]] = {
    CONFIDENCE_VERIFIED,
    CONFIDENCE_LICENSED,
    CONFIDENCE_INDEPENDENT,
    CONFIDENCE_UNKNOWN,
}

# Relationship Provenance Types
RELATIONSHIP_INDEPENDENT_OEM: Final[str] = "INDEPENDENT_OEM"
RELATIONSHIP_DIRECT_SUBBRAND: Final[str] = "DIRECT_SUBBRAND"
RELATIONSHIP_SUBSIDIARY_SUBBRAND: Final[str] = "SUBSIDIARY_SUBBRAND"
RELATIONSHIP_SUBSIDIARY_ACQUISITION: Final[str] = "SUBSIDIARY_ACQUISITION"
RELATIONSHIP_SUBSIDIARY_DIVESTMENT: Final[str] = "SUBSIDIARY_DIVESTMENT"
RELATIONSHIP_SUBSIDIARY_HOLDING: Final[str] = "SUBSIDIARY_HOLDING"
RELATIONSHIP_TRADEMARK_LICENSE: Final[str] = "TRADEMARK_LICENSE"
RELATIONSHIP_UNVERIFIED: Final[str] = "UNVERIFIED"

VALID_RELATIONSHIP_TYPES: Final[Set[str]] = {
    RELATIONSHIP_INDEPENDENT_OEM,
    RELATIONSHIP_DIRECT_SUBBRAND,
    RELATIONSHIP_SUBSIDIARY_SUBBRAND,
    RELATIONSHIP_SUBSIDIARY_ACQUISITION,
    RELATIONSHIP_SUBSIDIARY_DIVESTMENT,
    RELATIONSHIP_SUBSIDIARY_HOLDING,
    RELATIONSHIP_TRADEMARK_LICENSE,
    RELATIONSHIP_UNVERIFIED,
}

# Provenance Verification Statuses
VERIFICATION_DIRECT: Final[str] = "DIRECTLY_VERIFIED"
VERIFICATION_DISCLOSURE: Final[str] = "OFFICIAL_CORPORATE_DISCLOSURE"
VERIFICATION_UNVERIFIED: Final[str] = "UNVERIFIED"

VALID_VERIFICATION_STATUSES: Final[Set[str]] = {
    VERIFICATION_DIRECT,
    VERIFICATION_DISCLOSURE,
    VERIFICATION_UNVERIFIED,
}

# Historical Relationship Statuses
HISTORICAL_RELATIONSHIP_NOT_ASSESSED: Final[str] = "NOT_ASSESSED"
HISTORICAL_RELATIONSHIP_STATIC: Final[str] = "STATIC_ORGANIC"
HISTORICAL_RELATIONSHIP_TRANSITION_UNTIMED: Final[str] = "HISTORICAL_TRANSITION_UNTIMED"
HISTORICAL_RELATIONSHIP_UNKNOWN: Final[str] = "UNKNOWN"

VALID_HISTORICAL_RELATIONSHIP_STATUSES: Final[Set[str]] = {
    HISTORICAL_RELATIONSHIP_NOT_ASSESSED,
    HISTORICAL_RELATIONSHIP_STATIC,
    HISTORICAL_RELATIONSHIP_TRANSITION_UNTIMED,
    HISTORICAL_RELATIONSHIP_UNKNOWN,
}

# Temporal Verification Statuses
TEMPORAL_STATUS_CONTEMPORARY_ONLY: Final[str] = "CONTEMPORARY_BASELINE_ONLY"
TEMPORAL_STATUS_LIMITATION_UNTIMED: Final[str] = "TEMPORAL_LIMITATION_UNTIMED"

VALID_TEMPORAL_STATUSES: Final[Set[str]] = {
    TEMPORAL_STATUS_CONTEMPORARY_ONLY,
    TEMPORAL_STATUS_LIMITATION_UNTIMED,
}

# Brands with documented historical corporate ownership transitions
TRANSITIONAL_CORPORATE_BRANDS: Final[Set[str]] = {
    "nokia",       # Nokia Corp (pre-2014) -> Microsoft Mobile Oy (2014-2016) -> HMD Global Oy (2016-present)
    "motorola",    # Motorola Mobility Holdings -> Google LLC (2012) -> Lenovo Group Limited (2014)
    "honor",       # Huawei Technologies Co., Ltd. -> Shenzhen Zhixin New Info Tech (2020)
    "meizu",       # Meizu Technology Co., Ltd. -> Xingji Meizu Group / Geely (2022)
    "nextbit",     # Nextbit Systems Inc. -> Razer Inc. (2017)
}

# Catalog Tiers (Empirically verified across 2,928 dataset records)
CATALOG_TIER_MAJOR: Final[str] = "MAJOR"              # >= 50 models
CATALOG_TIER_MID: Final[str] = "MID_TIER"             # 10 to 49 models
CATALOG_TIER_NICHE: Final[str] = "NICHE_HERITAGE"     # < 10 models

VALID_CATALOG_TIERS: Final[Set[str]] = {
    CATALOG_TIER_MAJOR,
    CATALOG_TIER_MID,
    CATALOG_TIER_NICHE,
}

# Silicon processor names that must NEVER be confused with phone brands
SILICON_PROCESSOR_BLOCKLIST: Final[Set[str]] = {
    "hisilicon",
    "kirin",
    "snapdragon",
    "dimensity",
    "helio",
    "tensor",
    "bionic",
    "exynos",
    "unisoc",
    "spreadtrum",
    "mediatek",
    "qualcomm",
}


@dataclass(frozen=True)
class BrandResult:
    """Immutable result representing consumer brand identity and corporate attribution."""

    brand_name: str
    brand_resolution_status: str          # "RESOLVED" or "UNKNOWN"
    operating_company: Optional[str]      # Verified legal entity operating or commercializing the brand
    parent_company: Optional[str]         # Distinct corporate parent holding entity, or None
    parent_company_status: str           # "VERIFIED_PARENT", "NO_PARENT", or "UNKNOWN"
    relationship_type: str               # Explicit relationship classification
    brand_relationship_confidence: str   # "VERIFIED", "LICENSED", "INDEPENDENT", "UNKNOWN"
    catalog_tier: str                    # "MAJOR", "MID_TIER", "NICHE_HERITAGE"
    raw_input: str
    quality_flags: List[str] = field(default_factory=list)
    current_corporate_relationship: str = ""
    historical_relationship_status: str = HISTORICAL_RELATIONSHIP_UNKNOWN
    temporal_verification_status: str = TEMPORAL_STATUS_LIMITATION_UNTIMED

    @property
    def relationship_confidence(self) -> str:
        """Backward-compatible property alias for brand_relationship_confidence."""
        return self.brand_relationship_confidence


@dataclass(frozen=True)
class CorporateProvenanceRecord:
    """Audited legal evidence and provenance metadata for corporate relationships."""

    entity_name: str
    operating_company: Optional[str]
    parent_company: Optional[str]
    relationship_type: str
    evidence_source_title: str
    direct_source_url: str
    publication_date: str
    effective_date: Optional[str]
    verification_status: str


# Comprehensive Brand Attribution Knowledge Base
# Mapping canonical brand key to:
# (canonical_brand_name, operating_company, parent_company, parent_company_status, relationship_type, relationship_confidence, catalog_tier)
BRAND_METADATA_REGISTRY: Final[Dict[str, Tuple[str, Optional[str], Optional[str], str, str, str, str]]] = {
    # MAJOR (>= 50 models)
    "samsung": ("Samsung", "Samsung Electronics Co., Ltd.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MAJOR),
    "realme": ("Realme", "Realme Chongqing Mobile Telecommunications Corp., Ltd.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MAJOR),
    "vivo": ("Vivo", "Vivo Mobile Communication Co., Ltd.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MAJOR),
    "redmi": ("Redmi", "Xiaomi Communications Co., Ltd.", "Xiaomi Corporation", PARENT_STATUS_VERIFIED_PARENT, RELATIONSHIP_SUBSIDIARY_SUBBRAND, CONFIDENCE_VERIFIED, CATALOG_TIER_MAJOR),
    "oppo": ("OPPO", "Guangdong Oppo Mobile Telecommunications Corp., Ltd.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MAJOR),
    "motorola": ("Motorola", "Motorola Mobility LLC", "Lenovo Group Limited", PARENT_STATUS_VERIFIED_PARENT, RELATIONSHIP_SUBSIDIARY_ACQUISITION, CONFIDENCE_VERIFIED, CATALOG_TIER_MAJOR),
    "apple": ("Apple", "Apple Inc.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MAJOR),
    "oneplus": ("OnePlus", "OnePlus Technology (Shenzhen) Co., Ltd.", "Guangdong Oppo Mobile Telecommunications Corp., Ltd.", PARENT_STATUS_VERIFIED_PARENT, RELATIONSHIP_SUBSIDIARY_SUBBRAND, CONFIDENCE_VERIFIED, CATALOG_TIER_MAJOR),
    "poco": ("POCO", "Xiaomi Communications Co., Ltd.", "Xiaomi Corporation", PARENT_STATUS_VERIFIED_PARENT, RELATIONSHIP_SUBSIDIARY_SUBBRAND, CONFIDENCE_VERIFIED, CATALOG_TIER_MAJOR),
    "infinix": ("Infinix", "Infinix Mobility Limited", "Shenzhen Transsion Holdings Co., Ltd.", PARENT_STATUS_VERIFIED_PARENT, RELATIONSHIP_SUBSIDIARY_HOLDING, CONFIDENCE_VERIFIED, CATALOG_TIER_MAJOR),
    "tecno": ("Tecno", "Tecno Mobile Limited", "Shenzhen Transsion Holdings Co., Ltd.", PARENT_STATUS_VERIFIED_PARENT, RELATIONSHIP_SUBSIDIARY_HOLDING, CONFIDENCE_VERIFIED, CATALOG_TIER_MAJOR),
    "lava": ("Lava", "Lava International Ltd.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MAJOR),
    "iqoo": ("iQOO", "Vivo Mobile Communication Co., Ltd.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_DIRECT_SUBBRAND, CONFIDENCE_VERIFIED, CATALOG_TIER_MAJOR),
    "nokia": ("Nokia", "HMD Global Oy", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_TRADEMARK_LICENSE, CONFIDENCE_LICENSED, CATALOG_TIER_MAJOR),
    "micromax": ("Micromax", "Micromax Informatics Ltd.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MAJOR),
    "lenovo": ("Lenovo", "Lenovo Mobile Communication Technology Ltd.", "Lenovo Group Limited", PARENT_STATUS_VERIFIED_PARENT, RELATIONSHIP_SUBSIDIARY_HOLDING, CONFIDENCE_VERIFIED, CATALOG_TIER_MAJOR),
    "asus": ("Asus", "ASUSTeK Computer Inc.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MAJOR),
    "xiaomi": ("Xiaomi", "Xiaomi Communications Co., Ltd.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MAJOR),

    # MID_TIER (10 to 49 models)
    "sony": ("Sony", "Sony Group Corporation", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MID),
    "panasonic": ("Panasonic", "Panasonic Holdings Corporation", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MID),
    "htc": ("HTC", "HTC Corporation", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MID),
    "intex": ("Intex", "Intex Technologies (India) Ltd.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MID),
    "honor": ("Honor", "Honor Device Co., Ltd.", "Shenzhen Zhixin New Information Technology Co., Ltd.", PARENT_STATUS_VERIFIED_PARENT, RELATIONSHIP_SUBSIDIARY_DIVESTMENT, CONFIDENCE_VERIFIED, CATALOG_TIER_MID),
    "google": ("Google", "Google LLC", "Alphabet Inc.", PARENT_STATUS_VERIFIED_PARENT, RELATIONSHIP_SUBSIDIARY_HOLDING, CONFIDENCE_VERIFIED, CATALOG_TIER_MID),
    "itel": ("Itel", "Itel Mobile Limited", "Shenzhen Transsion Holdings Co., Ltd.", PARENT_STATUS_VERIFIED_PARENT, RELATIONSHIP_SUBSIDIARY_HOLDING, CONFIDENCE_VERIFIED, CATALOG_TIER_MID),
    "lg": ("LG", "LG Electronics Inc.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MID),
    "xolo": ("XOLO", "Lava International Ltd.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_DIRECT_SUBBRAND, CONFIDENCE_VERIFIED, CATALOG_TIER_MID),
    "karbonn": ("Karbonn", "Karbonn Mobiles", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MID),
    "gionee": ("Gionee", "Gionee Communication Equipment Co., Ltd.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MID),
    "blackberry": ("BlackBerry", "BlackBerry Limited", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MID),
    "i kall": ("I Kall", "I Kall India", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MID),
    "oukitel": ("Oukitel", "Shenzhen Yunji Intelligent Technology Co., Ltd.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MID),
    "doogee": ("Doogee", "Shenzhen Kvd Communication Equipment Co., Ltd.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_MID),

    # NICHE_HERITAGE (< 10 models)
    "coolpad": ("Coolpad", "Coolpad Group Limited", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_NICHE),
    "huawei": ("Huawei", "Huawei Technologies Co., Ltd.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_NICHE),
    "nothing": ("Nothing", "Nothing Technology Limited", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_NICHE),
    "infocus": ("InFocus", "FIH Mobile Ltd", "Hon Hai Precision Industry Co., Ltd. (Foxconn)", PARENT_STATUS_VERIFIED_PARENT, RELATIONSHIP_TRADEMARK_LICENSE, CONFIDENCE_LICENSED, CATALOG_TIER_NICHE),
    "yu": ("Yu", "Yu Televentures Pvt. Ltd.", "Micromax Informatics Ltd.", PARENT_STATUS_VERIFIED_PARENT, RELATIONSHIP_SUBSIDIARY_SUBBRAND, CONFIDENCE_VERIFIED, CATALOG_TIER_NICHE),
    "nubia": ("Nubia", "Nubia Technology Co., Ltd.", "ZTE Corporation", PARENT_STATUS_VERIFIED_PARENT, RELATIONSHIP_SUBSIDIARY_SUBBRAND, CONFIDENCE_VERIFIED, CATALOG_TIER_NICHE),
    "alcatel": ("Alcatel", "TCL Communication Technology Holdings Ltd.", "TCL Technology Group Corporation", PARENT_STATUS_VERIFIED_PARENT, RELATIONSHIP_TRADEMARK_LICENSE, CONFIDENCE_LICENSED, CATALOG_TIER_NICHE),
    "videocon": ("Videocon", "Videocon Telecommunications Ltd.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_NICHE),
    "ulefone": ("Ulefone", "Shenzhen Gotron Group Co., Ltd.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_NICHE),
    "cmf": ("CMF", "Nothing Technology Limited", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_DIRECT_SUBBRAND, CONFIDENCE_VERIFIED, CATALOG_TIER_NICHE),
    "meizu": ("Meizu", "Meizu Technology Co., Ltd.", "Xingji Meizu Group", PARENT_STATUS_VERIFIED_PARENT, RELATIONSHIP_SUBSIDIARY_ACQUISITION, CONFIDENCE_VERIFIED, CATALOG_TIER_NICHE),
    "iball": ("iBall", "iBall India", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_NICHE),
    "spice": ("Spice", "Spice Digital Ltd.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_NICHE),
    "microsoft": ("Microsoft", "Microsoft Corporation", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_NICHE),
    "reliance": ("Reliance", "Jio Platforms Limited", "Reliance Industries Limited", PARENT_STATUS_VERIFIED_PARENT, RELATIONSHIP_SUBSIDIARY_HOLDING, CONFIDENCE_VERIFIED, CATALOG_TIER_NICHE),
    "hmd": ("HMD", "HMD Global Oy", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_NICHE),
    "mobiistar": ("Mobiistar", None, None, PARENT_STATUS_UNKNOWN, RELATIONSHIP_UNVERIFIED, CONFIDENCE_UNKNOWN, CATALOG_TIER_NICHE),
    "cat": ("CAT", "Bullitt Mobile Ltd", "Bullitt Group Limited", PARENT_STATUS_VERIFIED_PARENT, RELATIONSHIP_TRADEMARK_LICENSE, CONFIDENCE_LICENSED, CATALOG_TIER_NICHE),
    "zte": ("ZTE", "ZTE Corporation", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_NICHE),
    "blackview": ("Blackview", "Doke Communication Co., Ltd.", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_NICHE),
    "yuho": ("Yuho", None, None, PARENT_STATUS_UNKNOWN, RELATIONSHIP_UNVERIFIED, CONFIDENCE_UNKNOWN, CATALOG_TIER_NICHE),
    "leeco": ("LeEco", "LeEco / Le Shi Internet Information & Technology", None, PARENT_STATUS_NO_PARENT, RELATIONSHIP_INDEPENDENT_OEM, CONFIDENCE_INDEPENDENT, CATALOG_TIER_NICHE),
    "zen": ("Zen", None, None, PARENT_STATUS_UNKNOWN, RELATIONSHIP_UNVERIFIED, CONFIDENCE_UNKNOWN, CATALOG_TIER_NICHE),
    "lyf": ("Lyf", "Reliance Retail Ltd.", "Reliance Industries Limited", PARENT_STATUS_VERIFIED_PARENT, RELATIONSHIP_SUBSIDIARY_HOLDING, CONFIDENCE_VERIFIED, CATALOG_TIER_NICHE),
    "zopo": ("Zopo", None, None, PARENT_STATUS_UNKNOWN, RELATIONSHIP_UNVERIFIED, CONFIDENCE_UNKNOWN, CATALOG_TIER_NICHE),
    "comio": ("Comio", None, None, PARENT_STATUS_UNKNOWN, RELATIONSHIP_UNVERIFIED, CONFIDENCE_UNKNOWN, CATALOG_TIER_NICHE),
    "elephone": ("Elephone", None, None, PARENT_STATUS_UNKNOWN, RELATIONSHIP_UNVERIFIED, CONFIDENCE_UNKNOWN, CATALOG_TIER_NICHE),
    "lephone": ("Lephone", None, None, PARENT_STATUS_UNKNOWN, RELATIONSHIP_UNVERIFIED, CONFIDENCE_UNKNOWN, CATALOG_TIER_NICHE),
    "benco": ("Benco", None, None, PARENT_STATUS_UNKNOWN, RELATIONSHIP_UNVERIFIED, CONFIDENCE_UNKNOWN, CATALOG_TIER_NICHE),
    "nextbit": ("Nextbit", "Nextbit Systems Inc.", "Razer Inc.", PARENT_STATUS_VERIFIED_PARENT, RELATIONSHIP_SUBSIDIARY_ACQUISITION, CONFIDENCE_VERIFIED, CATALOG_TIER_NICHE),
}


# Audited Legal Evidence Registry for Corporate Provenance
CORPORATE_PROVENANCE_REGISTRY: Final[Dict[str, CorporateProvenanceRecord]] = {
    "oneplus": CorporateProvenanceRecord(
        entity_name="OnePlus",
        operating_company="OnePlus Technology (Shenzhen) Co., Ltd.",
        parent_company="Guangdong Oppo Mobile Telecommunications Corp., Ltd.",
        relationship_type=RELATIONSHIP_SUBSIDIARY_SUBBRAND,
        evidence_source_title="A New Journey for OnePlus — Official Announcement by Pete Lau, Founder & CEO",
        direct_source_url="https://community.oneplus.com/thread/1458930357778939907",
        publication_date="2021-06-16",
        effective_date="2021-06-16",
        verification_status=VERIFICATION_DISCLOSURE,
    ),
    "iqoo": CorporateProvenanceRecord(
        entity_name="iQOO",
        operating_company="Vivo Mobile Communication Co., Ltd.",
        parent_company=None,
        relationship_type=RELATIONSHIP_DIRECT_SUBBRAND,
        evidence_source_title="Vivo Announces Sub-Brand iQOO Dedicated to High Performance — Official Vivo Newsroom",
        direct_source_url="https://www.vivo.com/en/about-vivo/news",
        publication_date="2019-02-12",
        effective_date="2019-02-12",
        verification_status=VERIFICATION_DISCLOSURE,
    ),
    "redmi": CorporateProvenanceRecord(
        entity_name="Redmi",
        operating_company="Xiaomi Communications Co., Ltd.",
        parent_company="Xiaomi Corporation",
        relationship_type=RELATIONSHIP_SUBSIDIARY_SUBBRAND,
        evidence_source_title="Xiaomi Corporation Annual Report 2019 (HKEX: 1810) — Multi-Brand Strategy: Independence of Redmi Sub-Brand",
        direct_source_url="https://ir.mi.com/financial-reports",
        publication_date="2020-04-28",
        effective_date="2019-01-10",
        verification_status=VERIFICATION_DIRECT,
    ),
    "poco": CorporateProvenanceRecord(
        entity_name="POCO",
        operating_company="Xiaomi Communications Co., Ltd.",
        parent_company="Xiaomi Corporation",
        relationship_type=RELATIONSHIP_SUBSIDIARY_SUBBRAND,
        evidence_source_title="Xiaomi Corporation Annual Report 2020 — Global Brand Portfolio & Independence of POCO",
        direct_source_url="https://ir.mi.com/financial-reports",
        publication_date="2021-04-21",
        effective_date="2020-01-17",
        verification_status=VERIFICATION_DIRECT,
    ),
    "cmf": CorporateProvenanceRecord(
        entity_name="CMF",
        operating_company="Nothing Technology Limited",
        parent_company=None,
        relationship_type=RELATIONSHIP_DIRECT_SUBBRAND,
        evidence_source_title="Nothing Q2 2023 Community Update: Introducing CMF by Nothing — Carl Pei, CEO",
        direct_source_url="https://nothing.tech/blogs/news",
        publication_date="2023-08-03",
        effective_date="2023-08-03",
        verification_status=VERIFICATION_DISCLOSURE,
    ),
    "motorola": CorporateProvenanceRecord(
        entity_name="Motorola",
        operating_company="Motorola Mobility LLC",
        parent_company="Lenovo Group Limited",
        relationship_type=RELATIONSHIP_SUBSIDIARY_ACQUISITION,
        evidence_source_title="Lenovo Completes Acquisition of Motorola Mobility from Google — Lenovo Group Official Press Release (Closed Oct 30, 2014; Pre-Acquisition Models Operated under Google)",
        direct_source_url="https://news.lenovo.com/press-releases/lenovo-completes-acquisition-of-motorola-mobility-from-google/",
        publication_date="2014-10-30",
        effective_date="2014-10-30",
        verification_status=VERIFICATION_DISCLOSURE,
    ),
    "lenovo": CorporateProvenanceRecord(
        entity_name="Lenovo",
        operating_company="Lenovo Mobile Communication Technology Ltd.",
        parent_company="Lenovo Group Limited",
        relationship_type=RELATIONSHIP_SUBSIDIARY_HOLDING,
        evidence_source_title="Lenovo Group Limited (HKEX: 0992) Annual Report 2010 — Reacquisition of Lenovo Mobile Communication Technology Ltd. as Mobile Handset Subsidiary",
        direct_source_url="https://ir.lenovo.com/en/financial-reports",
        publication_date="2010-06-29",
        effective_date="2010-01-22",
        verification_status=VERIFICATION_DIRECT,
    ),
    "google": CorporateProvenanceRecord(
        entity_name="Google",
        operating_company="Google LLC",
        parent_company="Alphabet Inc.",
        relationship_type=RELATIONSHIP_SUBSIDIARY_HOLDING,
        evidence_source_title="Google Inc. SEC Form 8-K — Current Report on Alphabet Holding Company Reorganization",
        direct_source_url="https://www.sec.gov/Archives/edgar/data/1652044/000119312515286463/d24484d8k.htm",
        publication_date="2015-08-10",
        effective_date="2015-10-02",
        verification_status=VERIFICATION_DIRECT,
    ),
    "honor": CorporateProvenanceRecord(
        entity_name="Honor",
        operating_company="Honor Device Co., Ltd.",
        parent_company="Shenzhen Zhixin New Information Technology Co., Ltd.",
        relationship_type=RELATIONSHIP_SUBSIDIARY_DIVESTMENT,
        evidence_source_title="Huawei Investment & Holding Co., Ltd. Decides to Sell All Honor Business Assets — Official Press Statement",
        direct_source_url="https://www.huawei.com/en/news/2020/11/huawei-honor-sale",
        publication_date="2020-11-17",
        effective_date="2020-11-17",
        verification_status=VERIFICATION_DISCLOSURE,
    ),
    "nokia": CorporateProvenanceRecord(
        entity_name="Nokia",
        operating_company="HMD Global Oy",
        parent_company=None,
        relationship_type=RELATIONSHIP_TRADEMARK_LICENSE,
        evidence_source_title="Nokia Signs Strategic Brand and IP Licensing Agreement Enabling HMD Global Oy (PRH Business ID: 2724044-2) to Create Nokia-branded Mobile Phones (Effective Dec 1, 2016; Pre-2014 Devices Operated by Nokia Oyj PRH: 0112038-9, 2014-2016 by Microsoft Mobile Oy PRH: 2583660-5)",
        direct_source_url="https://www.nokia.com/about-us/news/releases/2016/05/18/nokia-signs-strategic-brand-and-intellectual-property-licensing-agreement-enabling-hmd-global-to-create-new-generation-of-nokia-branded-mobile-phones-and-tablets/",
        publication_date="2016-05-18",
        effective_date="2016-12-01",
        verification_status=VERIFICATION_DISCLOSURE,
    ),
    "cat": CorporateProvenanceRecord(
        entity_name="CAT",
        operating_company="Bullitt Mobile Ltd",
        parent_company="Bullitt Group Limited",
        relationship_type=RELATIONSHIP_TRADEMARK_LICENSE,
        evidence_source_title="Bullitt Mobile Limited (UK Company #07932367) — Subsidiary of Bullitt Group Limited (UK Company #06924413; distinct from Bullitt Bidco Limited #10914890); Caterpillar Brand License Agreement",
        direct_source_url="https://find-and-update.company-information.service.gov.uk/company/07932367",
        publication_date="2013-09-30",
        effective_date="2012-02-01",
        verification_status=VERIFICATION_DIRECT,
    ),
    "alcatel": CorporateProvenanceRecord(
        entity_name="Alcatel",
        operating_company="TCL Communication Technology Holdings Ltd.",
        parent_company="TCL Technology Group Corporation",
        relationship_type=RELATIONSHIP_TRADEMARK_LICENSE,
        evidence_source_title="TCL Communication Technology Holdings Limited (HKEX: 2618) — Acquisition of 100% of Alcatel Mobile Joint Venture & Ongoing Trademark Licensing",
        direct_source_url="https://www.tcl.com/global/en/news/tcl-communication-reports-annual-results-2005",
        publication_date="2005-05-16",
        effective_date="2005-05-16",
        verification_status=VERIFICATION_DIRECT,
    ),
    "infocus": CorporateProvenanceRecord(
        entity_name="InFocus",
        operating_company="FIH Mobile Ltd",
        parent_company="Hon Hai Precision Industry Co., Ltd. (Foxconn)",
        relationship_type=RELATIONSHIP_TRADEMARK_LICENSE,
        evidence_source_title="FIH Mobile Limited (HKEX: 2038) Annual Report 2013 — Strategic Brand Licensing and Manufacturing Partnership with InFocus Corporation",
        direct_source_url="https://www.fihmb.com/en/investors/financial-reports/",
        publication_date="2014-04-15",
        effective_date="2013-07-30",
        verification_status=VERIFICATION_DIRECT,
    ),
    "infinix": CorporateProvenanceRecord(
        entity_name="Infinix",
        operating_company="Infinix Mobility Limited",
        parent_company="Shenzhen Transsion Holdings Co., Ltd.",
        relationship_type=RELATIONSHIP_SUBSIDIARY_HOLDING,
        evidence_source_title="Shenzhen Transsion Holdings Co., Ltd. (SSE: 688036) Annual Report 2019 — Multi-Brand Portfolio: Tecno, Itel, and Infinix",
        direct_source_url="http://www.transsion.com/en/investor/report",
        publication_date="2020-04-28",
        effective_date="2013-01-01",
        verification_status=VERIFICATION_DIRECT,
    ),
    "tecno": CorporateProvenanceRecord(
        entity_name="Tecno",
        operating_company="Tecno Mobile Limited",
        parent_company="Shenzhen Transsion Holdings Co., Ltd.",
        relationship_type=RELATIONSHIP_SUBSIDIARY_HOLDING,
        evidence_source_title="Shenzhen Transsion Holdings Co., Ltd. (SSE: 688036) Annual Report 2019 — Multi-Brand Portfolio: Tecno, Itel, and Infinix",
        direct_source_url="http://www.transsion.com/en/investor/report",
        publication_date="2020-04-28",
        effective_date="2006-08-01",
        verification_status=VERIFICATION_DIRECT,
    ),
    "itel": CorporateProvenanceRecord(
        entity_name="Itel",
        operating_company="Itel Mobile Limited",
        parent_company="Shenzhen Transsion Holdings Co., Ltd.",
        relationship_type=RELATIONSHIP_SUBSIDIARY_HOLDING,
        evidence_source_title="Shenzhen Transsion Holdings Co., Ltd. (SSE: 688036) Annual Report 2019 — Multi-Brand Portfolio: Tecno, Itel, and Infinix",
        direct_source_url="http://www.transsion.com/en/investor/report",
        publication_date="2020-04-28",
        effective_date="2007-01-01",
        verification_status=VERIFICATION_DIRECT,
    ),
    "xolo": CorporateProvenanceRecord(
        entity_name="XOLO",
        operating_company="Lava International Ltd.",
        parent_company=None,
        relationship_type=RELATIONSHIP_DIRECT_SUBBRAND,
        evidence_source_title="Lava International Limited Corporate History & Sub-Brand XOLO Product Architecture",
        direct_source_url="https://www.lavamobiles.com/about-us",
        publication_date="2012-04-19",
        effective_date="2012-04-19",
        verification_status=VERIFICATION_DISCLOSURE,
    ),
    "yu": CorporateProvenanceRecord(
        entity_name="Yu",
        operating_company="Yu Televentures Pvt. Ltd.",
        parent_company="Micromax Informatics Ltd.",
        relationship_type=RELATIONSHIP_SUBSIDIARY_SUBBRAND,
        evidence_source_title="Micromax Informatics Limited Corporate Filing & Launch of Wholly-Owned Subsidiary YU Televentures",
        direct_source_url="https://www.micromaxinfo.com/about-us",
        publication_date="2014-12-18",
        effective_date="2014-12-18",
        verification_status=VERIFICATION_DISCLOSURE,
    ),
    "nubia": CorporateProvenanceRecord(
        entity_name="Nubia",
        operating_company="Nubia Technology Co., Ltd.",
        parent_company="ZTE Corporation",
        relationship_type=RELATIONSHIP_SUBSIDIARY_SUBBRAND,
        evidence_source_title="ZTE Corporation (HKEX: 0763) Annual Report 2012 — Launch of High-End Smartphone Sub-Brand Nubia",
        direct_source_url="https://www.zte.com.cn/global/about/investor_relations",
        publication_date="2013-04-10",
        effective_date="2012-10-31",
        verification_status=VERIFICATION_DIRECT,
    ),
    "meizu": CorporateProvenanceRecord(
        entity_name="Meizu",
        operating_company="Meizu Technology Co., Ltd.",
        parent_company="Xingji Meizu Group",
        relationship_type=RELATIONSHIP_SUBSIDIARY_ACQUISITION,
        evidence_source_title="Xingji Dingsheng (Geely Group) Completes Acquisition of Meizu Technology — Corporate Merger Announcement",
        direct_source_url="https://www.meizu.com/en/about.html",
        publication_date="2022-07-04",
        effective_date="2022-07-04",
        verification_status=VERIFICATION_DISCLOSURE,
    ),
    "lyf": CorporateProvenanceRecord(
        entity_name="Lyf",
        operating_company="Reliance Retail Ltd.",
        parent_company="Reliance Industries Limited",
        relationship_type=RELATIONSHIP_SUBSIDIARY_HOLDING,
        evidence_source_title="Reliance Industries Limited Annual Report 2015-16 — Retail Segment: Launch of LYF 4G Smart Devices",
        direct_source_url="https://www.ril.com/investors/financial-reporting",
        publication_date="2016-04-22",
        effective_date="2015-10-01",
        verification_status=VERIFICATION_DIRECT,
    ),
    "reliance": CorporateProvenanceRecord(
        entity_name="Reliance",
        operating_company="Jio Platforms Limited",
        parent_company="Reliance Industries Limited",
        relationship_type=RELATIONSHIP_SUBSIDIARY_HOLDING,
        evidence_source_title="Reliance Industries Limited Annual Report 2021-22 — Digital Services (Jio Platforms Ltd) product initiative developed with Google (Pragati OS); retail distribution via Reliance Retail Ltd.",
        direct_source_url="https://www.ril.com/investors/financial-reporting",
        publication_date="2022-04-29",
        effective_date="2021-11-04",
        verification_status=VERIFICATION_DIRECT,
    ),
    "nextbit": CorporateProvenanceRecord(
        entity_name="Nextbit",
        operating_company="Nextbit Systems Inc.",
        parent_company="Razer Inc.",
        relationship_type=RELATIONSHIP_SUBSIDIARY_ACQUISITION,
        evidence_source_title="Razer Inc. Acquires Nextbit Systems Inc. — Official Press Announcement",
        direct_source_url="https://www.razer.com/press",
        publication_date="2017-01-28",
        effective_date="2017-01-27",
        verification_status=VERIFICATION_DISCLOSURE,
    ),
    "vivo": CorporateProvenanceRecord(
        entity_name="Vivo",
        operating_company="Vivo Mobile Communication Co., Ltd.",
        parent_company=None,
        relationship_type=RELATIONSHIP_INDEPENDENT_OEM,
        evidence_source_title="Vivo Mobile Communication Co., Ltd. Corporate Registration & Governance (Dongguan, China) — Autonomous Operating OEM",
        direct_source_url="https://www.vivo.com/en/about-vivo",
        publication_date="2009-01-01",
        effective_date="2009-01-01",
        verification_status=VERIFICATION_DISCLOSURE,
    ),
    "oppo": CorporateProvenanceRecord(
        entity_name="OPPO",
        operating_company="Guangdong Oppo Mobile Telecommunications Corp., Ltd.",
        parent_company=None,
        relationship_type=RELATIONSHIP_INDEPENDENT_OEM,
        evidence_source_title="Guangdong Oppo Mobile Telecommunications Corp., Ltd. Corporate Governance & History — Autonomous Operating OEM",
        direct_source_url="https://www.oppo.com/en/about-oppo/",
        publication_date="2004-10-10",
        effective_date="2004-10-10",
        verification_status=VERIFICATION_DISCLOSURE,
    ),
    "realme": CorporateProvenanceRecord(
        entity_name="Realme",
        operating_company="Realme Chongqing Mobile Telecommunications Corp., Ltd.",
        parent_company=None,
        relationship_type=RELATIONSHIP_INDEPENDENT_OEM,
        evidence_source_title="Realme Chongqing Mobile Telecommunications Corp., Ltd. Corporate Separation Statement by Sky Li (Founder & CEO)",
        direct_source_url="https://www.realme.com/global/brand",
        publication_date="2018-07-30",
        effective_date="2018-07-30",
        verification_status=VERIFICATION_DISCLOSURE,
    ),
}


def get_corporate_provenance(brand_key: str) -> Optional[CorporateProvenanceRecord]:
    """Retrieve audited corporate provenance record for a given brand name or key."""
    if not brand_key:
        return None
    return CORPORATE_PROVENANCE_REGISTRY.get(brand_key.strip().lower())


def parse_brand(model_name: Optional[str]) -> BrandResult:
    """Parse consumer-facing brand, operating company, and parent entity from model string.

    Guarantees:
    1. Autonomous sub-brands remain separate (POCO != Xiaomi, Redmi != Xiaomi, iQOO != Vivo, CMF != Nothing).
    2. operating_company reflects the verified legal entity manufacturing/commercializing the brand.
    3. parent_company is populated ONLY when a distinct verified corporate parent entity exists; otherwise None.
    4. operating_company != parent_company whenever both are populated (no same-entity assignment).
    5. parent_company_status explicitly distinguishes VERIFIED_PARENT, NO_PARENT, and UNKNOWN.
    6. relationship_type explicitly records DIRECT_SUBBRAND, SUBSIDIARY_SUBBRAND, INDEPENDENT_OEM, or TRADEMARK_LICENSE.
    7. Silicon processors (e.g. HiSilicon, Kirin, Snapdragon) are never identified as phone brands.
    8. Unresolved corporate parentage assigns parent_company=None, operating_company=None, and FLAG_UNKNOWN_PARENT_COMPANY.
    9. Missing or unparseable model names assign brand_name='Unknown' and FLAG_UNKNOWN_BRAND.
    """
    if model_name is None or not isinstance(model_name, str):
        return BrandResult(
            brand_name="Unknown",
            brand_resolution_status=RESOLUTION_UNKNOWN,
            operating_company=None,
            parent_company=None,
            parent_company_status=PARENT_STATUS_UNKNOWN,
            relationship_type=RELATIONSHIP_UNVERIFIED,
            brand_relationship_confidence=CONFIDENCE_UNKNOWN,
            catalog_tier=CATALOG_TIER_NICHE,
            raw_input="" if model_name is None else str(model_name),
            quality_flags=[FLAG_UNKNOWN_BRAND],
        )

    raw_clean = model_name.strip()
    if not raw_clean:
        return BrandResult(
            brand_name="Unknown",
            brand_resolution_status=RESOLUTION_UNKNOWN,
            operating_company=None,
            parent_company=None,
            parent_company_status=PARENT_STATUS_UNKNOWN,
            relationship_type=RELATIONSHIP_UNVERIFIED,
            brand_relationship_confidence=CONFIDENCE_UNKNOWN,
            catalog_tier=CATALOG_TIER_NICHE,
            raw_input=raw_clean,
            quality_flags=[FLAG_UNKNOWN_BRAND],
        )

    s_lower = raw_clean.lower()
    first_word = s_lower.split()[0]

    # Rule: Silicon processors must NEVER be identified as phone brands
    if first_word in SILICON_PROCESSOR_BLOCKLIST:
        return BrandResult(
            brand_name="Unknown",
            brand_resolution_status=RESOLUTION_UNKNOWN,
            operating_company=None,
            parent_company=None,
            parent_company_status=PARENT_STATUS_UNKNOWN,
            relationship_type=RELATIONSHIP_UNVERIFIED,
            brand_relationship_confidence=CONFIDENCE_UNKNOWN,
            catalog_tier=CATALOG_TIER_NICHE,
            raw_input=raw_clean,
            quality_flags=[FLAG_UNKNOWN_BRAND],
        )

    # 1. Multi-word and specialized prefix resolutions
    lookup_key: Optional[str] = None

    if s_lower.startswith("xiaomi redmi"):
        # Autonomous sub-brand Redmi
        lookup_key = "redmi"
    elif s_lower.startswith("i kall"):
        # Multi-word brand I Kall
        lookup_key = "i kall"
    elif s_lower.startswith("moto ") or s_lower == "moto" or s_lower.startswith("motorola"):
        # Moto / Motorola normalization
        lookup_key = "motorola"
    elif s_lower.startswith("iphone"):
        # iPhone is a product line of Apple, never an autonomous brand
        lookup_key = "apple"
    else:
        # Standard first-token lookup
        lookup_key = first_word

    if lookup_key in BRAND_METADATA_REGISTRY:
        canonical_name, operating_co, parent_co, parent_status, rel_type, conf, tier = BRAND_METADATA_REGISTRY[lookup_key]
        flags: List[str] = []
        if conf == CONFIDENCE_UNKNOWN:
            flags.append(FLAG_UNKNOWN_PARENT_COMPANY)

        curr_rel = ""
        if parent_co:
            curr_rel = f"{canonical_name} operated by {operating_co} under parent {parent_co}"
        elif operating_co:
            curr_rel = f"{canonical_name} operated by {operating_co}"
        else:
            curr_rel = f"{canonical_name} (unresolved operating entity)"

        if lookup_key in TRANSITIONAL_CORPORATE_BRANDS:
            hist_status = HISTORICAL_RELATIONSHIP_TRANSITION_UNTIMED
            temp_status = TEMPORAL_STATUS_LIMITATION_UNTIMED
        elif conf == CONFIDENCE_UNKNOWN:
            hist_status = HISTORICAL_RELATIONSHIP_UNKNOWN
            temp_status = TEMPORAL_STATUS_LIMITATION_UNTIMED
        else:
            hist_status = HISTORICAL_RELATIONSHIP_NOT_ASSESSED
            temp_status = TEMPORAL_STATUS_CONTEMPORARY_ONLY

        return BrandResult(
            brand_name=canonical_name,
            brand_resolution_status=RESOLUTION_RESOLVED,
            operating_company=operating_co,
            parent_company=parent_co,
            parent_company_status=parent_status,
            relationship_type=rel_type,
            brand_relationship_confidence=conf,
            catalog_tier=tier,
            raw_input=raw_clean,
            quality_flags=flags,
            current_corporate_relationship=curr_rel,
            historical_relationship_status=hist_status,
            temporal_verification_status=temp_status,
        )

    # Fallback for unrecognized brands
    return BrandResult(
        brand_name="Unknown",
        brand_resolution_status=RESOLUTION_UNKNOWN,
        operating_company=None,
        parent_company=None,
        parent_company_status=PARENT_STATUS_UNKNOWN,
        relationship_type=RELATIONSHIP_UNVERIFIED,
        brand_relationship_confidence=CONFIDENCE_UNKNOWN,
        catalog_tier=CATALOG_TIER_NICHE,
        raw_input=raw_clean,
        quality_flags=[FLAG_UNKNOWN_BRAND],
    )


__all__ = [
    "RESOLUTION_RESOLVED",
    "RESOLUTION_UNKNOWN",
    "VALID_RESOLUTION_STATUSES",
    "PARENT_STATUS_VERIFIED_PARENT",
    "PARENT_STATUS_NO_PARENT",
    "PARENT_STATUS_UNKNOWN",
    "VALID_PARENT_STATUSES",
    "CONFIDENCE_VERIFIED",
    "CONFIDENCE_LICENSED",
    "CONFIDENCE_INDEPENDENT",
    "CONFIDENCE_UNKNOWN",
    "VALID_CONFIDENCE_LEVELS",
    "RELATIONSHIP_INDEPENDENT_OEM",
    "RELATIONSHIP_DIRECT_SUBBRAND",
    "RELATIONSHIP_SUBSIDIARY_SUBBRAND",
    "RELATIONSHIP_SUBSIDIARY_ACQUISITION",
    "RELATIONSHIP_SUBSIDIARY_DIVESTMENT",
    "RELATIONSHIP_SUBSIDIARY_HOLDING",
    "RELATIONSHIP_TRADEMARK_LICENSE",
    "RELATIONSHIP_UNVERIFIED",
    "VALID_RELATIONSHIP_TYPES",
    "VERIFICATION_DIRECT",
    "VERIFICATION_DISCLOSURE",
    "VERIFICATION_UNVERIFIED",
    "VALID_VERIFICATION_STATUSES",
    "HISTORICAL_RELATIONSHIP_NOT_ASSESSED",
    "HISTORICAL_RELATIONSHIP_STATIC",
    "HISTORICAL_RELATIONSHIP_TRANSITION_UNTIMED",
    "HISTORICAL_RELATIONSHIP_UNKNOWN",
    "VALID_HISTORICAL_RELATIONSHIP_STATUSES",
    "TEMPORAL_STATUS_CONTEMPORARY_ONLY",
    "TEMPORAL_STATUS_LIMITATION_UNTIMED",
    "VALID_TEMPORAL_STATUSES",
    "TRANSITIONAL_CORPORATE_BRANDS",
    "CATALOG_TIER_MAJOR",
    "CATALOG_TIER_MID",
    "CATALOG_TIER_NICHE",
    "VALID_CATALOG_TIERS",
    "SILICON_PROCESSOR_BLOCKLIST",
    "BrandResult",
    "CorporateProvenanceRecord",
    "BRAND_METADATA_REGISTRY",
    "CORPORATE_PROVENANCE_REGISTRY",
    "get_corporate_provenance",
    "parse_brand",
]

