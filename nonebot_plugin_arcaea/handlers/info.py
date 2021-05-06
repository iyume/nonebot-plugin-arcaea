from typing import Any
from time import time

from nonebot.adapters.cqhttp import Bot
from nonebot.typing import T_State
from nonebot.log import logger

from ..config import config
from ..matcher import arc
from .. import schema
from ..api import ArcApiPlus
from ..messages import ArcMessage


async def info_handler(bot: Bot, state: T_State) -> Any:
    cmd = state['cmd']
    current_user: schema.User = state['current_user']
    if cmd in config.CMDA_INFO:
        if not current_user.code:
            raise ValueError
        api = ArcApiPlus(current_user.code)
        query_start_time = time()
        try:
            userinfo = await api.userinfo(with_recent=False)
        except Exception as e:
            logger.error(str(e))
            await arc.finish('查询失败', at_sender=True)
            return
        query_end_time = time()
        userinfo_msg = ArcMessage.text(userinfo)
        send_msg = userinfo_msg + f"\n查询耗时: {query_end_time - query_start_time:.2f}s"
        await arc.finish('Info 查询结果\n' + send_msg, at_sender=True)
        return
