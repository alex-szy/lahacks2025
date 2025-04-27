import click
import sys
import subprocess
from settings import BASE_DIR


@click.command()
def start():
    """
    Starts the munchkin daemon
    """
    daemon_path = BASE_DIR / "daemon.py"
    python_executable = sys.executable

    subprocess.Popen([python_executable, daemon_path], close_fds=True)
    click.echo("Starting Munchkin daemon...")
