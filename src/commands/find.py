import click

import api.find


@click.command()
@click.argument("query")
def find(query: str):
    """Semantic search for files using a QUERY string and return file paths."""
    res, err = api.find.find(query)

    if err:
        raise click.ClickException(err)
    if len(res) == 0:
        click.echo(f"No files found that matches the query '{query}'")
    else:
        for r in res:
            click.echo(f"{r.get('path')}: {r.get('summary')}\n")
