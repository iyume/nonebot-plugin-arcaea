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
    def __init__(self, code: str) -> None:
        super().__init__()
        self.code = code
        self.estertion = Estertion(code)
        self.botarcapi = Botarcapi(code)
        self.query_config: Dict[str, APIQueryBase] = {
            key: {
                'estertion': self.estertion,
                'botarcapi': self.botarcapi
            }[val]
            for key, val in config.QUERY_CONFIG.items()
        }

    async def userinfo(self, with_recent: bool) -> schema.UserInfo:
        api = self.query_config['userinfo']
        return await api.userinfo(with_recent=with_recent)

    async def userbest30(self) -> schema.UserBest30:
        api = self.query_config['best30']
        return await api.userbest30()

    async def songinfo(self, song_id: str) -> schema.SongInfo:
        api = self.query_config['songinfo']
        return await api.songinfo(song_id)
