from nonebot.plugin import on_shell_command

from .config import config
from .models import Rule, Parser


arc = on_shell_command(
    cmd=config.CMD,
    aliases=config.ALIASES,
    rule=Rule(),
    parser=Parser()
)
