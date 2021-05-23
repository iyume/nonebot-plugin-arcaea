from nonebot.plugin import on_shell_command

from .config import config
from .models import Rule, Parser


arc = on_shell_command(
    cmd=config.CMD,
    aliases=set(map(lambda x: x + ' ', config.ALIASES)),
    # 空格旨在防止命令重叠，主要由于 nb 允许命令和第一个参数之间不留空格
    rule=Rule(),
    parser=Parser()
)
