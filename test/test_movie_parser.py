import unittest
import os
from linkarr.parsers.movie import MovieParser
from linkarr.models import MovieInfo


class TestMovieParser(unittest.TestCase):
    """Test cases for movie parser functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = MovieParser("/media/movies", ".*\\.mkv$")

    #
    # Parse info
    #

    def test_parse_info_valid_format_simple(self):
        """Test parse_info with valid movie filename (title.year.extension)."""
        source_file = "/path/to/Movie.Title.2023.mkv"
        result = self.parser.parse_info(source_file)

        self.assertIsInstance(result, MovieInfo)
        if result:  # Type guard for linter
            self.assertEqual(result.title, "Movie Title")
            self.assertEqual(result.year, "2023")
    
    def test_parse_info_valid_format_extended(self):
        """Test parse_info with valid movie filename (title.year.extension.res.details)."""
        source_file = "/path/to/Movie.Title.2023.1080p.x264.mkv"
        result = self.parser.parse_info(source_file)

        self.assertIsInstance(result, MovieInfo)
        if result:  # Type guard for linter
            self.assertEqual(result.title, "Movie Title")
            self.assertEqual(result.year, "2023")

    def test_parse_info_with_special_characters(self):
        """Test parse_info with special characters in title."""
        source_file = "/path/to/Movie-Title!@#.2023.mkv"
        result = self.parser.parse_info(source_file)

        self.assertIsInstance(result, MovieInfo)
        if result:  # Type guard for linter
            self.assertEqual(result.title, "Movie-Title!@#")
            self.assertEqual(result.year, "2023")


    #
    # Get destination path
    #

    def test_get_destination_path_valid(self):
        """Test get_destination_path with valid movie file."""
        source_file = "/path/to/Movie.Title.2023.mkv"
        expected = "/media/movies/Movie Title (2023)"

        result = self.parser.get_destination_path(source_file)
        self.assertEqual(result, expected)

    def test_get_destination_path_invalid(self):
        """Test get_destination_path with invalid movie file (should return None)."""
        source_file = "/path/to/not.a.movie.mkv"
        result = self.parser.get_destination_path(source_file)
        self.assertIsNone(result)

    def test_get_destination_path_different_destinations(self):
        """Test get_destination_path with different destination directories."""
        source_file = "/path/to/Movie.Title.2023.mkv"
        test_cases = [
            ("/media/movies", "/media/movies/Movie Title (2023)"),
            ("/home/user/My Movies", "/home/user/My Movies/Movie Title (2023)"),
        ]

        for dest_path, expected in test_cases:
            with self.subTest(dest_path=dest_path):
                parser = MovieParser(dest_path, ".*\\.mkv$")
                result = parser.get_destination_path(source_file)
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
