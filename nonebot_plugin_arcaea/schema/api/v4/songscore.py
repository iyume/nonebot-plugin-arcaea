from typing import Optional
from datetime import datetime

from pydantic import validator

from ...basemodel import Base
from ..utils import num2diffstr


"""
{
    "$schema": "https://github.com/TheSnowfield/BotArcAPI/wiki/Reference-of-v4-user-best",
    "song_id": "grievouslady",
    "difficulty": 2,
    "score": 0,
    "shiny_perfect_count": 0,
    "perfect_count": 0,
    "near_count": 0,
    "miss_count": 0,
    "health": 0,
    "modifier": 0,
    "time_played": 1145141145141,
    "best_clear_type": 0,
    "clear_type": 0,
    "character": 0,
    "is_skill_sealed": false,
    "is_char_uncapped": false,
    "rating": 0.0000
}
"""

class SongScore(Base):
    song_id: str
    difficulty: str
    score: int
    shiny_perfect_count: int
    perfect_count: int
    near_count: int
    miss_count: int
    time_played: datetime
    rating: float  # 单曲ptt

    health: Optional[int]
    clear_type: Optional[int]
    best_clear_type: Optional[int]
    modifier: Optional[int]
    song_date: Optional[int]
    character: Optional[int]
    is_skill_sealed: Optional[bool]
    is_char_uncapped: Optional[bool]

    @validator('difficulty', pre=True)
    def prehandle_songscore_difficulty(cls, val: int) -> str:
        return num2diffstr(val)
