#!/usr/bin/env -S uv run --script

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "google-api-python-client",
#     "google-auth",
#     "google-auth-oauthlib",
#     "pydantic",
#     "pydantic-ai",
#     "pypdf",
#     "python-dotenv",
#     "watchdog",
# ]
# ///
import time
import os
import json
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from src.autocalendar.pdf_procesor import mark_calendar  # Assuming this is the module where the mark_calendar function is defined

class MyEventHandler(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent) -> None:
        try:
            if event.src_path.endswith('.pdf'):  # Check if the created file is a PDF
                print(f"File created: {event.src_path}")
                res= mark_calendar(event.src_path)
        except:
            return

def main():
    WATCH_DIR = os.path.join(os.path.expanduser('~'))  # Directory to watch for file changes
    print(WATCH_DIR)
    downloads_dir = json.load(open('C:\\Windows\\System32\\config\\systemprofile\\address.json'))['address']
    print(downloads_dir)
    print(os.getlogin())
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, downloads_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()