import sqlite3
from sqlite3 import Connection
from typing import Any

from ..config import config


def dict_factory(cursor: Any, row: Any) -> Any:
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


conn = sqlite3.connect(config.SQLITE_DATABASE_URI, isolation_level=None)
# isolation_level implement auto-commit
conn.row_factory = dict_factory
# make query return with dict


def get_db() -> Connection:
    return conn
