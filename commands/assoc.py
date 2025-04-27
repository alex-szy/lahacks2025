import click
from utilities.file_system_config import FileSystemConfig


@click.group()
def assoc():
    """Configure destination folder associations."""
    pass


@assoc.command()
@click.argument('folder_path')
@click.argument('description')
def add(folder_path, description):
    """Add a folder association."""
    cfg = FileSystemConfig()
    cfg.append_entry(folder_path, description)
    print(f"Sucessfully added: {folder_path}, {description}")


@assoc.command()
@click.argument('folder_path')
def remove(folder_path):
    """Remove a folder association."""
    cfg = FileSystemConfig()
    cfg.remove_entry(folder_path)


@assoc.command(name="list")
def list_assoc():
    """List folder associations."""
    cfg = FileSystemConfig()
    path_list = cfg.read_all_entries()

    print("Existing Paths:\n")
    for path, info in path_list.items():
        print(path)
        print(info)
        print("")

