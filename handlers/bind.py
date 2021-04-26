from typing import Any
from contextlib import closing

from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State

from ..config import config
from ..db import get_db
from .. import schema, crud


async def bind_handler(bot: Bot, event: MessageEvent, state: T_State) -> Any:
    cmd: str = state['cmd']
    qq: int = state['qq']
    current_user: schema.User = state['current_user']
    db = get_db()
    if cmd in config.CMDA_BIND:
        try:
            code: str = state['argv'][1]
        except:
            await bot.send(event, '请带上 Arcaea code 绑定')
            return
        if len(code) != 9 or not code.isnumeric():
            await bot.send(event, 'Code 不合法')
            return
        with closing(db.cursor()) as cursor:
            if current_user:
                crud.user.update(cursor, qq, code=code)
            else:
                crud.user.create(cursor, qq, code=code)
        return
