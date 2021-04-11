from typing import Optional
from datetime import datetime

from pydantic import validator

from ..basemodel import Base
from ._songscore import SongScore


"""
{
    "$schema": "https://github.com/TheSnowfield/BotArcAPI/wiki/Reference-of-v3-userinfo",
    "user_id": 114514,
    "name": "114514",
    "recent_score": {
        "song_id": "grievouslady",
        "difficulty": 2,
        "score": 0,
        "shiny_perfect_count": 0,
        "perfect_count": 0,
        "near_count": 0,
        "miss_count": 0,
        "clear_type": 0,
        "best_clear_type": 0,
        "health": 0,
        "time_played": 1145141145141,
        "modifier": 0,
        "rating": 0
    },
    "character": 0,
    "join_date": 1145141145141,
    "rating": 0,
    "is_skill_sealed": false,
    "is_char_uncapped": false,
    "is_char_uncapped_override": false,
    "is_mutual": false
}
"""

class UserInfo(Base):
    user_id: Optional[int]
    name: str
    rating: float
    recent_score: SongScore

    @validator('recent_score', check_fields=False, pre=True)
    def prehandle_recent_score(cls, val: dict) -> SongScore:
        return SongScore(**val)

    character: Optional[int]
    join_date: Optional[datetime]
    is_skill_sealed: Optional[bool]
    is_char_uncapped: Optional[bool]
    is_char_uncapped_override: Optional[bool]
    is_mutual: Optional[bool]
