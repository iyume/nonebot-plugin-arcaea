from typing import Any

from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State

from ..config import config
from ..matcher import arc
from .. import schema, api


async def recent_handler(bot: Bot, event: MessageEvent, state: T_State) -> Any:
    cmd = state['cmd']
    current_user: schema.User = state['current_user']
    if cmd in config.CMDA_RECENT:
        if not current_user.code:
            raise ValueError
        userinfo = await api.query.userinfo(current_user.code, with_recent=True)
        recent = userinfo.recent_score
        if not recent:
            raise RuntimeError
        if current_user.recent_type == 'text':
            await arc.send('\n'.join((
                f"name: {userinfo.name}",
                f"PTT: {userinfo.rating}",
                f'最近游玩: {recent.song_id}',
                f'难度: {recent.difficulty}',
                f'Score: {recent.score}',
                f'PTT: {recent.rating:.2f}',
                f'大P: {recent.shiny_perfect_count}',
                f'小P: {recent.perfect_count - recent.shiny_perfect_count}',
                f'count P: {recent.perfect_count}',
                f'count FAR: {recent.near_count}',
                f'count MISS: {recent.miss_count}',
                f'Time: {recent.time_played}'
            )))
        else:
            await arc.send('this_is_recent.jpg')
        await arc.finish()
        return
