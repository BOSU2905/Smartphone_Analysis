"""Unit and Integration Tests for Brand Taxonomy and Ratings/Reviews Preservation

Project: 'What Are We Really Paying For When We Buy a Smartphone?'
Phase 03 — Stage 03: Brand Taxonomy & Metadata Preservation
"""

import hashlib
from pathlib import Path
import unittest

from scripts.pipeline.brand_taxonomy import (
    BRAND_METADATA_REGISTRY,
    CATALOG_TIER_MAJOR,
    CATALOG_TIER_MID,
    CATALOG_TIER_NICHE,
    CONFIDENCE_INDEPENDENT,
    CONFIDENCE_LICENSED,
    CONFIDENCE_UNKNOWN,
    CONFIDENCE_VERIFIED,
    CORPORATE_PROVENANCE_REGISTRY,
    PARENT_STATUS_NO_PARENT,
    PARENT_STATUS_UNKNOWN,
    PARENT_STATUS_VERIFIED_PARENT,
    RELATIONSHIP_DIRECT_SUBBRAND,
    RELATIONSHIP_INDEPENDENT_OEM,
    RELATIONSHIP_SUBSIDIARY_ACQUISITION,
    RELATIONSHIP_SUBSIDIARY_DIVESTMENT,
    RELATIONSHIP_SUBSIDIARY_HOLDING,
    RELATIONSHIP_SUBSIDIARY_SUBBRAND,
    RELATIONSHIP_TRADEMARK_LICENSE,
    RELATIONSHIP_UNVERIFIED,
    RESOLUTION_RESOLVED,
    RESOLUTION_UNKNOWN,
    VALID_CONFIDENCE_LEVELS,
    VALID_PARENT_STATUSES,
    VALID_RELATIONSHIP_TYPES,
    VALID_RESOLUTION_STATUSES,
    VALID_VERIFICATION_STATUSES,
    VERIFICATION_DIRECT,
    VERIFICATION_DISCLOSURE,
    VERIFICATION_UNVERIFIED,
    HISTORICAL_RELATIONSHIP_NOT_ASSESSED,
    HISTORICAL_RELATIONSHIP_STATIC,
    HISTORICAL_RELATIONSHIP_TRANSITION_UNTIMED,
    HISTORICAL_RELATIONSHIP_UNKNOWN,
    VALID_HISTORICAL_RELATIONSHIP_STATUSES,
    TEMPORAL_STATUS_CONTEMPORARY_ONLY,
    TEMPORAL_STATUS_LIMITATION_UNTIMED,
    VALID_TEMPORAL_STATUSES,
    TRANSITIONAL_CORPORATE_BRANDS,
    BrandResult,
    CorporateProvenanceRecord,
    get_corporate_provenance,
    parse_brand,
)
from scripts.pipeline.config import (
    FLAG_INVALID_EXPERT_RATING,
    FLAG_INVALID_USER_RATING,
    FLAG_MISSING_EXPERT_RATING,
    FLAG_MISSING_REVIEW_SNIPPET,
    FLAG_MISSING_REVIEW_URL,
    FLAG_MISSING_USER_RATING,
    FLAG_REVIEW_SNIPPET_WITHOUT_URL,
    FLAG_REVIEW_URL_WITHOUT_SNIPPET,
    FLAG_UNKNOWN_BRAND,
    FLAG_UNKNOWN_PARENT_COMPANY,
    FLAG_UNPARSEABLE_FORMAT,
    FLAG_UNPARSEABLE_USER_RATING,
    RAW_DATA_PATH,
    RAW_FILE_EXPECTED_BYTES,
    RAW_FILE_EXPECTED_SHA256,
)
from scripts.pipeline.ingestion import load_raw_dataset
from scripts.pipeline.ratings import (
    RatingsMetadata,
    ReviewResult,
    UserRatingResult,
    parse_all_ratings_and_reviews,
    parse_expert_rating,
    parse_review,
    parse_user_rating,
)


class TestBrandTaxonomy(unittest.TestCase):
    """Test suite verifying brand autonomy, corporate parentage, and catalog tiers."""

    def test_autonomous_subbrand_separation_xiaomi_redmi_poco(self) -> None:
        """Verify POCO, Redmi, and Xiaomi remain distinct consumer-facing brands with verified operating and parent entities."""
        poco = parse_brand("POCO X6 Pro 5G 256GB")
        redmi = parse_brand("Xiaomi Redmi Note 13 Pro Plus 5G")
        xiaomi = parse_brand("Xiaomi 14 Ultra")

        # Autonomous brand names
        self.assertEqual(poco.brand_name, "POCO")
        self.assertEqual(redmi.brand_name, "Redmi")
        self.assertEqual(xiaomi.brand_name, "Xiaomi")

        # Distinct brands
        self.assertNotEqual(poco.brand_name, xiaomi.brand_name)
        self.assertNotEqual(redmi.brand_name, xiaomi.brand_name)
        self.assertNotEqual(poco.brand_name, redmi.brand_name)

        # Operating company commercializing the hardware
        self.assertEqual(poco.operating_company, "Xiaomi Communications Co., Ltd.")
        self.assertEqual(redmi.operating_company, "Xiaomi Communications Co., Ltd.")
        self.assertEqual(xiaomi.operating_company, "Xiaomi Communications Co., Ltd.")

        # Corporate parent holding entity
        self.assertEqual(poco.parent_company, "Xiaomi Corporation")
        self.assertEqual(redmi.parent_company, "Xiaomi Corporation")
        self.assertIsNone(xiaomi.parent_company)  # Top-level operating OEM

        # Relationship confidence
        self.assertEqual(poco.relationship_confidence, CONFIDENCE_VERIFIED)
        self.assertEqual(redmi.relationship_confidence, CONFIDENCE_VERIFIED)
        self.assertEqual(xiaomi.relationship_confidence, CONFIDENCE_INDEPENDENT)

    def test_autonomous_subbrand_separation_bbk_entities(self) -> None:
        """Verify Vivo, iQOO, OPPO, OnePlus, and Realme operating and parent company attribution."""
        vivo = parse_brand("vivo X100 Pro")
        iqoo = parse_brand("iQOO 12 5G")
        oppo = parse_brand("OPPO Find X7 Ultra")
        oneplus = parse_brand("OnePlus 12 256GB")
        realme = parse_brand("realme GT 6")

        self.assertEqual(vivo.brand_name, "Vivo")
        self.assertEqual(iqoo.brand_name, "iQOO")
        self.assertEqual(oppo.brand_name, "OPPO")
        self.assertEqual(oneplus.brand_name, "OnePlus")
        self.assertEqual(realme.brand_name, "Realme")

        # Assert all brand names are distinct
        brand_names = {vivo.brand_name, iqoo.brand_name, oppo.brand_name, oneplus.brand_name, realme.brand_name}
        self.assertEqual(len(brand_names), 5)

        # Autonomous operating companies
        self.assertEqual(vivo.operating_company, "Vivo Mobile Communication Co., Ltd.")
        self.assertIsNone(vivo.parent_company)
        self.assertEqual(vivo.relationship_confidence, CONFIDENCE_INDEPENDENT)

        self.assertEqual(oppo.operating_company, "Guangdong Oppo Mobile Telecommunications Corp., Ltd.")
        self.assertIsNone(oppo.parent_company)
        self.assertEqual(oppo.relationship_confidence, CONFIDENCE_INDEPENDENT)

        self.assertEqual(realme.operating_company, "Realme Chongqing Mobile Telecommunications Corp., Ltd.")
        self.assertIsNone(realme.parent_company)
        self.assertEqual(realme.relationship_confidence, CONFIDENCE_INDEPENDENT)

        # Verified subsidiaries
        self.assertEqual(oneplus.operating_company, "OnePlus Technology (Shenzhen) Co., Ltd.")
        self.assertEqual(oneplus.parent_company, "Guangdong Oppo Mobile Telecommunications Corp., Ltd.")
        self.assertEqual(oneplus.relationship_confidence, CONFIDENCE_VERIFIED)

        self.assertEqual(iqoo.operating_company, "Vivo Mobile Communication Co., Ltd.")
        self.assertIsNone(iqoo.parent_company)
        self.assertEqual(iqoo.parent_company_status, PARENT_STATUS_NO_PARENT)
        self.assertEqual(iqoo.relationship_type, RELATIONSHIP_DIRECT_SUBBRAND)
        self.assertEqual(iqoo.relationship_confidence, CONFIDENCE_VERIFIED)

    def test_autonomous_subbrand_separation_nothing_cmf(self) -> None:
        """Verify CMF is preserved as distinct from Nothing while operating directly under Nothing Technology."""
        nothing = parse_brand("Nothing Phone 2")
        cmf = parse_brand("CMF Phone 1 5G")

        self.assertEqual(nothing.brand_name, "Nothing")
        self.assertEqual(cmf.brand_name, "CMF")
        self.assertNotEqual(nothing.brand_name, cmf.brand_name)

        self.assertEqual(nothing.operating_company, "Nothing Technology Limited")
        self.assertIsNone(nothing.parent_company)
        self.assertEqual(nothing.relationship_confidence, CONFIDENCE_INDEPENDENT)

        self.assertEqual(cmf.operating_company, "Nothing Technology Limited")
        self.assertIsNone(cmf.parent_company)
        self.assertEqual(cmf.parent_company_status, PARENT_STATUS_NO_PARENT)
        self.assertEqual(cmf.relationship_type, RELATIONSHIP_DIRECT_SUBBRAND)
        self.assertEqual(cmf.relationship_confidence, CONFIDENCE_VERIFIED)

    def test_apple_identity_never_mapped_to_iphone(self) -> None:
        """Verify Apple devices resolve to brand Apple, never iPhone, with independent corporate structure."""
        apple1 = parse_brand("Apple iPhone 15 Pro Max 256GB")
        apple2 = parse_brand("iPhone 14 128GB")

        self.assertEqual(apple1.brand_name, "Apple")
        self.assertEqual(apple2.brand_name, "Apple")
        self.assertNotEqual(apple1.brand_name.lower(), "iphone")
        self.assertEqual(apple1.operating_company, "Apple Inc.")
        self.assertIsNone(apple1.parent_company)
        self.assertEqual(apple1.relationship_confidence, CONFIDENCE_INDEPENDENT)

    def test_motorola_prefix_normalization(self) -> None:
        """Verify both 'Moto' and 'Motorola' map to brand Motorola under Lenovo Group."""
        moto1 = parse_brand("Moto G84 5G")
        moto2 = parse_brand("Motorola Edge 50 Pro")

        self.assertEqual(moto1.brand_name, "Motorola")
        self.assertEqual(moto2.brand_name, "Motorola")
        self.assertEqual(moto1.operating_company, "Motorola Mobility LLC")
        self.assertEqual(moto2.operating_company, "Motorola Mobility LLC")
        self.assertEqual(moto1.parent_company, "Lenovo Group Limited")
        self.assertEqual(moto2.parent_company, "Lenovo Group Limited")
        self.assertEqual(moto1.relationship_confidence, CONFIDENCE_VERIFIED)

    def test_corporate_attribution_licensing_confidence(self) -> None:
        """Verify licensed brand relationships (Nokia, CAT, Alcatel, InFocus)."""
        nokia = parse_brand("Nokia G42 5G")
        cat = parse_brand("CAT S62 Pro")
        alcatel = parse_brand("Alcatel 1S")
        infocus = parse_brand("InFocus Turbo 5")

        self.assertEqual(nokia.relationship_confidence, CONFIDENCE_LICENSED)
        self.assertEqual(nokia.operating_company, "HMD Global Oy")
        self.assertIsNone(nokia.parent_company)

        self.assertEqual(cat.relationship_confidence, CONFIDENCE_LICENSED)
        self.assertEqual(cat.operating_company, "Bullitt Mobile Ltd")
        self.assertEqual(cat.parent_company, "Bullitt Group Limited")
        self.assertEqual(cat.parent_company_status, PARENT_STATUS_VERIFIED_PARENT)
        self.assertEqual(cat.relationship_type, RELATIONSHIP_TRADEMARK_LICENSE)

        self.assertEqual(alcatel.relationship_confidence, CONFIDENCE_LICENSED)
        self.assertEqual(alcatel.operating_company, "TCL Communication Technology Holdings Ltd.")
        self.assertEqual(alcatel.parent_company, "TCL Technology Group Corporation")

        self.assertEqual(infocus.relationship_confidence, CONFIDENCE_LICENSED)
        self.assertEqual(infocus.operating_company, "FIH Mobile Ltd")
        self.assertEqual(infocus.parent_company, "Hon Hai Precision Industry Co., Ltd. (Foxconn)")

    def test_corporate_attribution_independent_confidence(self) -> None:
        """Verify independent OEMs operating primarily under their own brand."""
        sony = parse_brand("Sony Xperia 1 V")
        asus = parse_brand("Asus ROG Phone 8")
        micromax = parse_brand("Micromax In 1b")
        lg = parse_brand("LG Wing 5G")

        for res in (sony, asus, micromax, lg):
            self.assertEqual(res.relationship_confidence, CONFIDENCE_INDEPENDENT)
            self.assertIsNotNone(res.operating_company)
            self.assertIsNone(res.parent_company)

    def test_unknown_corporate_parent_confidence(self) -> None:
        """Verify obscure/unresolved brands receive UNKNOWN confidence and flag."""
        mobiistar = parse_brand("Mobiistar X1 Dual")
        zen = parse_brand("Zen Cinemax 2+")

        self.assertEqual(mobiistar.relationship_confidence, CONFIDENCE_UNKNOWN)
        self.assertIsNone(mobiistar.operating_company)
        self.assertIsNone(mobiistar.parent_company)
        self.assertIn(FLAG_UNKNOWN_PARENT_COMPANY, mobiistar.quality_flags)

        self.assertEqual(zen.relationship_confidence, CONFIDENCE_UNKNOWN)
        self.assertIsNone(zen.operating_company)
        self.assertIsNone(zen.parent_company)
        self.assertIn(FLAG_UNKNOWN_PARENT_COMPANY, zen.quality_flags)

    def test_hisilicon_silicon_separation(self) -> None:
        """Verify silicon processor names are never misidentified as smartphone brands."""
        hisilicon = parse_brand("HiSilicon Kirin 9000")
        snapdragon = parse_brand("Snapdragon 8 Gen 3 Phone")

        self.assertEqual(hisilicon.brand_name, "Unknown")
        self.assertIn(FLAG_UNKNOWN_BRAND, hisilicon.quality_flags)

        self.assertEqual(snapdragon.brand_name, "Unknown")
        self.assertIn(FLAG_UNKNOWN_BRAND, snapdragon.quality_flags)

    def test_catalog_tier_assignment(self) -> None:
        """Verify catalog tier mapping based on empirical volume in dataset."""
        samsung = parse_brand("Samsung Galaxy S24 Ultra")
        google = parse_brand("Google Pixel 8 Pro")
        cmf = parse_brand("CMF Phone 1")

        self.assertEqual(samsung.catalog_tier, CATALOG_TIER_MAJOR)
        self.assertEqual(google.catalog_tier, CATALOG_TIER_MID)
        self.assertEqual(cmf.catalog_tier, CATALOG_TIER_NICHE)

    def test_brand_resolution_status_separation(self) -> None:
        """Verify explicit separation between brand resolution status and corporate parentage."""
        # 1. Resolved brand with verified operating company and independent corporate structure
        samsung = parse_brand("Samsung Galaxy S24")
        self.assertEqual(samsung.brand_name, "Samsung")
        self.assertEqual(samsung.brand_resolution_status, RESOLUTION_RESOLVED)
        self.assertEqual(samsung.operating_company, "Samsung Electronics Co., Ltd.")
        self.assertIsNone(samsung.parent_company)
        self.assertEqual(samsung.brand_relationship_confidence, CONFIDENCE_INDEPENDENT)

        # 1B. Resolved brand with verified operating company and verified parent holding entity
        poco = parse_brand("POCO F5")
        self.assertEqual(poco.brand_name, "POCO")
        self.assertEqual(poco.brand_resolution_status, RESOLUTION_RESOLVED)
        self.assertEqual(poco.operating_company, "Xiaomi Communications Co., Ltd.")
        self.assertEqual(poco.parent_company, "Xiaomi Corporation")
        self.assertEqual(poco.brand_relationship_confidence, CONFIDENCE_VERIFIED)

        # 2. Resolved brand with UNKNOWN corporate parent
        mobiistar = parse_brand("Mobiistar CQ")
        self.assertEqual(mobiistar.brand_name, "Mobiistar")
        self.assertEqual(mobiistar.brand_resolution_status, RESOLUTION_RESOLVED)
        self.assertIsNone(mobiistar.operating_company)
        self.assertIsNone(mobiistar.parent_company)
        self.assertEqual(mobiistar.brand_relationship_confidence, CONFIDENCE_UNKNOWN)
        self.assertIn(FLAG_UNKNOWN_PARENT_COMPANY, mobiistar.quality_flags)

        # 3. Unresolved brand (empty / unknown / silicon)
        unresolved = parse_brand("HiSilicon Kirin 990")
        self.assertEqual(unresolved.brand_name, "Unknown")
        self.assertEqual(unresolved.brand_resolution_status, RESOLUTION_UNKNOWN)
        self.assertIsNone(unresolved.operating_company)
        self.assertIsNone(unresolved.parent_company)
        self.assertEqual(unresolved.brand_relationship_confidence, CONFIDENCE_UNKNOWN)
        self.assertIn(FLAG_UNKNOWN_BRAND, unresolved.quality_flags)

    def test_corporate_provenance_registry(self) -> None:
        """Verify audited legal evidence and provenance metadata for corporate relationships."""
        oneplus_prov = get_corporate_provenance("oneplus")
        self.assertIsNotNone(oneplus_prov)
        self.assertEqual(oneplus_prov.parent_company, "Guangdong Oppo Mobile Telecommunications Corp., Ltd.")
        self.assertIn("A New Journey for OnePlus", oneplus_prov.evidence_source_title)
        self.assertEqual(oneplus_prov.verification_status, VERIFICATION_DISCLOSURE)

        nokia_prov = get_corporate_provenance("nokia")
        self.assertIsNotNone(nokia_prov)
        self.assertEqual(nokia_prov.operating_company, "HMD Global Oy")
        self.assertIsNone(nokia_prov.parent_company)
        self.assertEqual(nokia_prov.relationship_type, "TRADEMARK_LICENSE")
        self.assertEqual(nokia_prov.verification_status, VERIFICATION_DISCLOSURE)

        xolo_prov = get_corporate_provenance("xolo")
        self.assertIsNotNone(xolo_prov)
        self.assertEqual(xolo_prov.operating_company, "Lava International Ltd.")
        self.assertIsNone(xolo_prov.parent_company)
        self.assertEqual(xolo_prov.verification_status, VERIFICATION_DISCLOSURE)

        moto_prov = get_corporate_provenance("motorola")
        self.assertIsNotNone(moto_prov)
        self.assertEqual(moto_prov.parent_company, "Lenovo Group Limited")
        self.assertEqual(moto_prov.verification_status, VERIFICATION_DISCLOSURE)

        honor_prov = get_corporate_provenance("honor")
        self.assertIsNotNone(honor_prov)
        self.assertEqual(honor_prov.parent_company, "Shenzhen Zhixin New Information Technology Co., Ltd.")
        self.assertEqual(honor_prov.verification_status, VERIFICATION_DISCLOSURE)

        redmi_prov = get_corporate_provenance("redmi")
        self.assertIsNotNone(redmi_prov)
        self.assertEqual(redmi_prov.parent_company, "Xiaomi Corporation")
        self.assertEqual(redmi_prov.verification_status, VERIFICATION_DIRECT)

        google_prov = get_corporate_provenance("google")
        self.assertIsNotNone(google_prov)
        self.assertEqual(google_prov.parent_company, "Alphabet Inc.")
        self.assertEqual(google_prov.verification_status, VERIFICATION_DIRECT)

        lenovo_prov = get_corporate_provenance("lenovo")
        self.assertIsNotNone(lenovo_prov)
        self.assertEqual(lenovo_prov.operating_company, "Lenovo Mobile Communication Technology Ltd.")
        self.assertEqual(lenovo_prov.parent_company, "Lenovo Group Limited")
        self.assertEqual(lenovo_prov.verification_status, VERIFICATION_DIRECT)

        reliance_prov = get_corporate_provenance("reliance")
        self.assertIsNotNone(reliance_prov)
        self.assertEqual(reliance_prov.operating_company, "Jio Platforms Limited")
        self.assertEqual(reliance_prov.parent_company, "Reliance Industries Limited")
        self.assertEqual(reliance_prov.verification_status, VERIFICATION_DIRECT)

        # All provenance records must have valid verification statuses
        for key, rec in CORPORATE_PROVENANCE_REGISTRY.items():
            self.assertIn(
                rec.verification_status,
                VALID_VERIFICATION_STATUSES,
                f"Provenance record for '{key}' has invalid verification status: {rec.verification_status}"
            )

    def test_provenance_verification_classification_standards(self) -> None:
        """Verify all 26 provenance records strictly follow DIRECTLY_VERIFIED vs OFFICIAL_CORPORATE_DISCLOSURE rules."""
        expected_direct = {
            "redmi", "poco", "google", "cat", "alcatel", "infocus",
            "infinix", "tecno", "itel", "nubia", "lyf", "lenovo", "reliance"
        }
        expected_disclosure = {
            "oneplus", "iqoo", "cmf", "motorola", "honor", "nokia",
            "xolo", "yu", "meizu", "nextbit", "vivo", "oppo", "realme"
        }

        self.assertEqual(len(CORPORATE_PROVENANCE_REGISTRY), 26)
        for key, rec in CORPORATE_PROVENANCE_REGISTRY.items():
            if key in expected_direct:
                self.assertEqual(
                    rec.verification_status,
                    VERIFICATION_DIRECT,
                    f"Statutory/Audited record '{key}' must be DIRECTLY_VERIFIED, got {rec.verification_status}"
                )
            elif key in expected_disclosure:
                self.assertEqual(
                    rec.verification_status,
                    VERIFICATION_DISCLOSURE,
                    f"Executive/Press/Web disclosure record '{key}' must be OFFICIAL_CORPORATE_DISCLOSURE, got {rec.verification_status}"
                )
            else:
                self.fail(f"Unexpected provenance record key: '{key}'")

    def test_lenovo_motorola_reliance_operating_identity_separation(self) -> None:
        """Verify holding companies (Lenovo Group, Reliance Industries) are never assigned as operating entities."""
        lenovo = parse_brand("Lenovo K10 Note")
        motorola = parse_brand("Motorola Edge 50 Pro")
        reliance = parse_brand("Reliance JioPhone Next")
        lyf = parse_brand("Lyf Water 8")

        # Lenovo operating company is its mobile operating subsidiary, parent is holding company
        self.assertEqual(lenovo.operating_company, "Lenovo Mobile Communication Technology Ltd.")
        self.assertEqual(lenovo.parent_company, "Lenovo Group Limited")
        self.assertEqual(lenovo.parent_company_status, PARENT_STATUS_VERIFIED_PARENT)
        self.assertEqual(lenovo.relationship_type, RELATIONSHIP_SUBSIDIARY_HOLDING)

        # Motorola operating company is Motorola Mobility LLC, parent is Lenovo Group Limited
        self.assertEqual(motorola.operating_company, "Motorola Mobility LLC")
        self.assertEqual(motorola.parent_company, "Lenovo Group Limited")
        self.assertEqual(motorola.parent_company_status, PARENT_STATUS_VERIFIED_PARENT)
        self.assertEqual(motorola.relationship_type, RELATIONSHIP_SUBSIDIARY_ACQUISITION)

        # Lenovo Group Limited is never an operating company
        self.assertNotEqual(lenovo.operating_company, "Lenovo Group Limited")
        self.assertNotEqual(motorola.operating_company, "Lenovo Group Limited")

        # Reliance operating company is Jio Platforms Limited (Digital Services), parent is Reliance Industries Limited
        self.assertEqual(reliance.operating_company, "Jio Platforms Limited")
        self.assertEqual(reliance.parent_company, "Reliance Industries Limited")
        self.assertEqual(reliance.parent_company_status, PARENT_STATUS_VERIFIED_PARENT)
        self.assertEqual(reliance.relationship_type, RELATIONSHIP_SUBSIDIARY_HOLDING)

        # Lyf operating company is Reliance Retail Ltd., parent is Reliance Industries Limited
        self.assertEqual(lyf.operating_company, "Reliance Retail Ltd.")
        self.assertEqual(lyf.parent_company, "Reliance Industries Limited")
        self.assertEqual(lyf.parent_company_status, PARENT_STATUS_VERIFIED_PARENT)
        self.assertEqual(lyf.relationship_type, RELATIONSHIP_SUBSIDIARY_HOLDING)

        # Reliance Industries Limited is never an operating company
        self.assertNotEqual(reliance.operating_company, "Reliance Industries Limited")
        self.assertNotEqual(lyf.operating_company, "Reliance Industries Limited")

    def test_operating_company_differs_from_parent_company(self) -> None:
        """Verify operating_company != parent_company whenever both are populated across all brands."""
        for brand_key, (name, op_co, parent_co, parent_status, rel_type, conf, tier) in BRAND_METADATA_REGISTRY.items():
            if op_co is not None and parent_co is not None:
                self.assertNotEqual(
                    op_co, parent_co,
                    f"Same-entity attribution error for brand '{name}': operating_company and parent_company are both '{op_co}'"
                )

    def test_parent_company_status_consistency(self) -> None:
        """Verify parent_company_status aligns consistently with operating_company and parent_company."""
        for brand_key, (name, op_co, parent_co, parent_status, rel_type, conf, tier) in BRAND_METADATA_REGISTRY.items():
            if parent_status == PARENT_STATUS_VERIFIED_PARENT:
                self.assertIsNotNone(parent_co, f"Brand '{name}' has VERIFIED_PARENT but parent_company is None")
                self.assertIsNotNone(op_co, f"Brand '{name}' has VERIFIED_PARENT but operating_company is None")
                self.assertNotEqual(op_co, parent_co, f"Brand '{name}' has identical operating and parent companies")
            elif parent_status == PARENT_STATUS_NO_PARENT:
                self.assertIsNone(parent_co, f"Brand '{name}' has NO_PARENT but parent_company is '{parent_co}'")
                self.assertIsNotNone(op_co, f"Brand '{name}' has NO_PARENT but operating_company is None")
            elif parent_status == PARENT_STATUS_UNKNOWN:
                self.assertIsNone(parent_co, f"Brand '{name}' has UNKNOWN status but parent_company is populated")
                self.assertIsNone(op_co, f"Brand '{name}' has UNKNOWN status but operating_company is populated")

    def test_unknown_vs_no_parent_distinction(self) -> None:
        """Verify that parent_company is None does not automatically imply NO_PARENT."""
        apple = parse_brand("Apple iPhone 15")
        mobiistar = parse_brand("Mobiistar CQ")

        # Both have parent_company == None
        self.assertIsNone(apple.parent_company)
        self.assertIsNone(mobiistar.parent_company)

        # But parent_company_status is distinctly different!
        self.assertEqual(apple.parent_company_status, PARENT_STATUS_NO_PARENT)
        self.assertEqual(mobiistar.parent_company_status, PARENT_STATUS_UNKNOWN)
        self.assertNotEqual(apple.parent_company_status, mobiistar.parent_company_status)

    def test_iqoo_cmf_xolo_direct_subbrand_handling(self) -> None:
        """Verify iQOO, CMF, and XOLO are treated as direct sub-brands without same-entity parent assignment."""
        iqoo = parse_brand("iQOO Z9x")
        cmf = parse_brand("CMF Phone 1")
        xolo = parse_brand("XOLO Black 1X")

        for res, exp_op in ((iqoo, "Vivo Mobile Communication Co., Ltd."),
                            (cmf, "Nothing Technology Limited"),
                            (xolo, "Lava International Ltd.")):
            self.assertEqual(res.operating_company, exp_op)
            self.assertIsNone(res.parent_company, f"Sub-brand '{res.brand_name}' should have parent_company=None")
            self.assertEqual(res.parent_company_status, PARENT_STATUS_NO_PARENT)
            self.assertEqual(res.relationship_type, RELATIONSHIP_DIRECT_SUBBRAND)
            self.assertEqual(res.brand_relationship_confidence, CONFIDENCE_VERIFIED)
            self.assertNotEqual(res.operating_company, res.parent_company)


class TestRatingsAndReviews(unittest.TestCase):
    """Test suite verifying expert ratings, composite user ratings, and review preservation."""

    def test_expert_rating_parsing(self) -> None:
        """Verify expert rating float parsing, scaling, and null handling."""
        score, flags = parse_expert_rating(8.2)
        self.assertEqual(score, 8.2)
        self.assertEqual(flags, [])

        score_str, flags = parse_expert_rating("7.8")
        self.assertEqual(score_str, 7.8)
        self.assertEqual(flags, [])

        # Missing values
        score_none, flags_none = parse_expert_rating(None)
        self.assertIsNone(score_none)
        self.assertIn(FLAG_MISSING_EXPERT_RATING, flags_none)

        score_nan, flags_nan = parse_expert_rating(float("nan"))
        self.assertIsNone(score_nan)
        self.assertIn(FLAG_MISSING_EXPERT_RATING, flags_nan)

        # Out of bounds
        score_oob, flags_oob = parse_expert_rating(12.5)
        self.assertIsNone(score_oob)
        self.assertIn(FLAG_INVALID_EXPERT_RATING, flags_oob)

    def test_user_rating_parsing_kilo(self) -> None:
        """Verify user rating strings with 'K' suffix are multiplied by 1,000."""
        res = parse_user_rating("4.3 ★\r\n25.3K Ratings")
        self.assertEqual(res.score, 4.3)
        self.assertEqual(res.count, 25300)
        self.assertEqual(res.quality_flags, [])

    def test_user_rating_parsing_lakh(self) -> None:
        """Verify user rating strings with 'L' suffix are multiplied by 100,000 (Indian Lakh system)."""
        res = parse_user_rating("4.2 ★\r\n1.1L Ratings")
        self.assertEqual(res.score, 4.2)
        self.assertEqual(res.count, 110000)
        self.assertEqual(res.quality_flags, [])

    def test_user_rating_parsing_integer_with_commas(self) -> None:
        """Verify user rating strings with standard comma-separated integers."""
        res = parse_user_rating("4.6 ★\r\n1,921 Ratings")
        self.assertEqual(res.score, 4.6)
        self.assertEqual(res.count, 1921)
        self.assertEqual(res.quality_flags, [])

    def test_user_rating_missing_and_malformed(self) -> None:
        """Verify missing and unparseable user rating strings."""
        res_none = parse_user_rating(None)
        self.assertIsNone(res_none.score)
        self.assertIsNone(res_none.count)
        self.assertIn(FLAG_MISSING_USER_RATING, res_none.quality_flags)

        res_malformed = parse_user_rating("Customer review: highly recommended")
        self.assertIsNone(res_malformed.score)
        self.assertIsNone(res_malformed.count)
        self.assertIn(FLAG_UNPARSEABLE_USER_RATING, res_malformed.quality_flags)

    def test_review_snippet_and_url_exact_preservation(self) -> None:
        """Verify verbatim preservation of review excerpt and source URL."""
        snippet = "The Vivo V40 Pro shines with its cameras, performance, battery, display, and design."
        url = "https://www.mysmartprice.com/gear/mobiles/mobiles-reviews/vivo-v40-pro-review/"

        res = parse_review(snippet, url)
        self.assertEqual(res.snippet, snippet)
        self.assertEqual(res.url, url)
        self.assertEqual(res.quality_flags, [])

    def test_review_missing_handling(self) -> None:
        """Verify appropriate quality flags when review or URL is missing."""
        res = parse_review(None, None)
        self.assertIsNone(res.snippet)
        self.assertIsNone(res.url)
        self.assertIn(FLAG_MISSING_REVIEW_SNIPPET, res.quality_flags)
        self.assertIn(FLAG_MISSING_REVIEW_URL, res.quality_flags)
        self.assertNotIn(FLAG_REVIEW_SNIPPET_WITHOUT_URL, res.quality_flags)
        self.assertNotIn(FLAG_REVIEW_URL_WITHOUT_SNIPPET, res.quality_flags)

    def test_asymmetric_review_and_url_flags(self) -> None:
        """Verify asymmetric pairing flags for review snippet and URL."""
        # Snippet present, URL missing
        res_snippet_only = parse_review("Great camera review.", None)
        self.assertEqual(res_snippet_only.snippet, "Great camera review.")
        self.assertIsNone(res_snippet_only.url)
        self.assertIn(FLAG_MISSING_REVIEW_URL, res_snippet_only.quality_flags)
        self.assertIn(FLAG_REVIEW_SNIPPET_WITHOUT_URL, res_snippet_only.quality_flags)
        self.assertNotIn(FLAG_MISSING_REVIEW_SNIPPET, res_snippet_only.quality_flags)

        # URL present, snippet missing
        res_url_only = parse_review(None, "https://www.mysmartprice.com/review")
        self.assertIsNone(res_url_only.snippet)
        self.assertEqual(res_url_only.url, "https://www.mysmartprice.com/review")
        self.assertIn(FLAG_MISSING_REVIEW_SNIPPET, res_url_only.quality_flags)
        self.assertIn(FLAG_REVIEW_URL_WITHOUT_SNIPPET, res_url_only.quality_flags)
        self.assertNotIn(FLAG_MISSING_REVIEW_URL, res_url_only.quality_flags)

    def test_invalid_expert_and_user_rating_flags(self) -> None:
        """Verify distinct quality flags for invalid ratings vs missing ratings."""
        # Negative expert rating
        _, neg_flags = parse_expert_rating(-2.0)
        self.assertIn(FLAG_INVALID_EXPERT_RATING, neg_flags)
        self.assertNotIn(FLAG_MISSING_EXPERT_RATING, neg_flags)

        # Text expert rating
        _, text_flags = parse_expert_rating("Excellent")
        self.assertIn(FLAG_INVALID_EXPERT_RATING, text_flags)
        self.assertNotIn(FLAG_MISSING_EXPERT_RATING, text_flags)

        # Malformed user rating
        res_malformed = parse_user_rating("Rated 5 stars by John")
        self.assertIn(FLAG_INVALID_USER_RATING, res_malformed.quality_flags)
        self.assertNotIn(FLAG_MISSING_USER_RATING, res_malformed.quality_flags)

    def test_parse_all_ratings_and_reviews_coordination(self) -> None:
        """Verify full coordination across expert, user, and editorial review fields."""
        row = {
            "expert_rating": 8.1,
            "user_rating": "4.5 ★\r\n12.4K Ratings",
            "review": "Solid mid-range contender.",
            "review_link": "https://www.mysmartprice.com/sample-review",
        }
        res = parse_all_ratings_and_reviews(row)
        self.assertEqual(res.expert_rating, 8.1)
        self.assertEqual(res.user_rating.score, 4.5)
        self.assertEqual(res.user_rating.count, 12400)
        self.assertEqual(res.review.snippet, "Solid mid-range contender.")
        self.assertEqual(res.review.url, "https://www.mysmartprice.com/sample-review")
        self.assertEqual(res.all_quality_flags, [])


class TestDatasetWideIntegration(unittest.TestCase):
    """Integration test auditing all 2,928 rows of smartphones_uncleaned.csv."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.ingestion_res = load_raw_dataset(RAW_DATA_PATH)
        cls.df = cls.ingestion_res.raw_dataframe

    def test_all_rows_resolve_to_known_brands(self) -> None:
        """Verify that 100% of rows resolve to a valid known brand (0 Unknowns)."""
        unknowns = []
        for idx, row in self.df.iterrows():
            brand_res = parse_brand(row["model_name"])
            if brand_res.brand_name == "Unknown":
                unknowns.append((idx, row["model_name"]))

        self.assertEqual(len(unknowns), 0, f"Found {len(unknowns)} unknown brands: {unknowns[:5]}")

    def test_brand_counts_and_autonomy_across_dataset(self) -> None:
        """Verify exact brand counts for autonomous sub-brands and major OEMs."""
        brand_counts = {}
        for _, row in self.df.iterrows():
            brand_res = parse_brand(row["model_name"])
            brand_counts[brand_res.brand_name] = brand_counts.get(brand_res.brand_name, 0) + 1

        self.assertEqual(brand_counts.get("Redmi"), 207)
        self.assertEqual(brand_counts.get("Xiaomi"), 55)
        self.assertEqual(brand_counts.get("POCO"), 95)
        self.assertEqual(brand_counts.get("Apple"), 112)
        self.assertEqual(brand_counts.get("Motorola"), 119)
        self.assertEqual(brand_counts.get("iQOO"), 71)
        self.assertEqual(brand_counts.get("CMF"), 4)
        self.assertEqual(brand_counts.get("Nothing"), 9)
        self.assertEqual(brand_counts.get("Samsung"), 412)

    def test_ratings_and_reviews_counts_across_dataset(self) -> None:
        """Verify coverage counts for expert ratings, user ratings, and reviews."""
        expert_count = 0
        user_count = 0
        review_count = 0

        for _, row in self.df.iterrows():
            ratings_meta = parse_all_ratings_and_reviews(dict(row))
            if ratings_meta.expert_rating is not None:
                expert_count += 1
            if ratings_meta.user_rating.score is not None and ratings_meta.user_rating.count is not None:
                user_count += 1
            if ratings_meta.review.snippet is not None and ratings_meta.review.url is not None:
                review_count += 1

        self.assertEqual(expert_count, 1827)
        self.assertEqual(user_count, 2832)
        self.assertEqual(review_count, 1419)

    def test_relationship_type_distribution_sums_to_total_records(self) -> None:
        """Verify relationship_type distribution sums to exactly 2,928 and matches verified counts."""
        counts = {}
        for _, row in self.df.iterrows():
            brand_res = parse_brand(row["model_name"])
            rel = brand_res.relationship_type
            counts[rel] = counts.get(rel, 0) + 1

        total_sum = sum(counts.values())
        self.assertEqual(total_sum, 2928, f"Total listings across relationship types must be 2,928, got {total_sum}")

        expected_counts = {
            RELATIONSHIP_INDEPENDENT_OEM: 1865,
            RELATIONSHIP_SUBSIDIARY_SUBBRAND: 413,
            RELATIONSHIP_SUBSIDIARY_HOLDING: 292,
            RELATIONSHIP_SUBSIDIARY_ACQUISITION: 124,
            RELATIONSHIP_DIRECT_SUBBRAND: 105,
            RELATIONSHIP_TRADEMARK_LICENSE: 81,
            RELATIONSHIP_SUBSIDIARY_DIVESTMENT: 36,
            RELATIONSHIP_UNVERIFIED: 12,
        }
        self.assertEqual(counts, expected_counts)

    def test_parent_company_status_distribution_sums_to_total_records(self) -> None:
        """Verify parent_company_status distribution sums to exactly 2,928 and matches verified counts."""
        counts = {}
        for _, row in self.df.iterrows():
            brand_res = parse_brand(row["model_name"])
            status = brand_res.parent_company_status
            counts[status] = counts.get(status, 0) + 1

        total_sum = sum(counts.values())
        self.assertEqual(total_sum, 2928, f"Total listings across parent statuses must be 2,928, got {total_sum}")

        expected_counts = {
            PARENT_STATUS_NO_PARENT: 2035,
            PARENT_STATUS_VERIFIED_PARENT: 881,
            PARENT_STATUS_UNKNOWN: 12,
        }
        self.assertEqual(counts, expected_counts)

    def test_relationship_type_cross_tabulation_reconciles(self) -> None:
        """Verify cross-tabulation of relationship_type against parent_company_status reconciles in both dimensions."""
        cross_tab = {}
        for _, row in self.df.iterrows():
            brand_res = parse_brand(row["model_name"])
            key = (brand_res.relationship_type, brand_res.parent_company_status)
            cross_tab[key] = cross_tab.get(key, 0) + 1

        expected_cross_tab = {
            (RELATIONSHIP_INDEPENDENT_OEM, PARENT_STATUS_NO_PARENT): 1865,
            (RELATIONSHIP_SUBSIDIARY_SUBBRAND, PARENT_STATUS_VERIFIED_PARENT): 413,
            (RELATIONSHIP_SUBSIDIARY_HOLDING, PARENT_STATUS_VERIFIED_PARENT): 292,
            (RELATIONSHIP_SUBSIDIARY_ACQUISITION, PARENT_STATUS_VERIFIED_PARENT): 124,
            (RELATIONSHIP_DIRECT_SUBBRAND, PARENT_STATUS_NO_PARENT): 105,
            (RELATIONSHIP_TRADEMARK_LICENSE, PARENT_STATUS_NO_PARENT): 65,
            (RELATIONSHIP_TRADEMARK_LICENSE, PARENT_STATUS_VERIFIED_PARENT): 16,
            (RELATIONSHIP_SUBSIDIARY_DIVESTMENT, PARENT_STATUS_VERIFIED_PARENT): 36,
            (RELATIONSHIP_UNVERIFIED, PARENT_STATUS_UNKNOWN): 12,
        }
        self.assertEqual(cross_tab, expected_cross_tab)
        self.assertEqual(sum(cross_tab.values()), 2928)

    def test_no_duplicate_or_omitted_listing_assignments(self) -> None:
        """Verify every raw listing has exactly one primary relationship type and one parent status."""
        for idx, row in self.df.iterrows():
            brand_res = parse_brand(row["model_name"])
            self.assertIn(brand_res.relationship_type, VALID_RELATIONSHIP_TYPES)
            self.assertIn(brand_res.parent_company_status, VALID_PARENT_STATUSES)
            self.assertIn(brand_res.brand_relationship_confidence, VALID_CONFIDENCE_LEVELS)
            self.assertIn(brand_res.brand_resolution_status, VALID_RESOLUTION_STATUSES)
            self.assertIn(brand_res.historical_relationship_status, VALID_HISTORICAL_RELATIONSHIP_STATUSES)
            self.assertIn(brand_res.temporal_verification_status, VALID_TEMPORAL_STATUSES)

    def test_operating_company_distribution_sums_to_total_records(self) -> None:
        """Verify operating_company counts sum to exactly 2,916 non-null and 12 null records across 49 distinct entities."""
        op_counts = {}
        for _, row in self.df.iterrows():
            brand_res = parse_brand(row["model_name"])
            op = brand_res.operating_company
            op_counts[op] = op_counts.get(op, 0) + 1

        non_null_total = sum(count for op, count in op_counts.items() if op is not None)
        null_total = op_counts.get(None, 0)
        grand_total = non_null_total + null_total

        self.assertEqual(non_null_total, 2916, f"Non-null operating companies must sum to 2,916, got {non_null_total}")
        self.assertEqual(null_total, 12, f"Null operating companies must equal 12, got {null_total}")
        self.assertEqual(grand_total, 2928, f"Total operating companies must equal 2,928, got {grand_total}")

        # Explicitly verify Itel Mobile Limited listing count
        self.assertEqual(op_counts.get("Itel Mobile Limited"), 32, "Itel Mobile Limited must account for exactly 32 listings")

        # Explicitly verify Lenovo, Reliance, and Lyf separation
        self.assertEqual(op_counts.get("Lenovo Mobile Communication Technology Ltd."), 60)
        self.assertEqual(op_counts.get("Motorola Mobility LLC"), 119)
        self.assertEqual(op_counts.get("Jio Platforms Limited"), 2)
        self.assertEqual(op_counts.get("Reliance Retail Ltd."), 2)
        self.assertIsNone(op_counts.get("Lenovo Group Limited"), "Lenovo Group Limited should be parent holding entity, never operating company")
        self.assertIsNone(op_counts.get("Reliance Industries Limited"), "Reliance Industries Limited should be parent holding entity, never operating company")

        # Distinct non-null entity count must be exactly 49
        distinct_non_null = [op for op in op_counts.keys() if op is not None]
        self.assertEqual(len(distinct_non_null), 49, f"Must have exactly 49 distinct non-null operating companies, got {len(distinct_non_null)}")

    def test_temporal_semantics_and_historical_relationship_statuses(self) -> None:
        """Verify temporal semantics fields identify transitional vs static corporate lineages."""
        # Transitional brands
        nokia = parse_brand("Nokia G42 5G")
        moto = parse_brand("Motorola Edge 50 Pro")
        honor = parse_brand("Honor 90 5G")
        meizu = parse_brand("Meizu 21")
        nextbit = parse_brand("Nextbit Robin")

        for res in (nokia, moto, honor, meizu, nextbit):
            self.assertEqual(res.historical_relationship_status, HISTORICAL_RELATIONSHIP_TRANSITION_UNTIMED)
            self.assertEqual(res.temporal_verification_status, TEMPORAL_STATUS_LIMITATION_UNTIMED)
            self.assertTrue(len(res.current_corporate_relationship) > 0)

        # Neutral not-assessed brands (contemporary baseline without longitudinal historical audit)
        apple = parse_brand("Apple iPhone 15 Pro")
        samsung = parse_brand("Samsung Galaxy S24 Ultra")
        google = parse_brand("Google Pixel 8 Pro")

        for res in (apple, samsung, google):
            self.assertEqual(res.historical_relationship_status, HISTORICAL_RELATIONSHIP_NOT_ASSESSED)
            self.assertEqual(res.temporal_verification_status, TEMPORAL_STATUS_CONTEMPORARY_ONLY)
            self.assertTrue(len(res.current_corporate_relationship) > 0)

        # Unresolved brands
        mobiistar = parse_brand("Mobiistar X1 Dual")
        self.assertEqual(mobiistar.historical_relationship_status, HISTORICAL_RELATIONSHIP_UNKNOWN)
        self.assertEqual(mobiistar.temporal_verification_status, TEMPORAL_STATUS_LIMITATION_UNTIMED)

    def test_temporal_semantics_distribution_sums_to_total_records(self) -> None:
        """Verify historical relationship status and temporal verification status sum to exactly 2,928."""
        hist_counts = {}
        temp_counts = {}
        for _, row in self.df.iterrows():
            brand_res = parse_brand(row["model_name"])
            h_stat = brand_res.historical_relationship_status
            t_stat = brand_res.temporal_verification_status
            hist_counts[h_stat] = hist_counts.get(h_stat, 0) + 1
            temp_counts[t_stat] = temp_counts.get(t_stat, 0) + 1

        self.assertEqual(sum(hist_counts.values()), 2928)
        self.assertEqual(sum(temp_counts.values()), 2928)

        expected_hist = {
            HISTORICAL_RELATIONSHIP_NOT_ASSESSED: 2691,
            HISTORICAL_RELATIONSHIP_TRANSITION_UNTIMED: 225,
            HISTORICAL_RELATIONSHIP_UNKNOWN: 12,
        }
        self.assertEqual(hist_counts, expected_hist)

        expected_temp = {
            TEMPORAL_STATUS_CONTEMPORARY_ONLY: 2691,
            TEMPORAL_STATUS_LIMITATION_UNTIMED: 237,
        }
        self.assertEqual(temp_counts, expected_temp)

    def test_raw_csv_unmodified_byte_checksum(self) -> None:
        """Verify the raw CSV ground truth has not been modified or overwritten."""
        self.assertTrue(RAW_DATA_PATH.exists())
        file_bytes = RAW_DATA_PATH.read_bytes()
        self.assertEqual(len(file_bytes), RAW_FILE_EXPECTED_BYTES)

        sha256_hash = hashlib.sha256(file_bytes).hexdigest()
        self.assertEqual(sha256_hash, RAW_FILE_EXPECTED_SHA256)


if __name__ == "__main__":
    unittest.main()
