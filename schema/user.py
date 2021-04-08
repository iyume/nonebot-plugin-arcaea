import sqlite3
from typing import Optional, Any
from datetime import datetime

from pydantic import BaseModel, validator


class User(BaseModel):
    qq: int
    name: str
    code: str
    created_time: datetime
    query_recent_type: Optional[str]
    query_b30_type: Optional[str]

    @validator('code')
    def validate_code(cls, code: str) -> Any:
        if len(code) != 9:
            raise ValueError(f"length of code: '{code}' must be 9")
        return code

    @validator('query_recent_type', 'query_b30_type')
    def validate_query_b30_type(cls, v: str) -> Any:
        if v not in ['text', 'pic']:
            raise ValueError(f"query_type: '{v}' must be text or pic")
        return v
