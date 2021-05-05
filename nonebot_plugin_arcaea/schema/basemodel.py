from pydantic import BaseModel, validator


class Base(BaseModel):
    class Config:
        extra = "ignore"

    @validator('rating', check_fields=False, pre=True)
    def preprocess_rating(cls, val: float) -> float:
        return val / 100 if val > 100 else val
