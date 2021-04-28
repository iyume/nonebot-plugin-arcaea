from typing import Any
from time import time

from nonebot.adapters.cqhttp import Bot
from nonebot.typing import T_State

from ..config import config
from .. import schema, api
from ..matcher import arc


async def b30_handler(bot: Bot, state: T_State) -> Any:
    cmd = state['cmd']
    current_user: schema.User = state['current_user']
    if cmd in config.CMDA_B30:
        if not current_user.code:
            raise ValueError
        query_start_time = time()
        best30 = await api.query.best30(current_user.code)
        query_end_time = time()
        await arc.finish()
        return
