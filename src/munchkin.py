import importlib
import logging
import pkgutil

import click

import cli
from settings import BASE_DIR

logging.basicConfig(
    filename=BASE_DIR / "munchkin.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@click.group()
def main():
    """Munchkin CLI."""
    pass


# Dynamically load all commands
def _register_commands():
    package = cli
    for loader, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{package.__name__}.{module_name}")
        if hasattr(module, module_name):
            cmd = getattr(module, module_name)
            main.add_command(cmd)


_register_commands()

if __name__ == "__main__":
    main()
