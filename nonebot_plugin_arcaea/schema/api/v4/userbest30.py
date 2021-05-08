from typing import List

from pydantic import validator

from ...basemodel import Base
from .songscore import SongScore


"""
{
    "$schema": "https://github.com/TheSnowfield/BotArcAPI/wiki/Reference-of-v4-user-best30",
    "best30_avg": 0.0000,
    "recent10_avg": 0.0000,
    "best30_list": [
        {
            "song_id": "grievouslady",
            "difficulty": 2,
            "score": 0,
            "shiny_perfect_count": 0,
            "perfect_count": 0,
            "near_count": 0,
            "miss_count": 0,
            "health": 0,
            "modifier": 0,
            "time_played": 114514145141,
            "best_clear_type": 0,
            "clear_type": 0,
            "character": 0,
            "is_skill_sealed": false,
            "is_char_uncapped": false,
            "rating": 0.0000
        },
        # more data....
    ]
}
"""

class UserBest30(Base):
    best30_avg: float
    recent10_avg: float
    best30_list: List[SongScore]  # 依据 rating 排序

    @validator('best30_list', pre=True)
    def prehandle_best30_list(cls, best30_list: List[dict]) -> List[SongScore]:
        if len(best30_list) > 30:
            raise ValueError
        return [SongScore(**d) for d in sorted(best30_list, key=lambda x: x['rating'], reverse=True)]
