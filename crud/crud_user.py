from typing import Optional
from datetime import datetime
from sqlite3.dbapi2 import Cursor

from ..config import config
from .. import schema


class CRUDUser():
    model = schema.User

    def create(
        self,
        db: Cursor,
        qq: int,
        code: str
    ) -> None:
        user_dict = {
            "qq": qq,
            "code": code,
            "created_time": datetime.now(),
            "recent_type": config.DEFAULT_RECENT_TYPE,
            "best30_type": config.DEFAULT_BEST30_TYPE
        }
        db.execute(
            f"""INSERT INTO accounts ({','.join(user_dict.keys())})
            VALUES ({','.join([str(val) for val in user_dict.values()])})""")

    def get_by_qq(
        self,
        db: Cursor,
        qq: int
    ) -> Optional[schema.User]:
        user = db.execute(
            "SELECT * FROM user WHERE qq=?",
            (qq,)
        ).fetchone()
        if not user:
            return None
        return self.model(**user)

    def get_by_code(
        self,
        db: Cursor,
        code: str
    ) -> Optional[schema.User]:
        user = db.execute(
            "SELECT * FROM user WHERE code=?",
            (code,)
        ).fetchone()
        if not user:
            return None
        return self.model(**user)

    def update(
        self,
        db: Cursor,
        qq: int,
        best30_type: Optional[str],
        recent_type: Optional[str]
    ) -> None:
        update_dict = {
            "recent_type": recent_type,
            "best30_type": best30_type
        }
        argments = [f"{i}={val}" for i, val in update_dict.items() if val]
        db.execute(
            f"UPDATE user SET {','.join(argments)} WHERE qq=?",
            (qq,)
        )

    def delete(
        self,
        db: Cursor,
        qq: int
    ) -> None:
        # unbind method, not really delete user record
        db.execute(
            "UPDATE user SET code=NULL WHERE qq=?",
            (qq,)
        ).fetchone()


user = CRUDUser()
