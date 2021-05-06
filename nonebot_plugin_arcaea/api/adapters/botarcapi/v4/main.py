from ...._base import APIQueryBase
from .....config import config
from ..... import schema
from ....exceptions import HTTPException
from . import _call_api as call_api


def data_status_checker(status_code: int) -> None:
    if status_code == 0:
        return
    raise HTTPException(status_code=status_code, detail={
        -1: 'invalid username or usercode',
        -2: 'invalid usercode'
    }.get(status_code, None))
    # 报错信息参照 https://github.com/TheSnowfield/BotArcAPI/wiki/


class APIQuery(APIQueryBase):
    @property
    def botarcapi_uri(self) -> str:
        if not config.BOTARCAPI_URI:
            raise ValueError('Using Botarcapi query without setting a URI')
        return config.BOTARCAPI_URI

    async def userbest(self, songname: str, difficulty: int) -> schema.SongScore:
        recv = await call_api.userbest(self.code, songname, difficulty)
        data_status_checker(recv['status'])
        return schema.SongScore(**recv['content'])

    async def userbest30(self) -> schema.UserBest30:
        recv = await call_api.userbest30(self.code)
        data_status_checker(recv['status'])
        return schema.UserBest30(**recv['content'])

    async def userinfo(self, with_recent: bool = True) -> schema.UserInfo:
        recv = await call_api.userinfo(self.code, recent=with_recent)
        data_status_checker(recv['status'])
        return schema.UserInfo(**recv['content'])

    @staticmethod
    async def songinfo(songname: str) -> schema.SongInfo:
        recv = await call_api.songinfo(songname)
        data_status_checker(recv['status'])
        return schema.SongInfo(**recv['content'])
