from typing import Any

from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State


async def pre_handler(bot: Bot, event: MessageEvent, state: T_State) -> Any:
    state['qq'] = int(event.user_id)
    try:
        cmd = state['argv'][0]
        state['cmd'] = cmd
    except IndexError:
        return
