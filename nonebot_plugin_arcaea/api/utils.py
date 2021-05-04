from typing import Dict

from ._base import APIQueryBase
from .adapters.estertion import APIQuery as Estertion
from .adapters.botarcapi import APIQuery as Botarcapi
from ..config import config
from .. import schema


class QueryResolver(object):
    """
    根据配置的 arcaea_query_config 来选择每个命令的查分源
    """
    @property
    def query_config(self) -> Dict[str, APIQueryBase]:
        query_config: Dict[str, APIQueryBase] = {
            key: {
                'estertion': Estertion(self.code),
                'botarcapi': Botarcapi(self.code)
            }[val]
            for key, val in config.QUERY_CONFIG.items()
        }
        return query_config

    def __init__(self, code: str) -> None:
        super().__init__()
        self.code = code

    async def userinfo(self, with_recent: bool = True) -> schema.UserInfo:
        api = self.query_config['userinfo']
        return await api.userinfo(with_recent=with_recent)

    async def best30(self) -> schema.UserBest30:
        api = self.query_config['best30']
        return await api.best30()

    async def songinfo(self, song_id: str) -> schema.SongInfo:
        api = self.query_config['songinfo']
        return await api.songinfo(song_id)
