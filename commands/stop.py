import click
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
    if service.stop():
        click.echo("Stopping Munchkin daemon...")
    else:
        click.echo("Munchkin daemon doesn't seem to be running...")
