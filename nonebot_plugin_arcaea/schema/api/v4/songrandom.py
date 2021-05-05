from ...basemodel import Base


"""
{
    "$schema": "https://github.com/TheSnowfield/BotArcAPI/wiki/Reference-of-v4-song-random",
    "id": "ifi",
    "rating_class": 2
}
"""

class SongRandom(Base):
    id: str
    rating_class: int
