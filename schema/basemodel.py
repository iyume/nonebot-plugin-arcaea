from typing import Any

from pydantic import BaseModel, validator

from ..config import config


class Base(BaseModel):
    @validator('rating', check_fields=False)
    def validate_rating(cls, rating: float) -> Any:
        if not (0 <= rating <= config.HIGHEST_SONG_CONSTANT + 2):
            raise ValueError(
                f"rating: '{rating}' must be in [0, {config.HIGHEST_SONG_CONSTANT + 2}]")
        return rating

    @validator('constant', check_fields=False)
    def validate_constant(cls, constant: float) -> Any:
        if not (0 <= constant <= config.HIGHEST_SONG_CONSTANT):
            raise ValueError(
                f"constant: '{constant}' must be in [0, {config.HIGHEST_SONG_CONSTANT}]")


class SongScoreBase(Base):
    song_id: str
    difficulty: int
    score: int
    shiny_perfect_count: int
    perfect_count: int
    near_count: int
    miss_count: int
    time_played: int
    rating: float   # 单曲ptt
    constant: float # 歌曲定数
