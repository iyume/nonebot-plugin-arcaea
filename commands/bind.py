from typing import Any


class CMDBind:
    ALIASES = {'bind', 'register'}

    def __contains__(self, cmd: str) -> Any:
        return cmd in self.ALIASES


cmd_bind = CMDBind()
