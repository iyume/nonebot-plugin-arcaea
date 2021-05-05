from typing import Any, Optional
from contextlib import closing

from nonebot.adapters.cqhttp import Bot
from nonebot.typing import T_State

from ..config import config
from .. import schema, crud
from ..matcher import arc
from ..db import get_db


def validate_value(s: str) -> bool:
    return s in ['text', 'pic']


async def userconfig_handler(bot: Bot, state: T_State) -> Any:
    cmd: str = state['cmd']
    current_user: schema.User = state['current_user']
    if cmd.startswith('config'):
        try:
            config_item = cmd.split('.')[1]
        except IndexError:
            await arc.finish('可选配置\nconfig.recent\nconfig.b30')
            return
        try:
            config_val: Optional[str] = state['argv'][1]
        except IndexError:
            config_val = None
        if config_item in config.CMDA_RECENT:
            if config_val is None or config_val == 'list':
                await arc.finish('可用的值\n' + '\n'.join(config.AVAILABLE_USER_CONFIG))
                return
            if config_val in config.AVAILABLE_USER_CONFIG:
                with closing(get_db().cursor()) as cursor:
                    crud.user.update(cursor, current_user.qq, recent_type=config_val)
                await arc.finish('更新成功', at_sender=True)
                return
            else:
                await arc.finish('目标值不可用', at_sender=True)
                return
        if config_item in config.CMDA_B30:
            if config_val is None or config_val == 'list':
                await arc.finish('可用的值\n' + '\n'.join(config.AVAILABLE_USER_CONFIG))
                return
            if config_val in config.AVAILABLE_USER_CONFIG:
                with closing(get_db().cursor()) as cursor:
                    crud.user.update(cursor, current_user.qq, best30_type=config_val)
                await arc.finish('更新成功', at_sender=True)
                return
            else:
                await arc.finish('目标值不可用', at_sender=True)
                return
        await arc.finish('无此配置项', at_sender=True)
        return
    if cmd == 'current-config':
        await arc.finish(
            f"当前配置\nconfig.recent: {current_user.recent_type}\nconfig.b30: {current_user.b30_type}",
            at_sender=True)
        return
