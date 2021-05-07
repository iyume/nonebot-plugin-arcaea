from typing import Any
from time import time

from nonebot.adapters.cqhttp import Bot
from nonebot.typing import T_State
from nonebot.log import logger

from ..config import config
from .. import schema
from ..matcher import arc
from ..api import ArcApiPlus
from ..messages import ArcMessage


async def b30_handler(bot: Bot, state: T_State) -> Any:
    cmd = state['cmd']
    current_user: schema.User = state['current_user']
    if cmd in config.CMDA_B30:
        if not current_user.code:
            raise ValueError
        api = ArcApiPlus(current_user.code)
        query_start_time = time()
        try:
            userbest30 = await api.userbest30()
        except Exception as e:
            logger.error(str(e))
            await arc.finish('查询失败', at_sender=True)
            return
        query_end_time = time()
        if current_user.b30_type == 'text':
            userbest30_msg = ArcMessage.text(userbest30)
            send_msg = userbest30_msg + f"\n查询耗时: {query_end_time - query_start_time:.2f}s"
            await arc.finish('B30 查询结果\n' + send_msg, at_sender=True)
            return
        else:
            userbest30_msg = ArcMessage.image(userbest30, theme_name=current_user.b30_type)
            send_msg = userbest30_msg + f"\n查询耗时: {query_end_time - query_start_time:.2f}s"
            await arc.finish('B30 查询结果\n' + send_msg, at_sender=True)
            return
