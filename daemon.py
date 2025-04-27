import threading
import time
import json
import signal
import logging
import sys
import os
import psutil
from engine.watcher import WatcherHandler
from settings import BASE_DIR, ASSETS_DIR, WATCH_PATHS_FILE
from watchdog.observers import Observer
import pystray
from PIL import Image, ImageDraw

PID_FILE = BASE_DIR / "daemon.pid"


class DaemonService:
    def __init__(self):
        self.running = True
        self.observers = []
        self.tray_icon = None
        self.watch_thread = None

    def get_pid(self):
        if PID_FILE.exists():
            try:
                with PID_FILE.open("r") as f:
                    pid = int(f.read().strip())
                if psutil.pid_exists(pid):
                    p = psutil.Process(pid)
                    if "python" in p.name().lower():
                        # Optionally check cmdline to be 100% sure it's your daemon
                        cmdline = p.cmdline()
                        if any("daemon.py" in part for part in cmdline):
                            return pid
            except Exception:
                # If error reading PID, assume stale file
                pass
        return None

    def write_pid_file(self):
        with PID_FILE.open("w") as f:
            f.write(str(os.getpid()))
        logging.info(f"Wrote PID {os.getpid()} to {PID_FILE}")

    def remove_pid_file(self):
        try:
            PID_FILE.unlink()
            logging.info(f"Removed PID file {PID_FILE}")
        except FileNotFoundError:
            pass

    def signal_handler(self, sig, frame):
        logging.info(f"Received signal {sig}, shutting down...")
        self.running = False
        if self.tray_icon:
            self.tray_icon.stop()

    def create_image(self):
        try:
            return Image.open(ASSETS_DIR / "munchkin.ico")
        except Exception as e:
            logging.error(f"Failed to load tray icon: {e}")
            # fallback simple black circle
            image = Image.new('RGB', (64, 64), color=(255, 255, 255))
            dc = ImageDraw.Draw(image)
            dc.ellipse((16, 16, 48, 48), fill=(0, 0, 0))
            return image

    def on_quit(self, icon, item):
        logging.info("Tray menu clicked Quit")
        self.signal_handler(signal.SIGINT, None)

    def setup_tray(self):
        self.tray_icon = pystray.Icon("munchkin")
        self.tray_icon.icon = self.create_image()
        self.tray_icon.title = "Munchkin Daemon"  # <-- this is the hover tooltip!
        self.tray_icon.menu = pystray.Menu(
            pystray.MenuItem("Quit", self.on_quit)
        )
        self.tray_icon.run()

    def watch_directories(self):
        logging.info("Starting service")
        logging.info(f"Watch paths file at: {WATCH_PATHS_FILE}")

        try:
            with open(WATCH_PATHS_FILE) as f:
                watch_paths = json.load(f)
        except Exception as e:
            logging.error(f"Failed to load watch paths: {e}")
            return

        logging.info(f"Watching directories: {watch_paths}")

        self.observers = [Observer() for _ in watch_paths]
        for observer, watch_path in zip(self.observers, watch_paths):
            event_handler = WatcherHandler()
            observer.schedule(event_handler, watch_path, recursive=True)
            observer.start()

        try:
            while self.running:
                time.sleep(1)
        finally:
            logging.info("Stopping observers...")
            for observer in self.observers:
                observer.stop()
            for observer in self.observers:
                observer.join()
            logging.info("Observers stopped.")

    def start(self):
        logging.basicConfig(
            filename=BASE_DIR / "mckndaemon.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        if self.get_pid() is not None:
            logging.error(
                "Another Munchkin daemon is already running. Exiting.")
            sys.exit(1)

        self.write_pid_file()
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        # Start background watcher thread
        self.watch_thread = threading.Thread(
            target=self.watch_directories, daemon=True)
        self.watch_thread.start()

        # Start the system tray (blocking)
        self.setup_tray()

        # After tray quits, shutdown
        logging.info("Tray icon closed, exiting service.")
        self.remove_pid_file()
        sys.exit(0)

    def stop(self):
        if (pid := self.get_pid()) is not None:
            os.kill(pid, signal.SIGTERM)
            self.remove_pid_file()
            return True
        return False


service = DaemonService()

# --- Entry Point ---
if __name__ == "__main__":
    service.start()
