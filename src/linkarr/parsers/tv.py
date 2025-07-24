import logging
import os
import re
from typing import Optional
from .base import BaseParser
from linkarr.models import TVShowInfo


class TVParser(BaseParser):
    """Parser for TV show files."""

    def parse_info(self, source_file_path: str) -> Optional[TVShowInfo]:
        """Parse TV show information from a source file path."""
        result = re.search(r".*/(.*).[Ss]([0-9]{2})[Ee]([0-9]{2}).*$", source_file_path)
        if not result:
            logging.debug(f"Failed to parse TV show info from {source_file_path}")
            return None

        series_name = result.group(1).replace(".", " ").title()
        season_number = result.group(2)
        episode_number = result.group(3)

        return TVShowInfo(
            series_name=series_name,
            season_number=season_number,
            episode_number=episode_number,
        )

    def get_destination_path(self, source_file_path: str) -> Optional[str]:
        """Calculate the destination path for a TV show file."""
        parsed_info = self.parse_info(source_file_path)
        if not parsed_info:
            return None

        target_dir = os.path.join(
            self.dest_path,
            parsed_info.series_name,
            f"Season {parsed_info.season_number}",
        )
        return target_dir
