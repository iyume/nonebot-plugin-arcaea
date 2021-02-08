import websockets
import brotli
from typing import Dict, List, Any
from websockets.exceptions import ConnectionClosedError

from nonebot.log import logger

try:
    import ujson as json
except ImportError:
    import json

'''
如果你想魔改此模块，有以下几个注意点
- ws.send(f'{code} 10 12')
    其中 10 和 12 代表查询难度 10-12 的歌曲
    ws.recv() 得到的曲目的顺序就是从填入的难度由高往低
'''

async def ws_query_songname(song_id: str, uri: str='wss://arc.estertion.win:616', timeout=8) -> str:
    """ 把 song_id 转为英文的歌名

    Args:
        uri (str): ws uri
        songid (str): song_id
        timeout (int, optional): Timeout. Defaults to 8.

    Returns:
        str: song_name (en)
    """

    async def fetch(uri, timeout=8):
        async with websockets.connect(uri, timeout=timeout) as websocket:
            await websocket.send('constants')
            r = await websocket.recv()
            return json.loads(brotli.decompress(r))

    try:
        datacol = await fetch(uri)
    except:
        logger.error('Executing ws_query_songname Error')
        return 'QueryingSongnameError'

    return datacol['data'][song_id]['en']



async def ws_query_songname_many(song_lst: list, uri: str='wss://arc.estertion.win:616', timeout=8) -> list:
    """ 批量把 song_id 转为英文的歌名

    Args:
        uri (str): ws uri
        songid (str): song_id
        timeout (int, optional): Timeout. Defaults to 8.

    Returns:
        str: song_name (en)
    """

    async def fetch(uri, timeout=8):
        async with websockets.connect(uri, timeout=timeout) as websocket:
            await websocket.send('constants')
            r = await websocket.recv()
            return json.loads(brotli.decompress(r))

    try:
        datacol = await fetch(uri)
    except:
        logger.error('Executing ws_query_songname Error')
        return []

    allsongs: list = datacol['data']

    return [allsongs[i]['en'] for i in song_lst]



async def ws_query_recent(code: str, uri: str='wss://arc.estertion.win:616', timeout=8) -> Dict:
    """ 连接 WebSocket 并返回标准格式的 Recent Dict

    Args:
        uri (str): WebSocket endpoint
        code (str): Arcaea code
        timeout (int, optional): Timeout. Defaults to 8.

    Receive Example: # 这个不是输入参考，是从 API 获取的数据参考
        {
            'cmd': 'userinfo',
            'data': {
                'user_id': 4139515,
                'name': 'iyumoe',
                'recent_score': [{
                    'song_id': 'dement',
                    'difficulty': 3,
                    'score': 9601786,
                    'shiny_perfect_count': 825,
                    'perfect_count': 974,
                    'near_count': 49,
                    'miss_count': 17,
                    'clear_type': 1,
                    'best_clear_type': 1,
                    'health': 74,
                    'time_played': 1612590691870,
                    'modifier': 0,
                    'rating': 10.239286666666667,
                    'constant': 9.9,
                    'song_date': 1480000000}],
                'character': 21,
                'join_date': xxxxxxxxxxxxx,
                'rating': 1279,
                'is_skill_sealed': False,
                'is_char_uncapped': True,
                'is_char_uncapped_override': False,
                'is_mutual': False,
                'rating_records': [['210206', '1279'], ...],
                'user_code': 'xxxxxxxxx'
            }
        }

    Returns Example:
        ``正常返回``
        {
            'status': 1,
            'content': {
                'name': 'iyumoe',
                'rating': 12.79,
                'recent_score': [{
                    'song_id': 'ifi',
                    'difficulty': 3,
                    'score': 9601786,
                    'shiny_perfect_count': 114514,
                    'perfect_count': 114514,
                    'near_count': 49,
                    'miss_count': 17,
                    'clear_type': 1,
                    'best_clear_type': 1,
                    'health': 74,
                    'time_played': 1612590691870,
                    'modifier': 0,
                    'rating': 10.239286666666667,
                    'constant': 9.9,
                    'song_date': 1480000000}],
            }
        }

        ``超时返回``
        {
            'status': -1
        }

        ``Code 错误返回``
        {
            'status': -2
        }

        ``异常返回``
        {
            'status': -114514
        }
    """
    # 由于没有复杂的返回类型，就不在此写 logger 了
    # ConnectionClosedError 太玄了，先留个坑
    try:

        async with websockets.connect(uri, timeout=timeout) as websocket:

            await websocket.send(f'{code} 10 12')
            pure_string = await websocket.recv()

            if pure_string == 'queried':
                while True:

                    if websocket.closed:
                        break

                    r = await websocket.recv()

                    if isinstance(r, str) and r == 'error,add':
                        return {'status': -2}

                    if isinstance(r, bytes):
                        receive = json.loads(brotli.decompress(r))
                        if receive['cmd'] == 'userinfo':
                            _recent = receive['data']['recent_score'][0]
                            _recent['rating'] = f'{_recent["rating"]:.2f}'
                            return {'status': 1,
                                    'content': {
                                        'name': receive['data']['name'],
                                        'rating': receive['data']['rating'] / 100,
                                        'recent_score': _recent
                                    }}

            if pure_string == 'timeout':
                return {'status': -1}

        return {'status': -2}

    except:

        return {'status': -114514}



async def ws_query_b30(code: str, uri: str='wss://arc.estertion.win:616', timeout=8) -> Dict:
    """ 连接 WebSocket 并返回标准格式的 Recent Dict

    Args:
        uri (str): WebSocket endpoint
        code (str): Arcaea code
        timeout (int, optional): Timeout. Defaults to 8.

    Returns Example:
        ``正常返回``
        {
            'status': 1,
            'content': {
                'user_name': 'iyumoe',
                'user_ptt': 12.79,
                'best30_avg': 12.77,
                'recent10_avg': 10.77,
                'best30_list': {
                    0: {
                        'user_id': 4139515,
                        'song_id': 'ifi',
                        'difficulty': 2,
                        'score': 9039846,
                        'shiny_perfect_count': 1141,
                        'perfect_count': 1350,
                        'near_count': 149,
                        'miss_count': 77,
                        'health': 46,
                        'modifier': 0,
                        'time_played': ms timestamp,
                        'best_clear_type': 0,
                        'clear_type': 0,
                        'name': 'iyumoe',
                        'character': 21,
                        'is_skill_sealed': False,
                        'is_char_uncapped': True,
                        'rank': 1,
                        'constant': 10.9,
                        'rating': 9.366153333333333,
                        'song_date': 1590537604
                    },
                    1: {
                        ...
                    },
                    x: {
                        ...
                    },
                }
            }
        }

        ``超时返回``
        {
            'status': -1
        }

        ``异常返回``
        {
            'status': -114514
        }
    """
    async def fetchall(uri, code, timeout=8):
        _data = []
        try:
            async with websockets.connect(uri, timeout=timeout) as websocket:
                await websocket.send(f'{code} 5 12')
                pure_string = await websocket.recv()
                if pure_string == 'queried':
                    while True:
                        if websocket.closed:
                            break
                        r = await websocket.recv()
                        if isinstance(r, str) and r == 'bye':
                            break
                        if isinstance(r, bytes):
                            _data.append(json.loads(brotli.decompress(r)))
                if pure_string == 'timeout':
                    return 'timeout'
        except:
            logger.error('Executing ws_query_b30.fetchall Unknown Error')
        return _data

    async def resample_b30(r: list) -> Dict:
        songs = sorted(r, key=(lambda k:k['rating']), reverse=True)
        best30 = songs[:30]
        return {i: val for i, val in enumerate(best30)}

    _r = await fetchall(uri, code, timeout=timeout)

    if isinstance(_r, str) and _r == 'timeout':

        logger.error('Executing ws_query_b30.fetchall Timeout')
        return {'status': -1}

    if isinstance(_r, list) and [1 for i in _r if isinstance(i, dict)]:

        userinfo = _r[1]['data']
        user_name = userinfo['name']
        user_ptt = userinfo['rating'] / 100

        best30dict = await resample_b30([i for j in _r[2:] for i in j['data']])

        from statistics import mean
        b30_avg = mean([best30dict[i]['rating'] for i in best30dict])

        r10_avg = (user_ptt - 0.75 * b30_avg) * 4

        return {'status': 1,
                'content': {
                    'user_name': user_name,
                    'user_ptt': user_ptt,
                    'best30_avg': f'{b30_avg:.2f}',
                    'recent10_avg': f'{r10_avg:.2f}',
                    'best30_list': best30dict
                }}

    else:

        logger.error(f'{_r}')
        return {'status': -114514}





