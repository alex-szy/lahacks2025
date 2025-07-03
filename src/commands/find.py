import requests
import logging

import click

from settings import settings


def _find(query: str) -> tuple[list[dict], str | None]:
    try:
        res = requests.get(
            f"http://localhost:{settings.get_daemon_port()}/query", {"query": query}
        )
        logging.info(f"Find request returned response: {res.text}")
        return res.json(), None
    except requests.ConnectionError:
        return (
            [],
            "Can't connect to the munchkin server. Is it running? Run mckn start to start it if you haven't.",
        )


@click.command()
@click.argument("query")
def find(query: str):
    """Semantic search for files using a QUERY string and return file paths."""
    res, err = _find(query)

    if err:
        raise click.ClickException(err)
    if len(res) == 0:
        click.echo(f"No files found that matches the query '{query}'")
    else:
        for r in res:
            click.echo(f"{r.get('path')}: {r.get('summary')}\n")
