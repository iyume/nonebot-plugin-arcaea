from typing import Any

from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State

from .. import schema


async def auth_handler(bot: Bot, event: MessageEvent, state: T_State) -> Any:
    current_user: schema.User = state['current_user']
    if not current_user or not current_user.code:
        await bot.send(event, '尚未注册')
        return
