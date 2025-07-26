import os
import re
from typing import Optional
from .base import BaseParser
from linkarr.helpers import logger
from linkarr.models import TVShowInfo


class TVParser(BaseParser):
    """Parser for TV show files."""

    def parse_info(self, source_file_path: str) -> Optional[TVShowInfo]:
        """Parse TV show information from a source file path."""
        delim = self.DELIM_PATTERN
        pattern = (
            rf"(?:.*/)?"                    # Optional path
            rf"(?P<series>.+?)"             # Series name (non-greedy)
            rf"{delim}"
            rf"(?:\d{{4}}{delim})?"         # Optional year
            rf"[Ss](?P<season>\d{{2}})"     # Season
            rf"[Ee](?P<episode>\d{{2}})"    # Episode
            rf"(?:.*$)"                     # Rest of the filename
        )

        result = re.search(pattern, source_file_path, re.VERBOSE)
        if not result:
            logger.warning(f"Failed to parse TV show info from file: {source_file_path}")
            return None

        series_name = re.sub(delim, " ", result.group("series"))
        series_name = series_name.strip().title()
        season_number = result.group("season")
        episode_number = result.group("episode")

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
