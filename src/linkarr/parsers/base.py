import os
import re
from abc import ABC, abstractmethod
from typing import Optional
from linkarr.helpers import create_symlink, logger
from linkarr.models import ParsedInfo


class BaseParser(ABC):
    """Base class for media parsers that provides common functionality."""

    DELIM_PATTERN = r"[ .]"  # Delimiter: period or space

    def __init__(self, dest_path: str, file_type_regex: str):
        """Initialize parser."""
        self.dest_path = dest_path
        self.file_type_regex = file_type_regex

    @abstractmethod
    def parse_info(self, source_file_path: str) -> Optional[ParsedInfo]:
        """
        Parse media information from a source file path.

        Args:
            source_file_path: Path to the source media file

        Returns:
            ParsedInfo object containing the parsed information, or None if parsing fails
        """
        pass

    @abstractmethod
    def get_destination_path(self, source_file_path: str) -> Optional[str]:
        """
        Calculate the destination path for a given source file.

        Args:
            source_file_path: Path to the source media file

        Returns:
            Destination path where the file should be organized, or None if parsing fails
        """
        pass

    def check_file_type_valid(self, source_file_path: str) -> bool:
        """Check if the file matches the file_type_regex."""
        return re.match(self.file_type_regex, source_file_path) is not None

    def organize_file(self, source_file_path: str) -> Optional[str]:
        """
        Organize a file by creating a symlink at the calculated destination.

        Args:
            source_file_path: Path to the source media file

        Returns:
            Path to the created symlink, or None if organization fails
        """
        if not self.check_file_type_valid(source_file_path):
            logger.debug(f"Skipping file with ignored file type: {source_file_path}")
            return None

        dest_path = self.get_destination_path(source_file_path)
        if not dest_path:
            return None

        return create_symlink(source_file_path, dest_path)
