from typing import Any

from pydantic import BaseModel, validator

from ..config import config


class Base(BaseModel):
    @validator('rating', 'ratingReal', check_fields=False)
    def validate_rating(cls, rating: float) -> Any:
        if not (0 <= rating <= config.HIGHEST_SONG_CONSTANT + 2):
            raise ValueError(
                f"rating: '{rating}' must be in [0, {config.HIGHEST_SONG_CONSTANT + 2}]")
        return float(rating)

    @validator('constant', check_fields=False)
    def validate_constant(cls, constant: float) -> Any:
        if not (0 <= constant <= config.HIGHEST_SONG_CONSTANT):
            raise ValueError(
                f"constant: '{constant}' must be in [0, {config.HIGHEST_SONG_CONSTANT}]")
        return float(constant)
