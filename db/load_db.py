from typing import Any
import sqlite3
from typing import Generator

from ..config import config


def dict_factory(cursor: Any, row: Any) -> Any:
    # make query return with dict
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


conn = sqlite3.connect(config.SQLITE_DATABASE_URI)
conn.row_factory = dict_factory


def get_db() -> Generator:
    cursor: Any = None  # break pylance error
    try:
        cursor = conn.cursor()
        yield cursor
    finally:
        cursor.close()
        conn.commit()
