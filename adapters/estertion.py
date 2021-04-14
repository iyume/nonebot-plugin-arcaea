from typing import Any
from statistics import mean

from .. import schema


async def format_songdb(r: Any) -> Any:
    return r['data']


async def format_userinfo(r: Any, with_recent : bool = True) -> schema.UserInfo:
    r = r['data']
    recent = r['recent_score'][0] if with_recent else None
    name = r['name']
    rating = r['rating'] / 100
    return schema.UserInfo(
        name=name,
        rating=rating,
        recent_score=recent
    )


async def format_b30(r: Any) -> schema.UserBest30:
    # userinfo = r[1]['data']
    # user_name = userinfo['name']
    user_ptt = r[1]['data']['rating'] / 100
    parsed_songs = [i for __ in r[2:] for i in __['data']]
    best30 = sorted(parsed_songs, key=(lambda k:k['rating']), reverse=True)[:30]
    best30_avg = mean([i['rating'] for i in best30])
    recent10_avg = (user_ptt - 0.75 * best30_avg) * 4
    return schema.UserBest30(
        best30_avg=best30_avg,
        recent10_avg=recent10_avg,
        best30_list=best30
    )
    # return {i: val for i, val in enumerate(best30)}
    # from statistics import mean
    # b30_avg = mean([best30dict[i]['rating'] for i in best30dict])
    # r10_avg = (user_ptt - 0.75 * b30_avg) * 4
