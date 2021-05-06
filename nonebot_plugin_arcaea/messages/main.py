from typing import Union

from nonebot.adapters.cqhttp.message import MessageSegment

from .. import schema
from .themes.utils import import_theme
from .themes._base import ThemeBase


class ArcMessage(object):
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
            def songscore_msg(s: schema.SongScore) -> str:
                return '\n'.join((
                    f"{s.song_id} {s.difficulty}",
                    f"  Score: {s.score}",
                    f"  PTT: {s.rating:.2f}"
                ))
            info_msg = '\n'.join((
                f"b30_avg: {obj_in.best30_avg}",
                f"r10_avg: {obj_in.recent10_avg}"
            ))
            songs_msg = '\n'.join(
                f"{i + 1}: {val}" for i, val in enumerate(
                    map(songscore_msg, obj_in.best30_list)))
            msg = '\n'.join((info_msg, songs_msg))
            return MessageSegment.text(msg)
        if isinstance(obj_in, schema.SongInfo):
            def songinfo_perlevel(s: schema.SongInfoPerLevel) -> str:
                return '\n'.join((
                    f"- 难度: {s.ratingClass}",
                    f"  等级: {s.rating}{'+' if s.ratingPlus else ''}",
                    f"  定数: {s.ratingReal}",
                    f"  物量: {s.totalNotes}"
                ))
            info_msg = '\n'.join((
                f"song_id: {obj_in.id}",
                f"artist: {obj_in.artist}",
                f"bpm: {obj_in.bpm}",
                f"date: {obj_in.date:%F %X}"
            ))
            levels_msg = '\n'.join(map(songinfo_perlevel, obj_in.difficulties))
            msg = '\n'.join((info_msg, levels_msg))
            return MessageSegment.text(msg)

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
