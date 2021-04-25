from typing import Any

from nonebot.plugin import on_shell_command
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment
from nonebot.typing import T_State
from nonebot.log import logger

from .config import config
from .models import Rule, Parser, Command
from . import commands


arc = on_shell_command(
    cmd=config.CMD,
    aliases=config.ALIASES,
    rule=Rule(),
    parser=Parser()
)

@arc.handle()
async def arc_handle(bot: Bot, event: MessageEvent, state: T_State) -> Any:
    try:
        cmd = state['argv'][0]
    except IndexError:
        await arc.finish()
        return  # break pylance error
    if cmd in commands.bind:
        code = arc.got('code')
        await arc.finish(str(state['argv']))
    await arc.finish(cmd)
