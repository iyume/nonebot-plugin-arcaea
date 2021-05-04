from typing import Any
from time import time

from nonebot.adapters.cqhttp import Bot
from nonebot.typing import T_State

from ..config import config
from .. import schema
from ..matcher import arc
from ..api import ArcApiPlus


async def b30_handler(bot: Bot, state: T_State) -> Any:
    cmd = state['cmd']
    current_user: schema.User = state['current_user']
    if cmd in config.CMDA_B30:
        if not current_user.code:
            raise ValueError
        api = ArcApiPlus(current_user.code)
        query_start_time = time()
        userbest30 = await api.best30()
        query_end_time = time()
        await arc.finish()
        return
