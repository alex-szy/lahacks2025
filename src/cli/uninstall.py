import subprocess
import sys

import click


@click.command()
def uninstall():
    """
    Stop running munchkin at logon
    """
    if sys.platform == "win32":
        subprocess.run(
            ["schtasks", "/Delete", "/TN", "MunchkinDaemon", "/F"],
            check=False,
            stderr=subprocess.DEVNULL,
        )

        click.echo("Scheduled task 'MunchkinDaemon' deleted.")
    else:
        click.echo("Whoops, this hasn't been implemented yet!")
