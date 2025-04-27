import click
from frontend.ui.main_window import main


@click.command()
def gui():
    """Starts the gui of the application"""
    main()
