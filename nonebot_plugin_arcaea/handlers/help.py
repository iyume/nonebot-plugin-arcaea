from typing import Any

from nonebot.adapters.cqhttp import Bot
from nonebot.typing import T_State

from ..config import config
from ..matcher import arc


async def help_handler(bot: Bot, state: T_State) -> Any:
    cmd = state['cmd']
    if cmd in config.CMDA_HELP:
        await arc.finish('\n\n'.join((
            "Arcaea 查分命令皆以 \"/arc\" 开头",
            "/arc help 帮助文档",
            "/arc bind 绑定账户",
            "/arc info 查询个人信息，需绑定账户，返回 文字",
            "/arc recent 查询最近游玩，返回 文字 / 图片",
            "/arc b30 查询玩家 best30，返回 文字 / 图片",
            "/arc songinfo 查询歌曲信息，返回 文字，无需注册",
            "/arc config 配置用户信息，可选 config.{$b30} / config.{$recent}",
            "/arc current-config 查询用户配置信息"
        )))
        return
