import click

import api.daemon


@click.command()
def stop():
    """
    Stops the Munchkin Daemon
    """
    api.daemon.stop()
    click.echo("Stopping munchkin daemon...")
