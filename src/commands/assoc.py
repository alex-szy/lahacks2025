from pathlib import Path

import click

from settings import settings
from daemon_clerk import refresh_if_running
from utils import is_forbidden


@click.group()
def assoc():
    """Configure destination folder associations."""
    pass


def _add(folder_path: str, description: str):
    folder_path = str(Path(folder_path).resolve())
    if is_forbidden(folder_path):
        raise click.BadParameter("Access is denied", param_hint="FOLDER_PATH")
    paths = settings.get_folder_paths()
    paths[folder_path] = description
    settings.set_folder_paths(paths)
    click.echo(f"Sucessfully added: {folder_path}, {description}")
    refresh_if_running()


def _remove(folder_path: str):
    folder_path = str(Path(folder_path).resolve())
    paths = settings.get_folder_paths()
    if folder_path in paths:
        del paths[folder_path]
        settings.set_folder_paths(paths)
        refresh_if_running()


def _list_assoc():
    paths = settings.get_folder_paths()
    if not paths:
        click.echo("No folder path associations configured.")
        return
    click.echo("Existing Paths:\n")
    for path, info in paths.items():
        click.echo(path)
        click.echo(info)
        click.echo("")


@assoc.command()
@click.argument("folder_path")
@click.option(
    "--description",
    prompt="Description of the folder",
    help="Associate this folder with a certain kind of files.",
)
def add(folder_path: str, description: str):
    """Add a folder association."""
    _add(folder_path, description)


@assoc.command()
@click.argument("folder_path")
def remove(folder_path: str):
    """Remove a folder association."""
    _remove(folder_path)


@assoc.command(name="list")
def list_assoc():
    """List folder associations."""
    _list_assoc()
