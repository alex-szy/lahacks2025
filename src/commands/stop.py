import click

from daemon_clerk import stop as stop_daemon


@click.command()
def stop():
    """
    Stops the Munchkin Daemon
    """
    stop_daemon()
    click.echo("Stopping munchkin daemon...")
