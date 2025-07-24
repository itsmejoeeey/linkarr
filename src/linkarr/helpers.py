import logging
import os
import shutil
import re

logger = logging.getLogger("linkarr")

def ensure_directory_exists(path):
    """Ensure the given directory exists."""
    os.makedirs(path, exist_ok=True)


def get_relative_symlink_paths(src_file, dest_path):
    """Return the relative source path and destination symlink path for a file."""
    rel_src_file = os.path.relpath(src_file, dest_path)
    dest_file = os.path.join(dest_path, os.path.basename(src_file))
    return rel_src_file, dest_file


def symlink_exists(dest_file):
    """Check if the symlink or file already exists at the destination."""
    return os.path.exists(dest_file)


def create_symlink(src_file, dest_path):
    """Create a symlink for src_file in dest_path if it doesn't already exist."""
    ensure_directory_exists(dest_path)
    rel_src_file, dest_file = get_relative_symlink_paths(src_file, dest_path)
    if symlink_exists(dest_file):
        logger.debug(f"Link '{dest_file}' already exists... Skipping...")
        return
    os.symlink(rel_src_file, dest_file)
    logger.debug(f"Created symlink: {dest_file} -> {rel_src_file}")
    return dest_file


def is_broken_symlink(symlink_location):
    """Check if a symlink is broken (its target does not exist)."""
    if not os.path.islink(symlink_location):
        return False
    file_location = os.readlink(symlink_location)
    absolute_src_file = os.path.normpath(
        os.path.join(os.path.dirname(symlink_location), file_location)
    )
    return not os.path.exists(absolute_src_file)


def remove_broken_symlink(symlink_location):
    """Remove a broken symlink and log a warning."""
    if not os.path.islink(symlink_location):
        logger.error(f"Attempting remove non-symlink at path {symlink_location}")
        return False
    logger.warning(f"Path {symlink_location} is a broken symlink")
    os.unlink(symlink_location)
    logger.debug(f"Removed symlink: {symlink_location}")


def remove_empty_directory(dir_path, root_path):
    """Remove a directory if it is empty and not the root path."""
    if len(os.listdir(dir_path)) == 0 and dir_path != root_path:
        logger.warning(f"Deleting empty dir: {dir_path}")
        shutil.rmtree(dir_path)


def clean_broken_symlinks(dest_path):
    """Remove broken symlinks and empty directories recursively in dest_path."""
    num_removed_symlinks = 0
    for dir_path, folder_names, files in os.walk(dest_path, topdown=False):
        for filename in files:
            symlink_location = os.path.join(dir_path, filename)
            if is_broken_symlink(symlink_location):
                remove_broken_symlink(symlink_location)
                num_removed_symlinks += 1
        remove_empty_directory(dir_path, dest_path)
    return num_removed_symlinks


def is_media_file(filename, file_type_regex):
    """Check if the filename matches the media file regex."""
    return re.match(file_type_regex, filename, re.IGNORECASE) is not None


def find_media_files(src_path, file_type_regex):
    """Recursively find all media files in src_path matching the regex."""
    matches = []
    for root, dirs, files in os.walk(src_path):
        for file in files:
            if is_media_file(file, file_type_regex):
                matches.append(os.path.join(root, file))
    return matches


def setup_logging(log_level: str = "info"):
    """Configure logging to output to the console with a standard format."""
    # Convert string log level to logging constant
    level_map = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    log_level_constant = level_map.get(log_level, logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.setLevel(log_level_constant)

    if not logger.hasHandlers():
        logger.addHandler(handler)


def is_directory_path(path):
    """Validate that the provided path is a valid existing directory."""
    if not os.path.exists(path):
        return False
    if not os.path.isdir(path):
        return False
    return True
