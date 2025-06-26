from typing import List, Literal, TypedDict, Optional
from dataclasses import dataclass

# Type aliases for better readability
MediaType = Literal["tv", "movie"]
MediaServerFormat = Literal["jellyfin"]
RunMode = Literal["watch", "once"]
LogLevel = Literal["debug", "info", "warning", "error", "critical"]


@dataclass
class ParsedInfo:
    """Base class for parsed media information."""

    pass


@dataclass
class TVShowInfo(ParsedInfo):
    """Parsed information for TV shows."""

    series_name: str
    season_number: str
    episode_number: str


@dataclass
class MovieInfo(ParsedInfo):
    """Parsed information for movies."""

    title: str
    year: str


@dataclass
class Job:
    """Represents a media organization job configuration."""

    src: str
    dest: str
    media_type: MediaType = "tv"
    file_type_regex: str = ".*\\.(mkv|mp4|avi)$"
    enabled: bool = True


@dataclass
class Config:
    """Represents the complete configuration."""

    jobs: List[Job]
    mode: RunMode = "watch"
    media_server_format: MediaServerFormat = "jellyfin"
    log_level: LogLevel = "info"
