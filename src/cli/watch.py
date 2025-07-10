import click

import api.watch


@click.group()
def watch():
    """Configure watch folders."""
    pass


@watch.command()
@click.argument(
    "folder_path", type=click.Path(exists=True, file_okay=False, resolve_path=True)
)
def add(folder_path):
    """Add a watch folder."""
    _, err = api.watch.add(folder_path)
    if err:
        raise click.ClickException(err)


@watch.command()
@click.argument("folder_path", type=click.Path(file_okay=False, resolve_path=True))
def remove(folder_path):
    """Remove a watch folder."""
    _, err = api.watch.remove(folder_path)
    if err:
        raise click.ClickException(err)


@watch.command(name="list")
def list_watch():
    """List watch folders."""
    paths = api.watch.list()
    if not paths:
        click.echo("No watch paths configured.")
    else:
        for path in paths:
            click.echo(path)
