import click
import subprocess


@click.command()
def uninstall():
    """
    Stop running munchkin at logon
    """
    subprocess.run([
        "schtasks",
        "/Delete",
        "/TN", "MunchkinDaemon",
        "/F"
    ], check=False, stderr=subprocess.DEVNULL)

    click.echo("Scheduled task 'MunchkinDaemon' deleted.")
