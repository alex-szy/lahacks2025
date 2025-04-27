import click
import os
from utilities.file_system_config import FileSystemConfig
from daemon import service
from commands.start import _start


@click.group()
def assoc():
    """Configure destination folder associations."""
    pass


def _add(folder_path, description):
    cfg = FileSystemConfig()
    cfg.append_entry(os.path.normpath(folder_path), description)
    click.echo(f"Sucessfully added: {folder_path}, {description}")
    service.stop()
    _start()


def _remove(folder_path):
    cfg = FileSystemConfig()
    cfg.remove_entry(os.path.normpath(folder_path))
    service.stop()
    _start()


def _list_assoc():
    cfg = FileSystemConfig()
    path_list = cfg.read_all_entries()

    click.echo("Existing Paths:\n")
    for path, info in path_list.items():
        click.echo(path)
        click.echo(info)
        click.echo("")


@assoc.command()
@click.argument('folder_path')
@click.option('--description', prompt="Description of the folder", help="Associate this folder with a certain kind of files.")
def add(folder_path, description):
    """Add a folder association."""
    _add(folder_path, description)


@assoc.command()
@click.argument('folder_path')
def remove(folder_path):
    """Remove a folder association."""
    _remove(folder_path)


@assoc.command(name="list")
def list_assoc():
    """List folder associations."""
    _list_assoc()
