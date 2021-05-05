from typing import TYPE_CHECKING
from contextlib import closing

from nonebot.rule import Rule
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import MessageEvent

from .. import crud
from ..db import get_db

if TYPE_CHECKING:
    from nonebot.typing import Bot, Event


def validate_user() -> Rule:
    """
    validate user and assign to state
    """
    async def _validate_user(bot: "Bot", event: "Event", state: T_State) -> bool:
        if not isinstance(event, MessageEvent):
            return False
        with closing(get_db().cursor()) as cursor:
            user = crud.user.get_by_qq(cursor, int(event.get_user_id()))
        state['current_user'] = user
        return True if not user else user.is_active
    return Rule(_validate_user)
