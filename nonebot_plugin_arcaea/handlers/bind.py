from typing import Any
from contextlib import closing

from nonebot.adapters.cqhttp import Bot
from nonebot.typing import T_State

from ..config import config
from ..db import get_db
from .. import schema, crud
from ..matcher import arc


async def bind_handler(bot: Bot, state: T_State) -> Any:
    cmd: str = state['cmd']
    qq: int = state['qq']
    current_user: schema.User = state['current_user']
    db = get_db()
    if cmd in config.CMDA_BIND:
        try:
            code: str = state['argv'][1]
        except:
            await arc.finish('请带上 Arcaea Code 绑定', at_sender=True)
            return
        if len(code) != 9 or not code.isnumeric():
            await arc.finish('Code 不合法', at_sender=True)
            return
        with closing(db.cursor()) as cursor:
            if current_user:
                # 存在用户则更新 Code
                crud.user.update(cursor, qq, code=code)
                await arc.send('绑定更新成功', at_sender=True)
            else:
                # 不存在则创建
                crud.user.create(cursor, qq, code=code)
                await arc.send('绑定创建成功', at_sender=True)
        await arc.finish()
        return
