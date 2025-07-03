from typing import List
import requests

import click

from engine.db.models import File
from settings import settings


def _find(query: str) -> List[File]:
    try:
        res = requests.get(
            f"http://localhost:{settings.get_daemon_port()}/query", {query: query}
        )
        return res.json()
    except requests.ConnectionError:
        return []


@click.command()
@click.argument("query")
def find(query: str):
    """Semantic search for files using a QUERY string and return file paths."""
    res = _find(query)

    for r in res:
        click.echo(f"{r.path}: {r.summary}")
