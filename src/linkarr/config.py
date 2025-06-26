import json
import os
from typing import Any, Dict, List
import jsonschema
from linkarr.models import Job, MediaType, Config, RunMode, MediaServerFormat, LogLevel
from dataclasses import fields

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "config.schema.json")


class ConfigError(Exception):
    pass


def _get_default_value(cls, field_name: str) -> Any:
    """Get the default value for a field from a dataclass."""
    for field in fields(cls):
        if field.name == field_name:
            return field.default
    raise ValueError(f"Field {field_name} not found in {cls.__name__}")


def _default_job(job: Dict[str, Any]) -> Job:
    """
    Apply defaults and validate a single job config, returning a Job object.
    """
    if "src" not in job or "dest" not in job:
        raise ConfigError("Each job must have 'src' and 'dest' fields.")

    # Use defaults from Job dataclass in models.py
    media_type = job.get(
        "media_type", _get_default_value(Job, "media_type")
    )
    file_type_regex = job.get(
        "file_type_regex", _get_default_value(Job, "file_type_regex")
    )
    enabled = job.get("enabled", _get_default_value(Job, "enabled"))  # True

    return Job(
        src=job["src"],
        dest=job["dest"],
        media_type=media_type,
        file_type_regex=file_type_regex,
        enabled=enabled,
    )


def _load_schema() -> Dict[str, Any]:
    with open(SCHEMA_PATH, "r") as f:
        return json.load(f)


def load_config(config_path: str) -> Config:
    """
    Load and validate the config file, applying defaults where necessary.
    Returns a Config object with Job objects in the jobs list.
    """
    if not os.path.exists(config_path):
        raise ConfigError(f"Config file not found: {config_path}")
    with open(config_path, "r") as f:
        raw = json.load(f)
    schema = _load_schema()
    try:
        jsonschema.validate(instance=raw, schema=schema)
    except jsonschema.ValidationError as e:
        raise ConfigError(f"Config validation error: {e.message}")
    if "jobs" not in raw or not isinstance(raw["jobs"], list):
        raise ConfigError("Config must contain a 'jobs' list.")

    # Convert job dictionaries to Job objects
    jobs = [_default_job(job) for job in raw["jobs"]]

    # Use defaults from Config dataclass in models.py
    mode = raw.get(
        "mode", _get_default_value(Config, "mode")
    )
    media_server_format = raw.get(
        "media_server_format", _get_default_value(Config, "media_server_format")
    )
    log_level = raw.get(
        "log_level", _get_default_value(Config, "log_level")
    )

    return Config(
        jobs=jobs,
        mode=mode,
        media_server_format=media_server_format,
        log_level=log_level,
    )
