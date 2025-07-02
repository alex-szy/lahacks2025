import click

from utilities.daemon_utils import start as s


@click.command()
def start():
    """
    Starts the munchkin daemon
    """
    s()
    click.echo("Starting Munchkin daemon...")
