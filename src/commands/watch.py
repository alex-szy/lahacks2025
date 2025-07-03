from pathlib import Path

import click

from settings import settings
from daemon_clerk import refresh_if_running
from utils import is_forbidden


@click.group()
def watch():
    """Configure watch folders."""
    pass


def _add(folder_path: str):
    folder_path = str(Path(folder_path).resolve())

    if is_forbidden(folder_path):
        raise click.BadParameter("Access is denied", param_hint="FOLDER_PATH")

    paths = settings.get_watch_paths()
    if folder_path in paths:
        click.echo(f"Notice: The folder '{folder_path}' is already being watched.")
        return

    paths.append(folder_path)
    settings.set_watch_paths(paths)
    click.echo(f"Added folder '{folder_path}' to watch list.")
    refresh_if_running()


def _remove(folder_path: str):
    folder_path = str(Path(folder_path).resolve())

    paths = settings.get_watch_paths()
    if folder_path not in paths:
        click.echo(f"Notice: The folder '{folder_path}' is not in the watch list.")
        return

    paths.remove(folder_path)
    settings.set_watch_paths(paths)
    click.echo(f"Removed folder '{folder_path}' from watch list.")
    refresh_if_running()


def _list_watch():
    paths = settings.get_watch_paths()
    if not paths:
        click.echo("No watch folders configured.")
    else:
        for path in paths:
            click.echo(path)


@watch.command()
@click.argument(
    "folder_path", type=click.Path(exists=True, file_okay=False, resolve_path=True)
)
def add(folder_path):
    """Add a watch folder."""
    _add(folder_path)


@watch.command()
@click.argument("folder_path", type=click.Path(file_okay=False, resolve_path=True))
def remove(folder_path):
    """Remove a watch folder."""
    _remove(folder_path)


@watch.command(name="list")
def list_watch():
    """List watch folders."""
    _list_watch()
