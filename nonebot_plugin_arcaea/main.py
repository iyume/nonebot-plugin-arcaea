from .matcher import arc
from . import handlers


arc.handle()(handlers.pre_handler)
arc.handle()(handlers.help_handler)
arc.handle()(handlers.bind_handler)
arc.handle()(handlers.songinfo_handler)
arc.handle()(handlers.auth_handler)
arc.handle()(handlers.info_handler)
arc.handle()(handlers.recent_handler)
arc.handle()(handlers.b30_handler)
arc.handle()(handlers.userconfig_handler)
