import logging
import requests

from settings import settings


def find(query: str) -> tuple[list[dict], str | None]:
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
