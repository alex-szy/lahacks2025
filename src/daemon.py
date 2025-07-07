import logging
import threading
import time

import pystray
import uvicorn
from fastapi import APIRouter, FastAPI
from PIL import Image, ImageDraw
from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver

from engine.db.database import VectorDatabase
from engine.queryprocessor import QueryProcessor
from engine.saveprocessor import SaveProcessor
from engine.watcher import WatcherHandler
from settings import ASSETS_DIR, BASE_DIR, settings


class DaemonService:
    def __init__(self):
        self.is_dead = threading.Event()
        self.tray_icon = None
        self.watchers: dict[str, BaseObserver] = {}
        self.router = APIRouter()
        self.router.add_api_route("/shutdown", self.shutdown, methods=["POST"])
        self.router.add_api_route("/ping", lambda: "mckndaemon", methods=["GET"])
        self.router.add_api_route("/refresh", self.refresh, methods=["POST"])
        self.router.add_api_route("/query", self.query)
        self.app = FastAPI()
        self.app.include_router(self.router)
        db = VectorDatabase()
        self.saveprocessor = SaveProcessor(db)
        self.queryprocessor = QueryProcessor(db)

    # API Routes

    def shutdown(self):
        logging.info("Shutting down...")
        self.is_dead.set()

    def refresh(self):
        self.__clear_observers()
        self.__populate_observers()

    def query(self, query: str, return_length: int = 5):
        return self.queryprocessor.process_query(query, return_length)

    def __create_image(self):
        try:
            return Image.open(ASSETS_DIR / "munchkin.ico")
        except Exception as e:
            logging.error(f"Failed to load tray icon: {e}")
            # fallback simple black circle
            image = Image.new("RGB", (64, 64), color=(255, 255, 255))
            dc = ImageDraw.Draw(image)
            dc.ellipse((16, 16, 48, 48), fill=(0, 0, 0))
            return image

    def __populate_observers(self):
        watch_paths = settings.get_watch_paths()
        logging.info(f"Watching directories: {watch_paths}")

        for watch_path in watch_paths:
            observer = Observer()
            event_handler = WatcherHandler(self.saveprocessor)
            observer.schedule(event_handler, watch_path)
            observer.start()
            self.watchers[watch_path] = observer

    def __clear_observers(self):
        logging.info("Stopping observers...")
        for observer in self.watchers.values():
            observer.stop()
        for observer in self.watchers.values():
            observer.join()
        logging.info("Observers stopped.")

    def __watch_directories(self):
        """
        Watcher runs on a separate thread, stopping when shutdown is called
        """
        logging.info("Starting service")

        self.__populate_observers()
        self.is_dead.wait()
        self.__clear_observers()

    def __start_server(self):
        """Start the lightweight fastapi server"""
        try:
            uvicorn.run(self.app)
        except SystemExit as e:
            if e.code != 0:
                logging.error(
                    f"FastAPI server exited with code {e.code}. Usually this means that the port is in use. Try a different port?"
                )
                self.shutdown()

    def __check_for_shutdown(self):
        """Calls tray_icon.stop during shutdown"""
        self.is_dead.wait()
        while True:
            if self.tray_icon:
                self.tray_icon.stop()
            time.sleep(1)

    def start(self):
        logging.basicConfig(
            filename=BASE_DIR / "mckndaemon.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

        # Start http api thread
        threading.Thread(target=self.__start_server, daemon=True).start()

        # Start the background watcher thread
        watcher_thread = threading.Thread(target=self.__watch_directories)
        watcher_thread.start()

        # Setup the system tray
        self.tray_icon = pystray.Icon("munchkin")
        self.tray_icon.icon = self.__create_image()
        self.tray_icon.title = "Munchkin Daemon"
        self.tray_icon.menu = pystray.Menu(
            pystray.MenuItem("Quit", lambda icon, item: self.shutdown())
        )

        # Start thread to stop systray on shutdown
        threading.Thread(target=self.__check_for_shutdown, daemon=True).start()

        # Start the system tray
        self.tray_icon.run()
        watcher_thread.join()


if __name__ == "__main__":
    DaemonService().start()
