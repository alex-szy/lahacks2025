import click

import api.assoc


@click.group()
def assoc():
    """Configure destination folder associations."""
    pass


@assoc.command()
@click.argument("folder_path")
@click.option(
    "--description",
    prompt="Description of the folder",
    help="Associate this folder with a certain kind of files.",
)
def add(folder_path: str, description: str):
    """Add a folder association."""
    _, err = api.assoc.add(folder_path, description)
    if err:
        raise click.ClickException(err)


@assoc.command()
@click.argument("folder_path")
def remove(folder_path: str):
    """Remove a folder association."""
    _, err = api.assoc.remove(folder_path)
    if err:
        raise click.ClickException(err)


@assoc.command(name="list")
def list_assoc():
    """List folder associations."""
    paths = api.assoc.list()
    if not paths:
        click.echo("No folder path associations configured.")
        return
    for path, info in paths.items():
        click.echo(f"\033[0m{info} \033[93m-> \033[96m{path}")
