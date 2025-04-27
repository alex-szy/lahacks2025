import click


@click.group()
def assoc():
    """Configure destination folder associations."""
    pass


@assoc.command()
@click.argument('folder_path')
@click.argument('description')
def add(folder_path, description):
    """Add a folder association."""
    pass


@assoc.command()
def remove():
    """Remove a folder association."""
    pass


@assoc.command(name="list")
def list_assoc():
    """List folder associations."""
    pass
