from typing import Any

from .. import schema


async def format_songdb(r: Any) -> Any:
    return r['data']


async def format_recent(r: Any) -> schema.UserInfo:
    _recent = r['data']['recent_score'][0]
    return _recent


async def format_b30(r: Any) -> schema.UserBest30:
    return r
