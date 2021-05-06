from nonebot.adapters.cqhttp.message import MessageSegment

from ..... import schema
from ..._base import ThemeBase


class Theme(ThemeBase):
    @staticmethod
    def recent(obj_in: schema.UserInfo) -> MessageSegment:
        raise NotImplementedError

    @staticmethod
    def best30(obj_in: schema.UserBest30) -> MessageSegment:
        raise NotImplementedError
