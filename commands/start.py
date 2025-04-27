import click
import sys
import subprocess
from pathlib import Path
from settings import BASE_DIR


def _start():
    daemon_path = BASE_DIR / "daemon.py"
    python_executable = Path(sys.executable).resolve().parent / "pythonw.exe"

    subprocess.Popen([python_executable, daemon_path],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


@click.command()
def start():
    """
    Starts the munchkin daemon
    """
    _start()
    click.echo("Starting Munchkin daemon...")
