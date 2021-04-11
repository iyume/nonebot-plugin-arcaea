from ..basemodel import Base


"""
{
    "$schema": "https://github.com/TheSnowfield/BotArcAPI/wiki/Reference-of-v3-songinfo",
    "ratingClass": 0,
    "chartDesigner": "夜浪",
    "jacketDesigner": "望月けい",
    "rating": 5,
    "ratingReal": 5.5,
    "totalNotes": 765
}
"""

class SongInfoDiffic(Base):
    ratingClass: int
    chartDesigner: str
    jacketDesigner: str
    rating: float
    ratingReal: float
    totalNotes: int
