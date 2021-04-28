from .matcher import arc
from . import handlers


arc.handle()(handlers.pre_handler)
arc.handle()(handlers.help_handler)
arc.handle()(handlers.bind_handler)
arc.handle()(handlers.auth_handler)
