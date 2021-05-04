from ..._base import APIQueryBase
from ....config import config
from .... import schema

class APIQuery(APIQueryBase):
    @property
    def botarcapi_uri(self) -> str:
        if not config.BOTARCAPI_URI:
            raise ValueError('Using Botarcapi query without setting a URI')
        return config.BOTARCAPI_URI

    async def userinfo(self, with_recent: bool = True) -> schema.UserInfo:
        raise NotImplementedError

    async def best30(self) -> schema.UserBest30:
        raise NotImplementedError
