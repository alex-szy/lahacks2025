import click

import api.daemon


@click.command()
def start():
    """
    Starts the munchkin daemon
    """
    api.daemon.start()
    click.echo("Starting Munchkin daemon...")
