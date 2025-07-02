import click

from daemon_clerk import start as s


@click.command()
def start():
    """
    Starts the munchkin daemon
    """
    s()
    click.echo("Starting Munchkin daemon...")
