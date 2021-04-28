from typing import Any

from nonebot.adapters.cqhttp import Bot
from nonebot.typing import T_State

from ..config import config
from ..matcher import arc


async def help_handler(bot: Bot, state: T_State) -> Any:
    cmd = state['cmd']
    if cmd in config.CMDA_HELP:
        await arc.finish('help')
        return
