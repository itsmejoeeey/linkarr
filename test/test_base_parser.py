import unittest
import os
from linkarr.parsers.base import BaseParser
from linkarr.models import ParsedInfo

class DummyParser(BaseParser):
    """Minimal parser for testing file_type_regex in organize_file."""
    def parse_info(self, source_file_path: str):
        return ParsedInfo()
    def get_destination_path(self, source_file_path: str):
        # Just return a dummy path for testing
        return "/dummy/dest"

class TestBaseParser(unittest.TestCase):
    def setUp(self):
        self.dest_path = "/dummy/dest"

    def test_check_file_type_valid(self):
        parser = DummyParser(self.dest_path, r".*\.(mp4|avi)$")
        self.assertTrue(parser.check_file_type_valid("/some/path/file.mp4"))
        self.assertTrue(parser.check_file_type_valid("/some/path/file.avi"))
        self.assertFalse(parser.check_file_type_valid("/some/path/file.mkv"))

    def test_organize_file(self):
        parser = DummyParser(self.dest_path, r".*\.mkv$")
        result = parser.organize_file("/some/path/file.mkv")
        self.assertEqual(result, os.path.join(self.dest_path, "file.mkv"))

        result = parser.organize_file("/some/path/file.mp4")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
