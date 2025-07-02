import click

from daemon_clerk import stop as s


@click.command()
def stop():
    """
    Stops the Munchkin Daemon
    """
    s()
    click.echo("Stopping munchkin daemon...")
