import click
import json
from pathlib import Path
from settings import WATCH_PATHS_FILE
# Path to the watch paths JSON file


def load_watch_paths():
    if WATCH_PATHS_FILE.exists():
        with WATCH_PATHS_FILE.open('r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return []


def save_watch_paths(paths):
    with WATCH_PATHS_FILE.open('w', encoding='utf-8') as f:
        json.dump(paths, f, indent=4)


def is_forbidden(path):
    """Placeholder for forbidden paths logic."""
    # You can define your own forbidden logic here.
    return False


@click.group()
def watch():
    """Configure watch folders."""
    pass


@watch.command()
@click.argument('folder_path', type=click.Path(exists=True, file_okay=False, resolve_path=True))
def add(folder_path):
    """Add a watch folder."""
    folder_path = str(Path(folder_path).resolve())

    if is_forbidden(folder_path):
        click.echo(
            f"Error: The folder '{folder_path}' is forbidden and cannot be added.")
        return

    paths = load_watch_paths()
    if folder_path in paths:
        click.echo(
            f"Notice: The folder '{folder_path}' is already being watched.")
        return

    paths.append(folder_path)
    save_watch_paths(paths)
    click.echo(f"Added folder '{folder_path}' to watch list.")


@watch.command()
@click.argument('folder_path', type=click.Path(file_okay=False, resolve_path=True))
def remove(folder_path):
    """Remove a watch folder."""
    folder_path = str(Path(folder_path).resolve())

    paths = load_watch_paths()
    if folder_path not in paths:
        click.echo(
            f"Notice: The folder '{folder_path}' is not in the watch list.")
        return

    paths.remove(folder_path)
    save_watch_paths(paths)
    click.echo(f"Removed folder '{folder_path}' from watch list.")


@watch.command(name="list")
def list_watch():
    """List watch folders."""
    paths = load_watch_paths()
    if not paths:
        click.echo("No watch folders configured.")
    else:
        for path in paths:
            click.echo(path)
