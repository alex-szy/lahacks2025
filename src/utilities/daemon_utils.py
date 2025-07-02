import subprocess
import sys

import requests

from settings import BASE_DIR, settings


def is_running():
    try:
        res = requests.get(
            f"http://localhost:{settings.get_daemon_port()}/ping", timeout=0.5
        )
        return res.ok and res.text == '"mckndaemon"'
    except requests.ConnectionError:
        return False


def stop():
    try:
        requests.post(
            f"http://localhost:{settings.get_daemon_port()}/shutdown", timeout=0.5
        )
    except:  # noqa: E722
        pass


def start():
    if is_running():
        return
    daemon_path = BASE_DIR / "src" / "daemon.py"
    if sys.platform == "win32":
        subprocess.Popen(
            [sys.executable, daemon_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
    else:
        subprocess.Popen(
            [sys.executable, daemon_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )


def refresh_if_running():
    try:
        requests.post(
            f"http://localhost:{settings.get_daemon_port()}/refresh", timeout=0.5
        )
    except:  # noqa: E722
        pass
