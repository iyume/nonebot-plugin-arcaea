from typing import Dict, List
from datetime import datetime

from pydantic import validator

from ..basemodel import Base


"""
{
    "$schema": "https://github.com/TheSnowfield/BotArcAPI/wiki/Reference-of-v3-songinfo",
    "id": "ifi",
    "title_localized": {
        "en": "#1f1e33"
    },
    "artist": "かめりあ(EDP)",
    "bpm": "181",
    "bpm_base": 181,
    "set": "vs",
    "audioTimeSec": 163,
    "side": 1,
    "remote_dl": true,
    "world_unlock": false,
    "date": 1590537604,
    "difficulties": [
        {
            "ratingClass": 0,
            "chartDesigner": "夜浪",
            "jacketDesigner": "望月けい",
            "rating": 5,
            "ratingReal": 5.5,
            "totalNotes": 765
        },
        {
            "ratingClass": 1,
            "chartDesigner": "夜浪",
            "jacketDesigner": "望月けい",
            "rating": 9,
            "ratingReal": 9.2,
            "totalNotes": 1144
        },
        {
            "ratingClass": 2,
            "chartDesigner": "夜浪 VS 東星 \"Convergence\"",
            "jacketDesigner": "望月けい",
            "rating": 10,
            "ratingReal": 10.9,
            "ratingPlus": true,
            "totalNotes": 1576
        }
    ]
}
"""

class SongInfoDiffic(Base):
    ratingClass: int
    chartDesigner: str
    jacketDesigner: str
    rating: float
    ratingReal: float
    totalNotes: int

class SongInfo(Base):
    id_: str
    title_localized: Dict[str, str]
    artist: str
    bpm: float       # automatic type conversion
    bpm_base: float  # automatic type conversion
    set_: str
    audioTimeSec: int
    side: int
    remote_dl: bool
    world_unlock: bool
    date: datetime
    difficulties: List[SongInfoDiffic]

    @validator('difficulties', pre=True)
    def prehandle_songinfo_difficulties(cls, v: List[dict]) -> List[SongInfoDiffic]:
        return [SongInfoDiffic(**d) for d in sorted(v, key=lambda x: x['ratingClass'])]
