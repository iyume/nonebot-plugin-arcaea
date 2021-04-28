from typing import Any

from nonebot.adapters.cqhttp import Bot
from nonebot.typing import T_State

from ..config import config
from ..matcher import arc
from .. import api, schema


async def info_handler(bot: Bot, state: T_State) -> Any:
    cmd = state['cmd']
    current_user: schema.User = state['current_user']
    if cmd in config.CMDA_INFO:
        if not current_user.code:
            raise ValueError
        userinfo = await api.query.userinfo(current_user.code, with_recent=False)
        await arc.send('\n'.join((f"name: {userinfo.name}", f"rating: {userinfo.rating}")))
        await arc.finish()
        return
