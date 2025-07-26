import os
import re
from typing import Optional
from .base import BaseParser
from linkarr.helpers import logger
from linkarr.models import MovieInfo


class MovieParser(BaseParser):
    """Parser for movie files."""

    def parse_info(self, source_file_path: str) -> Optional[MovieInfo]:
        """Parse movie information from a source file path."""
        delim = self.DELIM_PATTERN
        pattern = (
            rf"(?:.*/)?"            # Optional path
            rf"(?P<movie>.+?)"      # Movie name (non-greedy)
            rf"{delim}"
            rf"(?P<year>\d{{4}})"   # Movie year
            rf"(?:.*$)"             # Rest of the filename
        )
        result = re.search(pattern, source_file_path)
        if not result:
            logger.warning(f"Failed to parse movie info from file: {source_file_path}")
            return None

        title = re.sub(delim, " ", result.group("movie"))
        title = title.strip().title()
        year = result.group("year")

        return MovieInfo(title=title, year=year)

    def get_destination_path(self, source_file_path: str) -> Optional[str]:
        """Calculate the destination path for a movie file."""
        parsed_info = self.parse_info(source_file_path)
        if not parsed_info:
            return None

        target_dir = os.path.join(
            self.dest_path, f"{parsed_info.title} ({parsed_info.year})"
        )
        return target_dir
