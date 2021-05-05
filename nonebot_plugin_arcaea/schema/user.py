from typing import Optional, Any
from datetime import datetime

from pydantic import BaseModel, validator


class User(BaseModel):
    __tablename__: str = 'accounts'

    qq: int  # primary key
    code: Optional[str] = None
    created_time: datetime
    is_active: bool = True
    recent_type: str
    b30_type: str

    @validator('code')
    def validate_code(cls, code: Optional[str]) -> Optional[str]:
        if not code:
            return None
        if len(code) != 9 or not code.isnumeric():
            raise ValueError(f"code: '{code}' must be of length 9 or number")
        return code

    @validator('recent_type', 'b30_type')
    def validate_query_type(cls, v: str) -> str:
        if v != 'text' and not v.startswith('theme_'):
            raise ValueError(f"type: '{v}' must be text or one of image themes")
        return v
