import click

from daemon_clerk import start as start_daemon


@click.command()
def start():
    """
    Starts the munchkin daemon
    """
    start_daemon()
    click.echo("Starting Munchkin daemon...")
