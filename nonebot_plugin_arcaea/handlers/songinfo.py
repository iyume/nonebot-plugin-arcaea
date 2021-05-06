from typing import Any, Optional

from nonebot.adapters.cqhttp import Bot
from nonebot.typing import T_State
from nonebot.log import logger

from ..config import config
from ..matcher import arc
from ..api import Botarcapi
from ..messages import ArcMessage


async def songinfo_handler(bot: Bot, state: T_State) -> Any:
    cmd = state['cmd']
    if cmd in config.CMDA_SONGINFO:
        try:
            songname: Optional[str] = state['argv'][1]
        except IndexError:
            songname = None
        if songname is None:
            await arc.finish('请在命令后输入歌曲名')
            return
        try:
            songinfo = await Botarcapi.songinfo(songname)
        except Exception as e:
            logger.error(str(e))
            await arc.finish('查询失败', at_sender=True)
            return
        songinfo_msg = ArcMessage.text(songinfo)
        send_msg = songinfo_msg
        await arc.finish('SongInfo 查询结果\n' + send_msg, at_sender=True)
        return
