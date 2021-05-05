from typing import Any

from nonebot.adapters.cqhttp import Bot
from nonebot.typing import T_State

from .. import schema
from ..matcher import arc


async def auth_handler(bot: Bot, state: T_State) -> Any:
    """
    阻断查分命令
    """
    current_user: schema.User = state['current_user']
    if not current_user or not current_user.code:
        await arc.finish('尚未绑定 Arcaea Code', at_sender=True)
        return
