import time

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

class MyEventHandler(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent) -> None:
        print(f"File created: {event.src_path}")

WATCH_DIR = "C:/Users/hian/Downloads"  # Directory to watch for file changes
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