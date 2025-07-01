import click
from daemon import service


@click.command()
def stop():
    """
    Stops the Munchkin Daemon
    """
    if service.stop():
        click.echo("Stopping Munchkin daemon...")
    else:
        click.echo("Munchkin daemon doesn't seem to be running...")
