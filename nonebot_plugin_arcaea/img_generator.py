

import os
import httpx
import random
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from PIL import Image, ImageFont, ImageDraw
from nonebot.log import logger

from .functions import imageobj_to_base64, level_to_text
from .api_estertion import ws_query_songname_many



async def genimg_recent(b30_dict: Dict[str, Union[int, Dict[str, Any]]]) -> str:
    ...



async def genb64img_b30_theme_inuchan(b30_dict: Dict[str, Union[int, Dict[str, Any]]]) -> str:
    """ 由标准化后的 b30_dict 生成 base64，可以自行设计主题

    Args:
        b30_dict (Dict[str, Union[int, Dict[str, Union[int, Union[int, Dict[str, Union[int, str]]]]]]]): 格式参考 `api_` 查询 b30 函数的 Return Example
        PS: 请直接传入 `api_` 查询 b30 函数中获取的包含所有信息的 dict

    Returns:
        str: base64_encoded string-like object
    """
    if isinstance(b30_dict['content'], dict):
        content = b30_dict['content']
    else:
        return ''

    if isinstance(content, dict):
        try:
            user_name = content['user_name']
            user_ptt = content['user_ptt']
            b30_avg = content['best30_avg']
            r10_avg = content['recent10_avg']
            b30_lst = content['best30_list']
        except:
            logger.error('genb64img_b30 second if statement Error')
            return ''
    else:
        return ''

    songnames = await ws_query_songname_many([b30_lst[i]['song_id'] for i in b30_lst])
    difficulties = [await level_to_text(b30_lst[i]['difficulty']) for i in b30_lst]
    scores = [str(b30_lst[i]['score']) for i in b30_lst]
    ratings = [f"{b30_lst[i]['rating']:.2f}" for i in b30_lst]

    current_path = os.path.dirname(os.path.realpath(__file__))

    ft = ImageFont.truetype(os.path.join(current_path, 'assets/b30_theme_inuchan/Roboto-Bold.ttf'), 18)
    ft_low = ImageFont.truetype(os.path.join(current_path, 'assets/b30_theme_inuchan/Roboto-Regular.ttf'), 14)
    ft_title = ImageFont.truetype(os.path.join(current_path, 'assets/b30_theme_inuchan/Roboto-Bold.ttf'), 25)

    img = Image.open(os.path.join(current_path, 'assets/b30_theme_inuchan/in.png'))
    draw = ImageDraw.ImageDraw(img)

    title_color = (230, 230, 230)
    inner_gap = [20, 52, 52]

    for i in range(15):
        ylen = 60 * i
        draw.text((150, ylen + inner_gap[0]), songnames[i] + ' ' + f'[{difficulties[i].upper()}]', title_color, font=ft_title)
        draw.text((150, ylen + inner_gap[1]), 'Score: ' + scores[i], (255, 255, 255), font=ft)
        draw.text((400, ylen + inner_gap[2]), 'PTT: ' + ratings[i], (255, 255, 255), font=ft)
        draw.text((600, ylen + inner_gap[0]), songnames[i+15] + ' ' + f'[{difficulties[i+15].upper()}]', title_color, font=ft_title)
        draw.text((600, ylen + inner_gap[1]), 'Score: ' + scores[i+15], (255, 255, 255), font=ft)
        draw.text((850, ylen + inner_gap[2]), 'PTT: ' + ratings[i+15], (255, 255, 255), font=ft)

    info_draw = f'Name: {user_name}   Player PTT: {user_ptt}   b30_avg: {b30_avg}   r10_avg: {r10_avg}'
    draw.text((700, 930), info_draw, (200, 200, 200), font=ft_low)
    author_draw = datetime.now().strftime("%F %X") + "   Powered by iyume"
    draw.text((20, 930), author_draw, (200, 200, 200), font=ft_low)

    return await imageobj_to_base64(img)




