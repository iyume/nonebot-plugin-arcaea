from typing import Optional, Dict, Any
from pathlib import Path
import sqlite3

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

    SQLITE_DATABASE_URI: str = 'db/all.db'

    @validator("SQLITE_DATABASE_URI", pre=True)
    def prehandle_sqlite_db_uri(cls, v: str) -> str:
        plugin_dir = Path(__file__).resolve().parent
        db_path = plugin_dir / v
        if not db_path.is_file():
            with open(plugin_dir / 'db' / 'init_db.sql') as f:
                sql_text = f.read()
            with sqlite3.connect(str(db_path)) as conn:
                conn.execute(sql_text)
                conn.commit()
        return str(db_path)

    ESTERTION_URI = 'wss://arc.estertion.win:616'
    # 获取游玩信息的默认 API，来自 estertion 维护的公开源
    BOTARCAPI_URI: Optional[str] = _config.arcaea_botarcapi_uri
    """
    - **类型**: ``Optional[str]``
    - **默认值**: None

    :说明:
        可选配置项，填写 BotArcApi 的服务器地址
        配置名 ARCAEA_BOTARCAPI_URI

    :示例:
        'http://127.0.0.1/v4'
    """
    QUERY_CONFIG: Dict[str, str] = _config.arcaea_query_config
    """
    - **类型**: ``Optional[Dict[str, str]]``
    - **默认值**:
        {
            "userinfo": "estertion",  # include recent score
            "best30": "estertion",
            "songinfo": "estertion"
        }

    :说明:
        可选配置项，用于配置每个命令查询使用的源
        如果检查到 BOTARCAPI_URI 配置项，则全部的值默认为 botarcapi
        配置名 ARCAEA_QUERY_CONFIG

    :示例:
        {
            "userinfo": "botarcapi",
            "best30": "botarcapi",
            "songinfo": "botarcapi"
        }
    """
    @validator('QUERY_CONFIG', pre=True)
    def preprocess_arcaea_query_config(
        cls, v: Optional[Dict[str, str]]
    ) -> Dict[str, str]:
        query_config: Dict[str, str] = {
            'userinfo': 'botarcapi' if cls.BOTARCAPI_URI else 'estertion',
            'best30': 'botarcapi' if cls.BOTARCAPI_URI else 'estertion',
            'songinfo': 'botarcapi' if cls.BOTARCAPI_URI else 'estertion'
        }
        if v:
            query_config.update(v)
        return query_config

    TIMEOUT = 5

    HIGHEST_SONG_CONSTANT = 11.5
    # 目前最高歌曲定数（风暴byd）

    DEFAULT_RECENT_TYPE: str = 'pic'
    DEFAULT_BEST30_TYPE: str = 'pic'
    # 可选：['pic', 'text']，分别对应图片和文字


config = Config()
