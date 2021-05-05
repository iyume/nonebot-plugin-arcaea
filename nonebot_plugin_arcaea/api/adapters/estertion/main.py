from statistics import mean

from . import _call_api
from ..._base import APIQueryBase
from .... import schema


class APIQuery(APIQueryBase):
    @staticmethod
    async def songdb() -> dict:
        r = await _call_api.songdb()
        return r['data']

    @staticmethod
    async def songname(song_id: str) -> str:
        r = await _call_api.songdb()
        r = r['data']
        songname = r[song_id]['en']  # 有其他语种，后期再写
        return songname

    async def userinfo(self, *, with_recent: bool) -> schema.UserInfo:
        r = await _call_api.userinfo(self.code)
        r = r['data']
        recent = r['recent_score'] if with_recent else None
        name = r['name']
        rating = r['rating'] / 100
        return schema.UserInfo(
            name=name,
            rating=rating,
            recent_score=recent
        )

    async def userbest30(self) -> schema.UserBest30:
        r = await _call_api.all(self.code)
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
