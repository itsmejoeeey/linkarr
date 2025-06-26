import logging
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def watch_folders(watched_folders, on_change_callback):
    """
    Watch the given folders for any changes and call on_change_callback when a change is detected.
    """
    class RerunHandler(FileSystemEventHandler):
        def __init__(self, watched_folder):
            self.watched_folder = watched_folder

        def on_created(self, event):
            logging.info(f"Detected file created: {event.src_path}")
            self.handler()

        def on_deleted(self, event):
            logging.info(f"Detected file deleted: {event.src_path}")
            self.handler()

        def on_moved(self, event):
            logging.info(f"Detected file moved: {event.src_path} to {event.dest_path}.")
            self.handler()

        def handler(self):
            on_change_callback(self.watched_folder)

    observer = Observer()
    for folder in watched_folders:
        event_handler = RerunHandler(folder)
        observer.schedule(event_handler, folder, recursive=True)
    observer.start()
    logging.info(f"Watching folders: {watched_folders}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
