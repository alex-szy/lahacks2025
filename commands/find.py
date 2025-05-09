import click
import os
from settings import MONGO_URI
from typing import List
from models.file import File
import sys
import contextlib


def _find(query: str) -> List[File]:
    from db.database import VectorDatabase
    from engine.encoder import Encoder
    from engine.queryprocessor import QueryProcessor
    db = VectorDatabase(MONGO_URI)
    qp = QueryProcessor(Encoder(), db=db)

    with contextlib.redirect_stderr(open(os.devnull, "w")):
        res = qp.process_query(query)

    return res


@click.command()
@click.argument('query')
def find(query: str):
    """Semantic search for files using a QUERY string and return file paths."""
    res = _find(query)

    for r in res:
        click.echo(f"{r.path}: {r.summary}")
