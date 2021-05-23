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
from ..exceptions import HTTPException


async def recent_handler(bot: Bot, state: T_State) -> Any:
    cmd = state['cmd']
    current_user: schema.User = state['current_user']
    if cmd in config.CMDA_RECENT:
        if not current_user.code:
            raise ValueError
        api = ArcApiPlus(current_user.code)
        query_start_time = time()
        try:
            userinfo = await api.userinfo(with_recent=True)
        except HTTPException as e:
            logger.error(e.detail)
            await arc.finish('服务器连接失败', at_sender=True)
            return
        except Exception as e:
            logger.error(str(e))
            await arc.finish('查询失败~', at_sender=True)
            return
        query_end_time = time()
        if current_user.recent_type == 'text':
            userinfo_msg = ArcMessage.text(userinfo)
            send_msg = userinfo_msg + f"\n查询耗时: {query_end_time - query_start_time:.2f}s"
            await arc.finish('Recent 查询结果\n' + send_msg, at_sender=True)
            return
        else:
            await arc.finish('this_is_recent.jpg')
            return
