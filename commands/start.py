import click
import sys
import subprocess
from settings import BASE_DIR


def _start():
    daemon_path = BASE_DIR / "daemon.py"
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


@click.command()
def start():
    """
    Starts the munchkin daemon
    """
    _start()
    click.echo("Starting Munchkin daemon...")
