from typing import Optional, Dict

from pydantic import BaseSettings, validator

import nonebot
from nonebot.log import logger


class Config(BaseSettings):
    _config = nonebot.get_driver().config

    CMD_START = list(_config.command_start)[0]
    CMD_SEP = list(_config.command_sep)[0]

    ARCAEA_API_TYPE: Optional[str] = _config.arcaea_api_type
    # example: 'botarcapi'
    # 可选配置项，作为给 API_URI 赋值的依据

    ARCAEA_API_URI: Optional[str] = _config.arcaea_api_uri
    # example: 'http://127.0.0.1/v3'
    # 可选配置项，关联于 ARCAEA_API_TYPE 配置项，作为获取游玩信息的第二 API，目前只支持 BotArcApi

    ARCAEA_QUERY_CONFIG: Optional[Dict[str, str]] = _config.arcaea_query_config
    """
    - **类型**: ``Optional[Dict[str, str]]``
    - **默认值**:
      {
        "recent": "estertion",
        "best30": "estertion",
        "songinfo": "estertion"
      }

    :说明:

      可选配置项，用于配置命令查分使用的源，此配置项要求填写 ARCAEA_API_TYPE, ARCAEA_API_URI

    :示例:

      {
        "recent":
        "best30": ''  # 由于 estertion 的源查 b30 速度特别快，所以不建议更改此项
      }
    """

    @validator('ARCAEA_QUERY_CONFIG', pre=True)
    def preprocess_arcaea_query_config(
        cls, v: Optional[Dict[str, str]]
    ) -> Optional[Dict[str, Optional[str]]]:
        if not cls.ARCAEA_API_TYPE or not cls.ARCAEA_API_URI or not v:
            return None
        return {
            "recent": v.get('recent', 'estertion'),
            "best30": v.get('best30', 'estertion')
        }

    ESTERTION_URI = 'wss://arc.estertion.win:616'
    """
    获取游玩信息的默认 API，来自 estertion 维护的公开源
    """

    TIMEOUT = 8

    HIGHEST_SONG_CONSTANT = 11.5  # 目前最高歌曲定数（风暴byd）

    # API_URI 填写
    estertion_uri = ESTERTION_URI
    botarcapi_uri = ARCAEA_API_URI if ARCAEA_API_TYPE == 'botarcapi' else None


config = Config()
