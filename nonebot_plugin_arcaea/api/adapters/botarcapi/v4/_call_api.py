from typing import Any, Optional

from httpx import AsyncClient, TimeoutException

from .....config import config
from .....exceptions import ConfigError
from ....utils import http_status_handler
from ....exceptions import HTTPException


def get_uri(uri: Optional[str]) -> str:
    if not uri:
        raise ConfigError
    return uri.rstrip('/')


async def get(uri: str, **params: Any) -> Any:
    timeout = params.get('timeout', config.TIMEOUT)
    try:
        async with AsyncClient(timeout=timeout) as client:
            response = await client.get(uri, params=params)
    except TimeoutException as e:
        raise e
    except:
        raise HTTPException(
            status_code=500, detail='500 Server error')
    http_status_handler(response)
    return response.json()


async def userbest(code: str, songname: str, difficulty: int) -> Any:
    endpoint = get_uri(config.BOTARCAPI_URI) + '/user/best'
    return await get(
        endpoint,
        usercode=code,
        songname=songname,
        difficulty=difficulty
    )


async def userbest30(code: str) -> Any:
    endpoint = get_uri(config.BOTARCAPI_URI) + '/user/best30'
    return await get(
        endpoint,
        usercode=code,
        timeout=config.TIMEOUT + 20
    )


async def userinfo(code: str, recent: int = 1) -> Any:
    endpoint = get_uri(config.BOTARCAPI_URI) + '/user/info'
    return await get(
        endpoint,
        usercode=code,
        recent=int(recent)
    )


async def songalias(songid: str) -> Any:
    endpoint = get_uri(config.BOTARCAPI_URI) + '/song/alias'
    return await get(
        endpoint,
        songid=songid
    )


async def songinfo(songname: str) -> Any:
    endpoint = get_uri(config.BOTARCAPI_URI) + '/song/info'
    return await get(
        endpoint,
        songname=songname
    )


async def songrandom(start: Optional[int] = None, end: Optional[int] = None) -> Any:
    endpoint = get_uri(config.BOTARCAPI_URI) + '/song/random'
    if start is not None:
        if end is None:
            end = start + 1
        return await get(endpoint, start=start, end=end)
    return await get(endpoint)


async def songrating(start: int, end: Optional[int] = None) -> Any:
    endpoint = get_uri(config.BOTARCAPI_URI) + '/song/rating'
    if start is not None:
        if end is None:
            end = start + 1
        return await get(endpoint, start=start, end=end)
    return await get(endpoint)
