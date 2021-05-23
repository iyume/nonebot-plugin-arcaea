from typing import Any, Optional
from time import time

from nonebot.adapters.cqhttp import Bot
from nonebot.typing import T_State
from nonebot.log import logger

from ..config import config
from ..matcher import arc
from ..api import Botarcapi
from ..messages import ArcMessage
from .. import schema
from ..exceptions import HTTPException


async def songinfo_handler(bot: Bot, state: T_State) -> Any:
    cmd = state['cmd']
    current_user: schema.User = state['current_user']
    if cmd in config.CMDA_BEST:
        if not current_user.code:
            raise ValueError
        try:
            songname: Optional[str] = state['argv'][1]
        except IndexError:
            songname = None
        try:
            difficulty_in: str = state['argv'][2]
            difficulty: Optional[int] = {
                'pst': 0, 'prs': 1, 'ftr': 2, 'byd': 3, 'byn': 3}.get(difficulty_in.lower())
        except IndexError:
            difficulty = None
        if songname is None:
            await arc.finish('请在命令后输入歌曲名')
            return
        api = Botarcapi(current_user.code)
        query_start_time = time()
        try:
            songscore = await api.userbest(songname, difficulty or 2)
        except HTTPException as e:
            logger.error(e.detail)
            await arc.finish('服务器连接失败', at_sender=True)
            return
        except Exception as e:
            logger.error(str(e))
            await arc.finish('查询失败~', at_sender=True)
            return
        query_end_time = time()
        songscore_msg = ArcMessage.text(songscore)
        send_msg = songscore_msg + f"\n查询耗时: {query_end_time - query_start_time:.2f}s"
        await arc.finish('Best 查询结果\n' + send_msg, at_sender=True)
        return
