import time
import os

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from pdf_procesor import mark_calendar  # Assuming this is the module where the mark_calendar function is defined

class MyEventHandler(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent) -> None:
        try:
            if event.src_path.endswith('.pdf'):  # Check if the created file is a PDF
                print(f"File created: {event.src_path}")
                res= mark_calendar(event.src_path)
        except:
            return

WATCH_DIR = os.path.expanduser('~/Downloads')  # Directory to watch for file changes
event_handler = MyEventHandler()
observer = Observer()
observer.schedule(event_handler, WATCH_DIR, recursive=True)
observer.start()
try:
    while True:
        time.sleep(1)
finally:
    observer.stop()
    observer.join()