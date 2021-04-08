from typing import Any

from .. import schema


async def format_songname_table(r: Any) -> Any:
    return r['data']


async def format_recent(r: Any) -> schema.Recent:
    _recent = r['data']['recent_score'][0]
    return _recent


async def format_b30(r: schema.Best30) -> schema.Best30:
    return r
