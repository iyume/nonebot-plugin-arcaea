from typing import Union

from nonebot.adapters.cqhttp.message import MessageSegment

from .. import schema


def _text_userinfo(obj_in: schema.UserInfo) -> MessageSegment:
    info_msg = '\n'.join((
        f"name: {obj_in.name}",
        f"PTT: {obj_in.rating}"))
    recent = obj_in.recent_score
    recent_msg = '\n'.join((
        f"最近游玩: {recent.song_id}",
        f"难度: {recent.difficulty}",
        f"Score: {recent.score}",
        f"PTT: {recent.rating:.2f}",
        f"大P: {recent.shiny_perfect_count}",
        f"小P: {recent.perfect_count - recent.shiny_perfect_count}",
        f"count P: {recent.perfect_count}",
        f"count FAR: {recent.near_count}",
        f"count MISS: {recent.miss_count}",
        f"Time: {recent.time_played:%F %X}"
    )) if recent else None
    msg = '\n'.join([x for x in [info_msg, recent_msg] if isinstance(x, str)])
    return MessageSegment.text(msg)


def _text_userbest30(obj_in: schema.UserBest30) -> MessageSegment:
    ...


def _text_songinfo(obj_in: schema.SongInfo) -> MessageSegment:
    ...


def text(
    obj_in: Union[schema.UserInfo, schema.UserBest30, schema.SongInfo]
    ) -> MessageSegment:
    # func: Callable[..., str] = {
    #     schema.UserInfo: _text_userinfo,
    #     schema.UserBest30: _text_userbest30,
    #     schema.SongInfo: _text_songinfo
    # }[obj_in.__class__]
    # return func(obj_in)
    if isinstance(obj_in, schema.UserInfo):
        return _text_userinfo(obj_in)
    if isinstance(obj_in, schema.UserBest30):
        return _text_userbest30(obj_in)
    if isinstance(obj_in, schema.SongInfo):
        return _text_songinfo(obj_in)
