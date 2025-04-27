import click
import click
import importlib
import pkgutil
import commands


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")


@click.group()
def cli():
    """Munchkin CLI."""
    pass


# Dynamically load all commands
def _register_commands():
    package = commands
    for loader, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{package.__name__}.{module_name}")
        if hasattr(module, module_name):
            cmd = getattr(module, module_name)
            cli.add_command(cmd)


_register_commands()

if __name__ == "__main__":
    cli()
