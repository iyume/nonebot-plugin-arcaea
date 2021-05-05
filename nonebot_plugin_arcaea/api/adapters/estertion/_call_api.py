import json
import websockets
import brotli
from typing import Any

from ....config import config


async def songdb(timeout: int = config.TIMEOUT) -> Any:
    """
    返回 ``song_id`` - 歌名(en|jp) 的字典表
    """
    async with websockets.connect(config.ESTERTION_URI, timeout=timeout) as ws:
        await ws.send('constants')
        r = await ws.recv()
        await ws.close()
        return json.loads(brotli.decompress(r))


async def userinfo(code: str, timeout: int = config.TIMEOUT) -> Any:
    """
    返回最近游玩成绩
    """
    async with websockets.connect(config.ESTERTION_URI, timeout=timeout) as ws:
        await ws.send(f"{code} 1 5")
        pstring = await ws.recv()
        if pstring != 'queried':
            raise RuntimeError(str(pstring))
        while True:
            if ws.closed:
                raise RuntimeError
            r = await ws.recv()
            if isinstance(r, str) and r == 'error,add':
                raise ConnectionError
            if isinstance(r, bytes):
                content = json.loads(brotli.decompress(r))
                if content['cmd'] == 'userinfo':
                    await ws.close()
                    return content


async def all(code: str, timeout: int = config.TIMEOUT) -> Any:
    """
    返回 ws 查询的全部结果，包括 ``userinfo``, ``recent``, ``record of all songs``
    """
    _data: list = []
    async with websockets.connect(config.ESTERTION_URI, timeout=timeout) as ws:
        await ws.send(f"{code} 5 12")
        pstring = await ws.recv()
        if pstring != 'queried':
            raise RuntimeError(str(pstring))
        try:
            # 这个源在 recv 33 次和 52 次循环时随机报错，目前暂无解决方法
            while True:
                if ws.closed:
                    raise RuntimeError
                r = await ws.recv()
                if isinstance(r, str) and r == 'error,add':
                    raise ConnectionError
                if isinstance(r, str) and r == 'bye':
                    return _data
                if isinstance(r, bytes):
                    data = json.loads(brotli.decompress(r))
                    _data.append(data)
        except websockets.exceptions.ConnectionClosedError as e:
            if _data:
                return _data
            else:
                raise e
