from typing import Union

from nonebot.adapters.cqhttp.message import MessageSegment

from .. import schema
from .themes.utils import import_theme
from .themes._base import ThemeBase


class Message(object):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def text(obj_in: Union[
        schema.UserInfo, schema.UserBest30, schema.SongInfo
    ]) -> MessageSegment:
        if isinstance(obj_in, schema.UserInfo):
            info_msg = '\n'.join((
                f"name: {obj_in.name}",
                f"PTT: {obj_in.rating}"))
            recent = obj_in.recent_score
            recent_msg = '\n'.join((
                f"最近游玩: {recent.song_id}",
                f"难度: {recent.difficulty}",
                f"Score: {recent.score}",
                f"PTT: {recent.rating:.2f}",
                f"大 P: {recent.shiny_perfect_count}",
                f"小 P: {recent.perfect_count - recent.shiny_perfect_count}",
                f"count P: {recent.perfect_count}",
                f"count FAR: {recent.near_count}",
                f"count MISS: {recent.miss_count}",
                f"Time: {recent.time_played:%F %X}"
            )) if recent else None
            msg = '\n'.join([x for x in [info_msg, recent_msg] if isinstance(x, str)])
            return MessageSegment.text(msg)
        if isinstance(obj_in, schema.UserBest30):
            raise NotImplementedError
        if isinstance(obj_in, schema.SongInfo):
            raise NotImplementedError

    @staticmethod
    def image(
        obj_in: Union[schema.UserInfo, schema.UserBest30],
        theme_name: str
    ) -> MessageSegment:
        try:
            themer: ThemeBase = import_theme(theme_name)
        except:
            raise ImportError(f"theme '{theme_name}' not found")
        if isinstance(obj_in, schema.UserInfo):
            return themer.recent(obj_in)
        if isinstance(obj_in, schema.UserBest30):
            return themer.best30(obj_in)
