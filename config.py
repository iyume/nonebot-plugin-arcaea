import os

from typing import Optional, Dict, Any

from pydantic import BaseSettings, validator

import nonebot
from nonebot.log import logger


class Config(BaseSettings):
    MAINTAINER: str = 'iyume <iyumelive@gmail.com>'

    _config: Any = nonebot.get_driver().config

    CMD: str = 'arc'       # 响应指令
    ALIASES: set = {'a'}  # 命令的 aliases
    CMD_START: str = list(_config.command_start)[0]
    CMD_SEP: str = list(_config.command_sep)[0]

    # command aliases setting
    CMDA_HELP: set    = { 'help', 'doc', '帮助' }
    CMDA_BIND: set    = { 'bind', 'register' }
    CMDA_INFO: set    = { 'info', 'userinfo' }
    CMDA_RECENT: set  = { 'recent' }
    CMDA_B30: set     = { 'b30', 'best30' }

    SQLITE_DATABASE_URI: str = ''

    @validator("SQLITE_DATABASE_URI", pre=True)
    def prehandle_sqlite_db_uri(cls, v: Optional[str]) -> str:
        current_path = os.path.dirname(os.path.realpath(__file__))
        db_name = 'db/all.db'
        db_path = os.path.join(current_path, db_name)
        return db_path

    ARCAEA_API_TYPE: Optional[str] = _config.arcaea_api_type
    # example: 'botarcapi'
    # 可选配置项，作为给 API_URI 赋值的依据
    ARCAEA_API_URI: Optional[str] = _config.arcaea_api_uri
    # example: 'http://127.0.0.1/v3'
    # 可选配置项，关联于 ARCAEA_API_TYPE 配置项，作为获取游玩信息的第二 API，目前只支持 BotArcApi
    ARCAEA_QUERY_CONFIG: Dict[str, str] = _config.arcaea_query_config
    """
    - **类型**: ``Optional[Dict[str, str]]``
    - **默认值**:
        {
            "recent": "estertion",
            "best30": "estertion",
            "songinfo": "botarcapi"
        }

    :说明:
        可选配置项，用于配置命令查分使用的源，此配置项要求填写 ARCAEA_API_TYPE, ARCAEA_API_URI

    :示例:
        {
            "recent": "botarcapi",
            "best30": "botarcapi",  # 由于 estertion 的源查 b30 速度特别快，所以不建议更改此项
            "songinfo": "botarcapi"
        }
    """
    @validator('ARCAEA_QUERY_CONFIG', pre=True)
    def preprocess_arcaea_query_config(
        cls, v: Optional[Dict[str, str]]
    ) -> Dict[str, str]:
        if not v:
            v = dict()
        return {
            "userinfo": v.get('userinfo', 'estertion'),
            "best30": v.get('best30', 'estertion'),
            "songinfo": v.get('songinfo', 'estertion')
        }

    ESTERTION_URI = 'wss://arc.estertion.win:616'
    """
    获取游玩信息的默认 API，来自 estertion 维护的公开源
    """

    TIMEOUT = 8

    HIGHEST_SONG_CONSTANT = 11.5  # 目前最高歌曲定数（风暴byd）

    estertion_uri: str = ESTERTION_URI
    botarcapi_uri: Optional[str] = ARCAEA_API_URI if ARCAEA_API_TYPE == 'botarcapi' else None

    DEFAULT_RECENT_TYPE: str = 'pic'
    DEFAULT_BEST30_TYPE: str = 'pic'
    # 可选：['pic', 'text']，分别对应图片和文字


config = Config()
