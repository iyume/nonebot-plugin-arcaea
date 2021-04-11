from . import _call_api
from ...adapters import estertion as formatter
from ... import schema


async def query_songdb() -> dict:
    data = await _call_api.songdb()
    songdb = await formatter.format_songdb(data)
    return songdb


async def query_songname(songid: str) -> str:
    songdb = await query_songdb()
    songname = songdb[songid]['en']  # 有其他语种，后期再写
    return songname


async def query_recent(code: str) -> schema.UserInfo:
    data = await _call_api.recent(code)
    _recent = await formatter.format_recent(data)
    return _recent


async def query_b30(code: str) -> schema.UserBest30:
    data = await _call_api.all(code)
    _b30 = await formatter.format_b30(data)
    return _b30
