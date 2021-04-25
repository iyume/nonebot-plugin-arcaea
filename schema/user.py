from typing import Optional, Any
from datetime import datetime

from pydantic import BaseModel, validator


class User(BaseModel):
    qq: int  # primary key
    code: Optional[str] = None
    created_time: datetime
    is_active: bool = True
    recent_type: Optional[str]
    b30_type: Optional[str]

    @validator('code')
    def validate_code(cls, code: Optional[str]) -> Any:
        if not code:
            return None
        if len(code) != 9:
            raise ValueError(f"length of code: '{code}' must be 9")
        return code

    @validator('recent_type', 'b30_type')
    def validate_query_type(cls, v: str) -> Any:
        if v not in ['text', 'pic']:
            raise ValueError(f"type: '{v}' must be text or pic")
        return v
