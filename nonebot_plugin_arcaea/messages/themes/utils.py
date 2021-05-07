from importlib import import_module
import base64
from PIL import Image
from io import BytesIO

from . import pkgs
from ._base import ThemeBase


def import_theme(theme_name: str) -> ThemeBase:
    pkg = import_module(f"{pkgs.__name__}.{theme_name}")
    return getattr(pkg, 'Theme')

def imageobj_to_base64(img: Image.Image) -> str:
    image_buffer = BytesIO()
    img.save(image_buffer, format='PNG')
    byte_obj = image_buffer.getvalue()
    return base64.b64encode(byte_obj).decode()
