import contextlib
import os
from typing import List

import click

from engine.database import File
from settings import MONGO_URI


def _find(query: str) -> List[File]:
    from engine.database import VectorDatabase
    from engine.encoder import Encoder
    from engine.queryprocessor import QueryProcessor

    db = VectorDatabase(MONGO_URI)
    qp = QueryProcessor(Encoder(), db=db)

    with contextlib.redirect_stderr(open(os.devnull, "w")):
        res = qp.process_query(query)

    return res


@click.command()
@click.argument("query")
def find(query: str):
    """Semantic search for files using a QUERY string and return file paths."""
    res = _find(query)

    for r in res:
        click.echo(f"{r.path}: {r.summary}")
