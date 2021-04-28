from typing import Any

from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State

from ..config import config
from ..matcher import arc
from .. import schema, api


async def recent_handler(bot: Bot, event: MessageEvent, state: T_State) -> Any:
    cmd = state['cmd']
    current_user: schema.User = state['current_user']
    if cmd in config.CMDA_RECENT:
        if not current_user.code:
            raise ValueError
        userinfo = await api.query.userinfo(current_user.code, with_recent=True)
        if current_user.recent_type == 'text':
            await arc.send('\n'.join((
                f"name: {userinfo.name}",
                f"rating: {userinfo.rating}",
                f"最近游玩: {userinfo.recent_score}"
            )))
        else:
            await arc.send('this_is_recent.jpg')
        await arc.finish()
        return
