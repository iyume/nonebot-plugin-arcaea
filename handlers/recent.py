from typing import Any

from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State

from ..config import config


async def recent_handler(bot: Bot, event: MessageEvent, state: T_State) -> Any:
    cmd = state['cmd']
    if cmd in config.CMDA_RECENT:
        await bot.send(event, 'help')
        return
