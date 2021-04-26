from nonebot.plugin import on_shell_command

from .config import config
from .models import Rule, Parser
from . import handlers


arc = on_shell_command(
    cmd=config.CMD,
    aliases=config.ALIASES,
    rule=Rule(),
    parser=Parser()
)

arc.handle()(handlers.pre_handler)
arc.handle()(handlers.help_handler)
arc.handle()(handlers.bind_handler)
arc.handle()(handlers.auth_handler)
