# file: file_watcher_windows_service.py

import win32serviceutil
import win32service
import win32event
import logging
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logging.basicConfig(
    filename="C:\\Users\\suziy\\Desktop\\file_watcher.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class WatcherHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"Created: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"Modified: {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory:
            logging.info(f"Deleted: {event.src_path}")


class FileWatcherService(win32serviceutil.ServiceFramework):
    _svc_name_ = "PythonFileWatcher"
    _svc_display_name_ = "Python File Watcher Service"
    _svc_description_ = "Watches a directory and logs file changes."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        logging.info("Starting service")

        watch_path = "C:\\Users\\suziy\\Downloads"
        event_handler = WatcherHandler()
        observer = Observer()
        observer.schedule(event_handler, watch_path, recursive=True)
        observer.start()

        while self.running:
            time.sleep(1)

        observer.stop()
        observer.join()
        logging.info("Stopping service")


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(FileWatcherService)
