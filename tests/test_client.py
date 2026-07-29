import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from chongplus_image_mcp import client as CLIENT_MODULE


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.config_root = tempfile.TemporaryDirectory()
        self.previous_config_root = os.environ.get("XDG_CONFIG_HOME")
        os.environ["XDG_CONFIG_HOME"] = self.config_root.name

    def tearDown(self):
        if self.previous_config_root is None:
            os.environ.pop("XDG_CONFIG_HOME", None)
        else:
            os.environ["XDG_CONFIG_HOME"] = self.previous_config_root
        self.config_root.cleanup()

    def test_save_key_is_private_and_reports_configured(self):
        CLIENT_MODULE.save_api_key("sk-test-value")
        path = CLIENT_MODULE.config_path()
        self.assertTrue(CLIENT_MODULE.is_configured())
        self.assertEqual(json.loads(path.read_text())["api_key"], "sk-test-value")
        if os.name != "nt":
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(path.parent.stat().st_mode & 0o777, 0o700)

    def test_empty_key_is_rejected(self):
        with self.assertRaises(CLIENT_MODULE.ChongPlusError):
            CLIENT_MODULE.save_api_key("  ")

    def test_invalid_options_are_rejected_before_network(self):
        with self.assertRaises(CLIENT_MODULE.ChongPlusError):
            CLIENT_MODULE._validate_request("1x2", 1)
        with self.assertRaises(CLIENT_MODULE.ChongPlusError):
            CLIENT_MODULE._validate_request("2048x2048", 5)

    def test_png_dimensions(self):
        raw = b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\rIHDR" + (1024).to_bytes(4, "big") + (1536).to_bytes(4, "big")
        self.assertEqual(CLIENT_MODULE._png_dimensions(raw), (1024, 1536))
