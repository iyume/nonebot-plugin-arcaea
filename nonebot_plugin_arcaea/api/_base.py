import abc
from typing import Optional

from .. import schema


class APIQueryBase(abc.ABC):
    """
    包含所有可用的查询方法
    """
    code: str  # Arcaea Code

    def __init__(self, code: str) -> None:
        self.code = code

    async def userbest(self, songname: str, difficulty: int) -> schema.SongScore:
        """
        Search and return the best score that the user has submitted to the server.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def userbest30(self) -> schema.UserBest30:
        """
        Search and calculate user best30 table and recent 10 average.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def userinfo(self, *, with_recent: bool) -> schema.UserInfo:
        """
        Search and return user info.
        """
        raise NotImplementedError

    @staticmethod
    async def songalias(songid: str) -> list[str]:
        """
        Return all of the aliases about this song.
        """
        raise NotImplementedError

    @staticmethod
    async def songinfo(song_id: str) -> schema.SongInfo:
        """
        Search and return the song info.
        """
        raise NotImplementedError

    @staticmethod
    async def songrandom(start: Optional[int] = None,
                        end: Optional[int] = None) -> schema.SongRandom:
        """
        Return all the song ids who matched the given rating range.
        如果给予一个参数 n，则查询 [n, n + 1) 范围的歌曲
        """
        raise NotImplementedError

    @staticmethod
    async def songrating(start: int,
                        end: Optional[int] = None) -> schema.SongRating:
        """
        Return all the song ids who matched the given rating range.
        如果给予一个参数 n，则查询 [n, n + 1) 范围的歌曲
        """
        raise NotImplementedError
