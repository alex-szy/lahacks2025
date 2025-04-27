import click
import psutil
import os
import signal
from settings import BASE_DIR
from daemon import service

PID_FILE = BASE_DIR / "munchkin.pid"


@click.command()
def stop():
    """
    Stops the Munchkin Daemon
    """
    if (pid := service.get_pid()) is not None:
        click.echo("Stopping Munchkin daemon...")
        os.kill(pid, signal.SIGTERM)
        service.remove_pid_file()
    else:
        click.echo("Munchkin daemon doesn't seem to be running...")
