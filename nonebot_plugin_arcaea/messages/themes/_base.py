import abc

from nonebot.adapters.cqhttp.message import MessageSegment

from ... import schema


class ThemeBase(abc.ABC):
    """
    定义了一个 theme 包需要有的抽象行为，便于编写自定义主题
    """
    @staticmethod
    @abc.abstractmethod
    def recent(obj_in: schema.UserInfo) -> MessageSegment:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def best30(obj_in: schema.UserBest30) -> MessageSegment:
        raise NotImplementedError
