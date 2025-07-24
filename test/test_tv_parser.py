import unittest
import os
from linkarr.parsers.tv import TVParser
from linkarr.models import TVShowInfo


class TestTVParser(unittest.TestCase):
    """Test cases for TV show parser functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = TVParser("/media/tv", ".*\\.mkv$")

    #
    # Parse info
    #

    def test_parse_info_valid_format_uppercase(self):
        """Test parse_info with valid TV show filename (S01E02 format)."""
        file_path = "/path/to/Show.Name.S01E02.mkv"
        result = self.parser.parse_info(file_path)

        self.assertIsInstance(result, TVShowInfo)
        if result:  # Type guard for linter
            self.assertEqual(result.series_name, "Show Name")
            self.assertEqual(result.season_number, "01")
            self.assertEqual(result.episode_number, "02")

    def test_parse_info_valid_format_lowercase(self):
        """Test parse_info with valid TV show filename (s01e02 format)."""
        file_path = "/path/to/Another.Show.s03e12.mkv"
        result = self.parser.parse_info(file_path)

        self.assertIsInstance(result, TVShowInfo)
        if result:  # Type guard for linter
            self.assertEqual(result.series_name, "Another Show")
            self.assertEqual(result.season_number, "03")
            self.assertEqual(result.episode_number, "12")

    def test_parse_info_with_special_characters(self):
        """Test parse_info with special characters in show name."""
        file_path = "/path/to/Show-Name!@#.S05E10.mkv"
        result = self.parser.parse_info(file_path)

        self.assertIsInstance(result, TVShowInfo)
        if result:  # Type guard for linter
            self.assertEqual(result.series_name, "Show-Name!@#")
            self.assertEqual(result.season_number, "05")
            self.assertEqual(result.episode_number, "10")

    def test_parse_info_invalid_format_no_season_episode(self):
        """Test parse_info with filename missing season/episode (should fail)."""
        file_path = "/path/to/not.a.tv.show.mkv"
        result = self.parser.parse_info(file_path)
        self.assertIsNone(result)


    #
    # Get destination path
    #

    def test_get_destination_path_valid(self):
        """Test get_destination_path with valid TV show."""
        source_file = "/path/to/Show.Name.S01E02.mkv"
        expected = os.path.join("/media/tv", "Show Name", "Season 01")

        result = self.parser.get_destination_path(source_file)
        self.assertEqual(result, expected)

    def test_get_destination_path_invalid(self):
        """Test get_destination_path with invalid TV show (should return None)."""
        source_file = "/path/to/not.a.tv.show.mkv"
        result = self.parser.get_destination_path(source_file)
        self.assertIsNone(result)

    def test_get_destination_path_different_destinations(self):
        """Test get_destination_path with different destination directories."""
        source_file = "/path/to/Show.Name.S01E02.mkv"
        test_cases = [
            ("/media/tv", "/media/tv/Show Name/Season 01"),
            ("/home/user/My TV", "/home/user/My TV/Show Name/Season 01"),
        ]

        for dest_path, expected in test_cases:
            with self.subTest(dest_path=dest_path):
                parser = TVParser(dest_path, ".*\\.mkv$")
                result = parser.get_destination_path(source_file)
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
