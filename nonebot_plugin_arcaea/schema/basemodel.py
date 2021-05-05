from pydantic import BaseModel
from pydantic.dataclasses import dataclass


@dataclass
class Base(BaseModel):
    class Config:
        extra = "ignore"
