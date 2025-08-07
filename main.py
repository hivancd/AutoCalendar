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

import dotenv

from src.autocalendar.utils import get_downloads_path 

import argparse

parser = argparse.ArgumentParser(description="AutoCalendar PDF Processor")
parser.add_argument('--user', type=str, help='Windows User to watch Downloads to.', required=False)
user= parser.parse_args().user
print(f"Watching Downloads for user: {user}")

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__),'.env')
dotenv.load_dotenv(env_path)  
api_key = os.getenv('OPENAI_API_KEY')

class MyEventHandler(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent) -> None:
        try:
            if event.src_path.endswith('.pdf'):  # Check if the created file is a PDF
                print(f"File created: {event.src_path}")
                res =mark_calendar(event.src_path, api_key)  # Call the mark_calendar function to process the PDF
                if res:   
                    print(f"Marked calendar for: {event.src_path}")
                    print( f"Event details: {res}")
                else:
                    print(f"Failed to mark calendar for: {event.src_path}")
        except Exception as e:
            print(f"Unexpected error processing file {event.src_path}: {e}")
            return

def main(user):
    # WATCH_DIR = os.path.join(os.path.expanduser(user),'Downloads')  # Directory to watch for file changes
    download_dir = json.load(open('C:\\Windows\\System32\\config\\systemprofile\\address.json'))['address']
    # print(WATCH_DIR)
    
    # Get the Downloads directory for the specified user
    if not user:
        user = 'hian'  # Default user if not provided
    
    # download_dir = get_downloads_path(user)  
    print(f"Downloads directory for user '{user}': {download_dir}")

    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, download_dir, recursive=True)
    observer.start()
    # f"Watching for new PDF files in {downloads_dir}..."
    try:
        while True:
            time.sleep(1)
    finally:
        print("Stopping observer...")
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main(user)