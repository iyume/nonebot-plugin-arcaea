from typing import Dict

from httpx import Response

from ._base import APIQueryBase
from .adapters.estertion import APIQuery as Estertion
from .adapters.botarcapi import APIQuery as Botarcapi
from ..config import config
from .. import schema
from .exceptions import HTTPException


class QueryResolver(object):
    """
    根据配置的 arcaea_query_config 来选择每个命令的查分源
    """
    @property
    def query_config(self) -> Dict[str, APIQueryBase]:
        query_config: Dict[str, APIQueryBase] = {
            key: {
                'estertion': self.estertion,
                'botarcapi': self.botarcapi
            }[val]
            for key, val in config.QUERY_CONFIG.items()
        }
        return query_config

    def __init__(self, code: str) -> None:
        super().__init__()
        self.code = code
        self.estertion = Estertion(code)
        self.botarcapi = Botarcapi(code)

    async def userinfo(self, with_recent: bool) -> schema.UserInfo:
        api = self.query_config['userinfo']
        return await api.userinfo(with_recent=with_recent)

    async def userbest30(self) -> schema.UserBest30:
        api = self.query_config['best30']
        return await api.userbest30()

    async def songinfo(self, song_id: str) -> schema.SongInfo:
        api = self.query_config['songinfo']
        return await api.songinfo(song_id)


def http_status_handler(response: Response) -> None:
    status_code = response.status_code
    if status_code == 200:
        return
    exception = HTTPException(
        status_code=status_code, detail={
            400: 'Bad request',
            403: 'Forbidden',
            404: 'Page not found',
            422: 'Validation error'
        }.get(status_code)
    )
    raise exception
