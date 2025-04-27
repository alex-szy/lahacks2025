import win32serviceutil
import win32service
import win32event
import logging
import time
import json
import os
from watchdog.observers import Observer
from watcher import WatcherHandler

logging.basicConfig(
    filename="C:\\Users\\suziy\\Desktop\\file_watcher.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
WATCH_PATHS_FILE = os.path.join(CONFIG_DIR, "watch_paths.json")


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
        logging.info(f"Watch paths file at: {WATCH_PATHS_FILE}")
        try:
            watch_paths = json.load(open(WATCH_PATHS_FILE))
            logging.info(f"Watching directories: {watch_paths}")

            # Instantiate an observer for every watched directory
            observers = [Observer() for _ in watch_paths]
            for observer, watch_path in zip(observers, watch_paths):
                observer.schedule(WatcherHandler(), watch_path, recursive=True)
                observer.start()

            while self.running:
                time.sleep(1)

            for observer in observers:
                observer.stop()
                observer.join()

            logging.info("Stopping service")
        except Exception as e:
            logging.error(e)


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(FileWatcherService)
