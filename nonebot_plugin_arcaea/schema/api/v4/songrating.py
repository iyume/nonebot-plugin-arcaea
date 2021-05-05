from typing import List

from pydantic import validator

from ...basemodel import Base


"""
{
    "$schema": "https://github.com/TheSnowfield/BotArcAPI/wiki/Reference-of-v4-song-rating",
    "rating": [
        {
            "sid": "fractureray",
            "rating": 11.2,
            "rating_class": 2,
            "difficulty": 22
        },
        {
            "sid": "grievouslady",
            "rating": 11.3,
            "rating_class": 2,
            "difficulty": 22
        },
        {
            "sid": "tempestissimo",
            "rating": 11.5,
            "rating_class": 3,
            "difficulty": 22
        }
    ]
}
"""

class _SongRatingOne(Base):
    sid: str
    rating: float
    rating_class: int
    difficulty: int

class SongRating(Base):
    rating: List[_SongRatingOne]

    @validator('rating', pre=True)
    def prehandle_rating(cls, rating_list: List[dict]) -> List[_SongRatingOne]:
        return [_SongRatingOne(**d) for d in sorted(rating_list, key=lambda x: x['rating'])]
