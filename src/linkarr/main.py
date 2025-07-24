import argparse
import sys
import os
from linkarr.config import load_config, ConfigError
from linkarr.helpers import clean_broken_symlinks, find_media_files, is_directory_path, logger, setup_logging
from linkarr.models import Job, MediaType, Config
from linkarr.parsers.tv import TVParser
from linkarr.parsers.movie import MovieParser
from linkarr.watch import watch_folders


def process_job(job: Job):
    """Process a single job."""
    os.makedirs(job.dest, exist_ok=True)
    num_removed_symlinks = clean_broken_symlinks(job.dest)

    parser = None
    match job.media_type:
        case "tv":
            parser = TVParser(job.dest)
        case "movie":
            parser = MovieParser(job.dest)

    num_added_symlinks = 0
    files = find_media_files(job.src, job.file_type_regex)
    for file in files:
        symlink_path = parser.organize_file(file)
        if symlink_path is not None:
            num_added_symlinks += 1

    logger.info(
        f"Added {num_added_symlinks} new symlink(s), removed {num_removed_symlinks} broken symlink(s)."
    )


def process_jobs(config: Config):
    """Process all jobs in the config."""
    for job in config.jobs:
        process_job(job)


def process_job_for_folder(config: Config, changed_folder: str):
    """Process only the job associated with the changed folder."""
    for job in config.jobs:
        if job.src == changed_folder:
            logger.info(f"Processing job for changed folder: {changed_folder}")
            process_job(job)
            return
    logger.warning(f"No job found for folder: {changed_folder}")


def main():
    parser = argparse.ArgumentParser(description="Media Organizer")
    parser.add_argument("config", help="Path to config JSON")
    args = parser.parse_args()

    try:
        config = load_config(args.config)
    except ConfigError as e:
        logger.error(f"Config error: {e}")
        sys.exit(1)

    # Setup logging with the configured log level
    setup_logging(config.log_level)
    logger.info(f"Config loaded from {args.config} successfully")

    match config.mode:
        case "watch":
            logger.info(f"Performing initial run")
            process_jobs(config)

            watched_folders = [job.src for job in config.jobs if job.enabled]
            for folder in watched_folders:
                if not is_directory_path(folder):
                    logger.error(f"Source folder does not exist: {folder}")
                    sys.exit(1)

            logger.info(f"Watching {len(watched_folders)} folders")
            watch_folders(watched_folders, lambda changed_folder: process_job_for_folder(config, changed_folder))
        case "once":
            logger.info(f"Triggering a single run")
            process_jobs(config)


if __name__ == "__main__":
    main()
