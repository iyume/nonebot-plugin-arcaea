from typing import Dict, Optional, Union
from pydantic import validator

from .basemodel import SongScoreBase, Base


class SongScore(SongScoreBase):
    clear_type: Optional[int]
    best_clear_type: Optional[int]
    modifier: Optional[int]
    song_date: Optional[int]
    character: Optional[int]
    health: Optional[int]
    is_skill_sealed: Optional[bool]
    is_char_uncapped: Optional[bool]


class Recent(Base):
    name: str
    rating: float
    recent_score: SongScore

    @validator('recent_score', pre=True)
    def prehandle_recent_score(
        cls, val: Union[dict, SongScore]
    ) -> SongScore:
        if isinstance(val, dict):
            return SongScore(**val)
        return val


class Best30(Base):
    name: str
    rating: float
    b30_avg: float
    r10_avg: float
    b30_dict: Dict[int, SongScore]  # 默认已依据 rating 排序，排序参照为 int 型键

    @validator('b30_dict', pre=True)
    def prehandle_b30_dictlist(
        cls, b30_dict: Dict[int, Union[dict, SongScore]]
    ) -> Dict[int, SongScore]:
        _b30: Dict[int, SongScore] = {}
        for key, val in sorted(b30_dict.items()):
            _b30[key] = SongScore(**val) if isinstance(val, dict) else val
        return _b30
