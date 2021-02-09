"""
处理函数封装
"""
import base64
from io import BytesIO
from PIL import Image # PIL 垃圾类型注解
from typing import Any

async def level_to_text(difficulty: int) -> str:
    dic = {0: 'pst', 1: 'prs', 2: 'ftr', 3: 'byd'}
    return dic[difficulty]


async def b64encoded(s: str) -> str:
    return base64.b64encode(s.encode()).decode()


async def b64decoded(s: str) -> str:
    return base64.b64decode(s.encode()).decode()


async def imageobj_to_base64(img: Any) -> str:
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_obj = output_buffer.getvalue()
    return base64.b64encode(byte_obj).decode()

