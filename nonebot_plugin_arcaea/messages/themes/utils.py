from importlib import import_module

from . import pkgs
from ._base import ThemeBase


def import_theme(theme_name: str) -> ThemeBase:
    pkg = import_module(f"{pkgs.__name__}.{theme_name}")
    return getattr(pkg, 'Theme')
