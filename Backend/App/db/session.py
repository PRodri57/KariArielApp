from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine

from App.Core.config import settings

engine: Engine = create_engine (
    settings.database_url,
    pool_pre_ping = True,
)

@contextmanager
def get_connection() -> Iterator[Connection]:
    with engine.connect() as conn:
        yield conn