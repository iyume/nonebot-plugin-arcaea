from importlib import import_module
from pkgutil import iter_modules
import base64
from pathlib import Path
from PIL import Image
from io import BytesIO

from nonebot.log import logger

from ._base import ThemeBase
from ...config import config


def import_theme(theme_name: str) -> ThemeBase:
    if '.' in theme_name:
        raise ValueError('theme_name cannot contain "."')
    pkg = import_module(f"{__package__}.pkgs.{theme_name}")
    return getattr(pkg, 'Theme')


def imageobj_to_base64(img: Image.Image) -> str:
    image_buffer = BytesIO()
    img.save(image_buffer, format='PNG')
    byte_obj = image_buffer.getvalue()
    return base64.b64encode(byte_obj).decode()


def check_available_themes() -> None:
    for theme in config.AVAILABLE_USER_CONFIG[1:]:
        try:
            import_theme(theme)
        except:
            logger.error(f'Arcaea theme fail to import {theme}')
        else:
            logger.opt(colors=True).info(f'Arcaea theme <b><u>{theme}</u></b> successfully import')


def print_themes_import_info() -> None:
    pkgs_path = Path(__file__).parent / 'pkgs'
    for module_info in iter_modules([str(pkgs_path)]):
        logger.opt(colors=True).info(f'Arcaea theme <b><u>{module_info.name}</u></b> successfully import')


check_available_themes()
