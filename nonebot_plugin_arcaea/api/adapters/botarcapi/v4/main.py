from ...._base import APIQueryBase
from .....config import config
from ..... import schema
from ....exceptions import HTTPException


def data_status_handler(status_code: int) -> None:
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

    async def userinfo(self, with_recent: bool = True) -> schema.UserInfo:
        raise NotImplementedError

    async def userbest30(self) -> schema.UserBest30:
        raise NotImplementedError
