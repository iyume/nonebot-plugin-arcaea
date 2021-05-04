import abc

from .. import schema


class APIQueryBase(abc.ABC):
    """
    包含所有可用的查询方法
    """
    def __init__(self, code: str) -> None:
        self.code = code

    @abc.abstractmethod
    async def userinfo(self, *, with_recent: bool = True) -> schema.UserInfo:
        raise NotImplementedError

    @abc.abstractmethod
    async def best30(self) -> schema.UserBest30:
        raise NotImplementedError

    @staticmethod
    async def songname(song_id: str) -> str:
        raise NotImplementedError

    @staticmethod
    async def songinfo(song_id: str) -> schema.SongInfo:
        raise NotImplementedError
