"""Unit and Integration Tests for Pipeline Ingestion and Specification Parsers

Project: 'What Are We Really Paying For When We Buy a Smartphone?'
Phase 03 — Stage 02: Pipeline Foundation & Specification Parsing
"""

import sys
from pathlib import Path
import unittest

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.pipeline.config import (
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
    FLAG_UNRESOLVED_PROCESSOR,
    RAW_DATA_PATH,
    RAW_FILE_EXPECTED_BYTES,
    RAW_FILE_EXPECTED_MD5,
    RAW_FILE_EXPECTED_SHA256,
)
from scripts.pipeline.ingestion import compute_file_checksum, load_raw_dataset
from scripts.pipeline.parsers import (
    generate_config_id,
    generate_device_id,
    parse_all_specifications,
    parse_battery,
    parse_display,
    parse_front_cameras,
    parse_processor,
    parse_ram,
    parse_rear_cameras,
    parse_storage,
)


class TestRawDataIngestion(unittest.TestCase):
    """Verifies file checksum, schema validation, and source record identity."""

    def test_raw_file_checksum_integrity(self):
        """Asserts raw CSV byte count, SHA-256, and MD5 match verified ground truth."""
        report = compute_file_checksum(RAW_DATA_PATH)
        self.assertEqual(report.byte_count, RAW_FILE_EXPECTED_BYTES)
        self.assertEqual(report.sha256, RAW_FILE_EXPECTED_SHA256)
        self.assertEqual(report.md5, RAW_FILE_EXPECTED_MD5)
        self.assertTrue(report.is_fully_valid)

    def test_raw_dataset_loading_and_row_count(self):
        """Asserts raw dataset loads all 2,928 rows and 14 columns without row loss."""
        res = load_raw_dataset()
        self.assertEqual(res.row_count, 2928)
        # 14 original columns + 1 inserted listing_id column = 15
        self.assertEqual(res.column_count, 15)
        self.assertIn("listing_id", res.raw_dataframe.columns)
        self.assertEqual(res.raw_dataframe["listing_id"].iloc[0], "rec_0001")
        self.assertEqual(res.raw_dataframe["listing_id"].iloc[-1], "rec_2928")

    def test_source_record_id_stability(self):
        """Asserts listing_id assignments are deterministic across multiple calls."""
        res1 = load_raw_dataset()
        res2 = load_raw_dataset()
        self.assertEqual(
            res1.raw_dataframe["listing_id"].tolist(),
            res2.raw_dataframe["listing_id"].tolist(),
        )


class TestSpecificationParsers(unittest.TestCase):
    """Unit tests covering all individual specification parsers using real source records."""

    def test_ram_gb_parsing(self):
        """Standard GB RAM extraction."""
        res = parse_ram("8 GB RAM | 128 GB Storage")
        self.assertEqual(res.ram_capacity_gb, 8.0)
        self.assertEqual(res.quality_flags, [])

    def test_ram_mb_fractional_conversion(self):
        """MB to GB conversion: 512 MB -> 0.5 GB, 32 MB -> 0.03125 GB."""
        # Real row 1008: vivo Y15 (512 MB RAM | 4 GB Storage)
        res_512 = parse_ram("512 MB RAM | 4 GB Storage")
        self.assertEqual(res_512.ram_capacity_gb, 0.5)
        self.assertIn(FLAG_FRACTIONAL_MEMORY_MB, res_512.quality_flags)

        # Real row 2036: Nokia Asha 210 (32 MB RAM | 64 MB Storage)
        res_32 = parse_ram("32 MB RAM | 64 MB Storage")
        self.assertEqual(res_32.ram_capacity_gb, 0.03125)
        self.assertIn(FLAG_FRACTIONAL_MEMORY_MB, res_32.quality_flags)

    def test_ram_missing_or_storage_only(self):
        """RAM missing when input is None, empty, or storage-only string."""
        self.assertIsNone(parse_ram(None).ram_capacity_gb)
        self.assertIn(FLAG_MISSING_RAM, parse_ram(None).quality_flags)

        # Real row 1597: Blackberry Pearl 3G 9105 ('256 MB Storage' - no RAM declared)
        res_no_ram = parse_ram("256 MB Storage")
        self.assertIsNone(res_no_ram.ram_capacity_gb)
        self.assertIn(FLAG_MISSING_RAM, res_no_ram.quality_flags)

    def test_storage_gb_and_tb_conversion(self):
        """Storage extraction: 1 TB -> 1024 GB, 256 GB -> 256.0 GB."""
        # Real row 822: Apple iPhone 15 Pro Max 1TB ('8 GB RAM | 1 TB Storage')
        res_1tb = parse_storage("8 GB RAM | 1 TB Storage")
        self.assertEqual(res_1tb.storage_capacity_gb, 1024.0)
        self.assertIn(FLAG_1TB_STORAGE_UNIT, res_1tb.quality_flags)

        # Real row: Samsung Galaxy S24 Ultra ('12 GB RAM | 256 GB Storage')
        res_256 = parse_storage("12 GB RAM | 256 GB Storage")
        self.assertEqual(res_256.storage_capacity_gb, 256.0)

    def test_storage_mb_fractional_conversion(self):
        """Storage MB to GB conversion: 256 MB -> 0.25 GB, 64 MB -> 0.0625 GB."""
        # Real row 1549: Blackberry Bold 9780 ('512 MB RAM | 256 MB Storage')
        res_256mb = parse_storage("512 MB RAM | 256 MB Storage")
        self.assertEqual(res_256mb.storage_capacity_gb, 0.25)
        self.assertIn(FLAG_FRACTIONAL_STORAGE_MB, res_256mb.quality_flags)

        res_64mb = parse_storage("32 MB RAM | 64 MB Storage")
        self.assertEqual(res_64mb.storage_capacity_gb, 0.0625)

    def test_storage_missing(self):
        """Storage missing handling."""
        self.assertIsNone(parse_storage(None).storage_capacity_gb)
        self.assertIn(FLAG_MISSING_STORAGE, parse_storage(None).quality_flags)

    def test_battery_capacity_and_charging_wattage(self):
        """Independent extraction of battery mAh and fast charging wattage."""
        # Real row 0: vivo V40 ('5500 mAh | 80W Fast Charging')
        res1 = parse_battery("5500 mAh | 80W Fast Charging")
        self.assertEqual(res1.battery_capacity_mah, 5500)
        self.assertEqual(res1.charging_wattage, 80)
        self.assertEqual(res1.quality_flags, [])

        # Real row: Samsung Galaxy S24 Ultra ('5000 mAh | 45W Fast Charging')
        res2 = parse_battery("5000 mAh | 45W Fast Charging")
        self.assertEqual(res2.battery_capacity_mah, 5000)
        self.assertEqual(res2.charging_wattage, 45)

        # Standard battery without fast charging
        res3 = parse_battery("5000 mAh")
        self.assertEqual(res3.battery_capacity_mah, 5000)
        self.assertIsNone(res3.charging_wattage)
        self.assertIn(FLAG_MISSING_CHARGING, res3.quality_flags)

    def test_display_size_and_explicit_refresh_rate(self):
        """Screen size, explicit refresh rate, and strict null when Hz unstated (D03)."""
        # Real row 0: vivo V40 ('6.78″ (17.22 cm) 120Hz AMOLED Display')
        res_120 = parse_display("6.78″ (17.22 cm) 120Hz AMOLED Display")
        self.assertEqual(res_120.screen_size_inches, 6.78)
        self.assertEqual(res_120.refresh_rate_hz, 120)
        self.assertEqual(res_120.display_panel_family, "OLED")
        self.assertEqual(res_120.display_technology_raw, "AMOLED")

        # MANDATORY CHECK (D03): When Hz is not in raw string, refresh_rate_hz MUST BE None!
        # Real row: Nokia Asha 210 ('2.4″ (6.1 cm) LCD Display')
        res_no_hz = parse_display("2.4″ (6.1 cm) LCD Display")
        self.assertEqual(res_no_hz.screen_size_inches, 2.4)
        self.assertIsNone(res_no_hz.refresh_rate_hz)
        self.assertIn(FLAG_MISSING_REFRESH_RATE, res_no_hz.quality_flags)
        self.assertEqual(res_no_hz.display_panel_family, "LCD")

    def test_display_panel_taxonomy(self):
        """Categorizes OLED vs LCD family across diverse display technology strings."""
        self.assertEqual(
            parse_display("6.8″ 120Hz Dynamic AMOLED 2x Display").display_panel_family,
            "OLED",
        )
        self.assertEqual(
            parse_display("6.67″ 144Hz P-OLED Display").display_panel_family, "OLED"
        )
        self.assertEqual(
            parse_display("6.6″ 120Hz Super AMOLED Display").display_panel_family,
            "OLED",
        )
        self.assertEqual(
            parse_display("6.5″ 90Hz IPS LCD Display").display_panel_family, "LCD"
        )
        self.assertEqual(
            parse_display("5.0″ TFT LCD Display").display_panel_family, "LCD"
        )

    def test_rear_cameras_parsing(self):
        """Main sensor MP, lens count, and sensor breakdown extraction."""
        # Quad camera: Real row S24 Ultra ('200+12+10+50 MP Rear Camera')
        res_quad = parse_rear_cameras("200+12+10+50 MP Rear Camera")
        self.assertEqual(res_quad.rear_main_sensor_mp, 200.0)
        self.assertEqual(res_quad.rear_lens_count, 4)
        self.assertEqual(res_quad.sensor_breakdown_mp, [200.0, 12.0, 10.0, 50.0])

        # Dual camera: Real row vivo V40 ('50+50 MP Rear Camera')
        res_dual = parse_rear_cameras("50+50 MP Rear Camera")
        self.assertEqual(res_dual.rear_main_sensor_mp, 50.0)
        self.assertEqual(res_dual.rear_lens_count, 2)
        self.assertEqual(res_dual.sensor_breakdown_mp, [50.0, 50.0])

        # Single camera: Real row Blackberry 8900 ('3.2 MP Rear Camera')
        res_single = parse_rear_cameras("3.2 MP Rear Camera")
        self.assertEqual(res_single.rear_main_sensor_mp, 3.2)
        self.assertEqual(res_single.rear_lens_count, 1)
        self.assertEqual(res_single.sensor_breakdown_mp, [3.2])

    def test_front_cameras_parsing(self):
        """Front selfie camera MP and null handling."""
        res_front = parse_front_cameras("50 MP Front Camera")
        self.assertEqual(res_front.front_main_sensor_mp, 50.0)
        self.assertEqual(res_front.front_lens_count, 1)

        # Missing front camera
        res_none = parse_front_cameras(None)
        self.assertIsNone(res_none.front_main_sensor_mp)
        self.assertIn(FLAG_MISSING_FRONT_CAMERAS, res_none.quality_flags)

    def test_processor_parsing_and_hisilicon_preservation(self):
        """Processor manufacturer, model, and cores. Preserves HiSilicon separately from Unisoc."""
        # Qualcomm
        res_snap = parse_processor("Snapdragon 8 Gen 3 Octa core")
        self.assertEqual(res_snap.manufacturer, "Qualcomm")
        self.assertEqual(res_snap.family, "Snapdragon")
        self.assertEqual(res_snap.core_count, 8)
        self.assertEqual(res_snap.model, "Snapdragon 8 Gen 3")

        # Apple Silicon
        res_apple = parse_processor("Apple A17 Pro Hexa Core")
        self.assertEqual(res_apple.manufacturer, "Apple")
        self.assertEqual(res_apple.family, "Apple Silicon")
        self.assertEqual(res_apple.core_count, 6)

        # HiSilicon Kirin (Must NOT be mapped to Unisoc!)
        res_kirin = parse_processor("HiSilicon Kirin 9000 Octa core")
        self.assertEqual(res_kirin.manufacturer, "HiSilicon")
        self.assertEqual(res_kirin.family, "Kirin")
        self.assertNotEqual(res_kirin.manufacturer, "Unisoc")

        # Unisoc
        res_unisoc = parse_processor("Unisoc T612 Octa core")
        self.assertEqual(res_unisoc.manufacturer, "Unisoc")

        # Niche Known Manufacturers
        res_broadcom = parse_processor("Broadcom")
        self.assertEqual(res_broadcom.manufacturer, "Broadcom")
        self.assertEqual(res_broadcom.family, "Broadcom")

        res_nvidia = parse_processor("Nvidia Tegra 3")
        self.assertEqual(res_nvidia.manufacturer, "Nvidia")
        self.assertEqual(res_nvidia.family, "Tegra")

        res_ste = parse_processor("ST-Ericsson NovaThor")
        self.assertEqual(res_ste.manufacturer, "ST-Ericsson")
        self.assertEqual(res_ste.family, "NovaThor")

        res_k3v2 = parse_processor("Huawei K3V2")
        self.assertEqual(res_k3v2.manufacturer, "HiSilicon")
        self.assertEqual(res_k3v2.family, "K3V2")

        # Unresolved/Unknown Processor Descriptions (Strict Null, NOT 'Other')
        res_quad = parse_processor("Quad core")
        self.assertIsNone(res_quad.manufacturer)
        self.assertIsNone(res_quad.family)
        self.assertEqual(res_quad.core_count, 4)
        self.assertIn(FLAG_UNRESOLVED_PROCESSOR, res_quad.quality_flags)

        res_tru = parse_processor("Tru-Octa Core")
        self.assertIsNone(res_tru.manufacturer)
        self.assertIsNone(res_tru.family)
        self.assertEqual(res_tru.core_count, 8)
        self.assertIn(FLAG_UNRESOLVED_PROCESSOR, res_tru.quality_flags)

        # Missing processor
        res_proc_none = parse_processor(None)
        self.assertIsNone(res_proc_none.manufacturer)
        self.assertIn(FLAG_MISSING_PROCESSOR, res_proc_none.quality_flags)


class TestIdentitySeparation(unittest.TestCase):
    """Verifies Mandatory Correction 2A: Separate device_id, config_id, and listing_id."""

    def test_device_id_preserves_meaningful_model_tiers(self):
        """Asserts generate_device_id preserves Pro, Plus, Ultra, 5G, Lite, Fusion, etc."""
        # Galaxy S24 Tier Preservations
        s24_ultra = generate_device_id("Samsung Galaxy S24 Ultra")
        s24_plus = generate_device_id("Samsung Galaxy S24 Plus 5G")
        s24_base = generate_device_id("Samsung Galaxy S24 5G")
        self.assertEqual(s24_ultra, "samsung-galaxy-s24-ultra")
        self.assertEqual(s24_plus, "samsung-galaxy-s24-plus-5g")
        self.assertEqual(s24_base, "samsung-galaxy-s24-5g")
        self.assertNotEqual(s24_ultra, s24_plus)
        self.assertNotEqual(s24_plus, s24_base)

        # iPhone 15 Tier Preservations
        ip15_promax = generate_device_id("Apple iPhone 15 Pro Max")
        ip15_pro = generate_device_id("Apple iPhone 15 Pro")
        ip15_plus = generate_device_id("Apple iPhone 15 Plus")
        ip15_base = generate_device_id("Apple iPhone 15")
        self.assertEqual(ip15_promax, "apple-iphone-15-pro-max")
        self.assertEqual(ip15_pro, "apple-iphone-15-pro")
        self.assertEqual(ip15_plus, "apple-iphone-15-plus")
        self.assertEqual(ip15_base, "apple-iphone-15")
        self.assertEqual(len({ip15_promax, ip15_pro, ip15_plus, ip15_base}), 4)

        # Mid-Range Tier Preservations
        moto_pro = generate_device_id("Motorola Edge 50 Pro 5G")
        moto_fusion = generate_device_id("Motorola Edge 50 Fusion")
        self.assertEqual(moto_pro, "motorola-edge-50-pro-5g")
        self.assertEqual(moto_fusion, "motorola-edge-50-fusion")
        self.assertNotEqual(moto_pro, moto_fusion)

        nord_lite = generate_device_id("OnePlus Nord CE 4 Lite 5G")
        nord_ce4 = generate_device_id("OnePlus Nord CE 4 5G")
        self.assertEqual(nord_lite, "oneplus-nord-ce-4-lite-5g")
        self.assertEqual(nord_ce4, "oneplus-nord-ce-4-5g")
        self.assertNotEqual(nord_lite, nord_ce4)

        # Only memory suffixes stripped
        s24_ultra_1tb = generate_device_id("Samsung Galaxy S24 Ultra 1TB")
        self.assertEqual(s24_ultra_1tb, s24_ultra)

        mi_max_32gb = generate_device_id("Xiaomi Mi Max 32GB")
        mi_max_base = generate_device_id("Xiaomi Mi Max")
        self.assertEqual(mi_max_32gb, mi_max_base)

    def test_xiaomi_mi_max_shares_config_id_with_distinct_listing_ids(self):
        """Xiaomi Mi Max and Xiaomi Mi Max 32GB share config_id but have distinct listing_ids (D01)."""
        row_v1 = {
            "model_name": "Xiaomi Mi Max",
            "ram_internal_memory": "3 GB RAM | 32 GB Storage",
            "battery": "4850 mAh",
            "display": "6.4″ (16.26 cm) IPS LCD Display",
            "rear_cameras": "16 MP Rear Camera",
            "front_cameras": "5 MP Front Camera",
            "processor": "Snapdragon 650 Hexa Core",
        }
        row_v2 = {
            "model_name": "Xiaomi Mi Max 32GB",
            "ram_internal_memory": "3 GB RAM | 32 GB Storage",
            "battery": "4850 mAh",
            "display": "6.4″ (16.26 cm) IPS LCD Display",
            "rear_cameras": "16 MP Rear Camera",
            "front_cameras": "5 MP Front Camera",
            "processor": "Snapdragon 650 Hexa Core",
        }

        parsed_v1 = parse_all_specifications(row_v1, listing_id="rec_0356")
        parsed_v2 = parse_all_specifications(row_v2, listing_id="rec_0357")

        # Distinct source listing identifiers
        self.assertEqual(parsed_v1.listing_id, "rec_0356")
        self.assertEqual(parsed_v2.listing_id, "rec_0357")
        self.assertNotEqual(parsed_v1.listing_id, parsed_v2.listing_id)

        # Same canonical base device identity
        self.assertEqual(parsed_v1.device_id, "xiaomi-mi-max")
        self.assertEqual(parsed_v2.device_id, "xiaomi-mi-max")

        # Same hardware configuration identity (identical 3GB/32GB specs)
        self.assertEqual(parsed_v1.config_id, parsed_v2.config_id)
        self.assertEqual(parsed_v1.config_id, "xiaomi-mi-max_3gb_32gb")

    def test_memory_variants_have_different_config_ids(self):
        """Variants of iPhone 15 Pro Max share device_id but have different config_ids."""
        dev_id = generate_device_id("Apple iPhone 15 Pro Max 256GB")
        self.assertEqual(dev_id, "apple-iphone-15-pro-max")

        config_256 = generate_config_id(dev_id, ram_gb=8.0, storage_gb=256.0)
        config_1tb = generate_config_id(dev_id, ram_gb=8.0, storage_gb=1024.0)

        self.assertEqual(config_256, "apple-iphone-15-pro-max_8gb_256gb")
        self.assertEqual(config_1tb, "apple-iphone-15-pro-max_8gb_1024gb")
        self.assertNotEqual(config_256, config_1tb)

    def test_plus_sign_semantic_preservation_and_collision_prevention(self):
        """Verify plus sign is preserved semantically as 'plus' preventing device and config collisions."""
        # OPPO Reno10 Pro vs Reno10 Pro+
        reno_pro = generate_device_id("OPPO Reno10 Pro 5G")
        reno_pro_plus = generate_device_id("OPPO Reno10 Pro+ 5G")
        self.assertEqual(reno_pro, "oppo-reno10-pro-5g")
        self.assertEqual(reno_pro_plus, "oppo-reno10-pro-plus-5g")
        self.assertNotEqual(reno_pro, reno_pro_plus)

        config_pro = generate_config_id(reno_pro, 12.0, 256.0)
        config_pro_plus = generate_config_id(reno_pro_plus, 12.0, 256.0)
        self.assertEqual(config_pro, "oppo-reno10-pro-5g_12gb_256gb")
        self.assertEqual(config_pro_plus, "oppo-reno10-pro-plus-5g_12gb_256gb")
        self.assertNotEqual(config_pro, config_pro_plus)

        # OPPO F19 Pro vs F19 Pro+
        f19_pro = generate_device_id("OPPO F19 Pro")
        f19_pro_plus = generate_device_id("OPPO F19 Pro+ 5G")
        self.assertEqual(f19_pro, "oppo-f19-pro")
        self.assertEqual(f19_pro_plus, "oppo-f19-pro-plus-5g")
        self.assertNotEqual(f19_pro, f19_pro_plus)

        # Sony Xperia Z3 vs Z3+
        z3 = generate_device_id("Sony Xperia Z3")
        z3_plus = generate_device_id("Sony Xperia Z3+")
        self.assertEqual(z3, "sony-xperia-z3")
        self.assertEqual(z3_plus, "sony-xperia-z3-plus")
        self.assertNotEqual(z3, z3_plus)


class TestFullRawDatasetEndToEndParsing(unittest.TestCase):
    """Integration test running all parsers over all 2,928 rows of the raw dataset."""

    @classmethod
    def setUpClass(cls):
        cls.ingestion_res = load_raw_dataset()

    def test_full_dataset_parsing_without_exceptions(self):
        """Verifies that all 2,928 raw rows parse cleanly without unhandled exceptions."""
        df = self.ingestion_res.raw_dataframe
        self.assertEqual(len(df), 2928)

        parsed_records = []
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            listing_id = row_dict["listing_id"]
            parsed = parse_all_specifications(row_dict, listing_id=listing_id)
            parsed_records.append(parsed)

        self.assertEqual(len(parsed_records), 2928)

        # Audit that 1TB phones never have 1GB storage
        for p in parsed_records:
            if "1TB" in str(p.device_id).upper() or "1 TB" in str(p.storage.raw_input):
                self.assertEqual(
                    p.storage.storage_capacity_gb,
                    1024.0,
                    f"1TB storage parsing failure on listing {p.listing_id}",
                )

        # Audit that HiSilicon processors are never mapped to Unisoc
        for p in parsed_records:
            if p.processor.raw_input and "kirin" in p.processor.raw_input.lower():
                self.assertEqual(p.processor.manufacturer, "HiSilicon")
                self.assertNotEqual(p.processor.manufacturer, "Unisoc")

        # Audit that refresh rate is None when Hz is absent
        for p in parsed_records:
            if p.display.raw_input and "hz" not in p.display.raw_input.lower():
                self.assertIsNone(
                    p.display.refresh_rate_hz,
                    f"Refresh rate must be None when Hz is absent: {p.display.raw_input}",
                )


if __name__ == "__main__":
    unittest.main()
