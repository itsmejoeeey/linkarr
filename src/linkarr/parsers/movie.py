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
        result = re.search(r".*/(.*?)\.([0-9]{4})\..*$", source_file_path)
        if not result:
            logger.warning(f"Failed to parse movie info from file: {source_file_path}")
            return None

        title = result.group(1).replace(".", " ").title()
        year = result.group(2)

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
