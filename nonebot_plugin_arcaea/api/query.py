from typing import Callable, Awaitable

from . import estertion, botarcapi
from ..config import config
from .. import schema


class Query:
    _config = config.ARCAEA_QUERY_CONFIG

    async def userinfo(
        self, code: str, with_recent: bool = True) -> schema.UserInfo:
        return await estertion.query_userinfo(
            code, with_recent=with_recent)

    async def best30(self, code: str) -> schema.UserBest30:
        return await estertion.query_best30(code)


query = Query()
