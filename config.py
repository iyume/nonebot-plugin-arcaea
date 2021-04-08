from typing import Optional

import nonebot


class Config():
    _config = nonebot.get_driver().config

    ARCAEA_API_TYPE: Optional[str] = _config.arcaea_api_type
    ARCAEA_API_URI: Optional[str] = _config.arcaea_api_uri

    ESTERTION_URI = 'wss://arc.estertion.win:616'

    TIMEOUT = 8

    HIGHEST_SONG_CONSTANT = 11.5  # 目前最高歌曲定数（风暴byd）

    @property
    def estertion_uri(self) -> str:
        return self.ESTERTION_URI

    @property
    def botarcapi_uri(self) -> Optional[str]:
        return self.ARCAEA_API_URI if self.ARCAEA_API_TYPE == 'botarcapi' else None


config = Config()
