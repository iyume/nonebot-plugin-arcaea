import os
import base64
from datetime import datetime
from databases import Database

import nonebot
from nonebot.plugin import on_shell_command, on_command
from nonebot.rule import ArgumentParser
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, Event, MessageEvent, Message
from nonebot.log import logger

from .api_estertion import ws_query_songname, ws_query_recent, ws_query_b30
from .img_generator import genb64img_b30_theme_inuchan
from .functions import level_to_text


config = nonebot.get_driver().config
api_config = config.arcaea_api or 'estertion'
"""
- 默认：`estertion` 使用公开源
- 可选：↓ ↓ ↓ config 填写示例 ↓ ↓ ↓
`estertion`                     -> 默认公开 API
`http://127.0.0.1:8080/v3`      -> 自建 API
`mix http://127.0.0.1:8080/v3`  -> estertion + 自建 API（推荐方式
"""
# 自建 API 可参考 https://github.com/TheSnowfield/BotArcAPI

current_path = os.path.dirname(os.path.realpath(__file__))
db_name = 'store.db'
db_path = os.path.join(current_path, db_name)
database = Database(f"sqlite:///{db_path}")



parser = ArgumentParser()
parser.add_argument('query')
parser.add_argument('code')

arc = on_shell_command('arc', aliases={'a'}, parser=parser, priority=1, block=True)

async def qq2code(qq) -> str:
    await database.connect()
    if code := await database.fetch_val(f"SELECT code FROM accounts WHERE user_id = {qq}"):
        await database.disconnect()
        return code
    else:
        await database.disconnect()
        return ''

async def handle_userinfo_msg(query_recent: dict) -> str:
    """
    **params**
        `name`: 称号
        `ppt`: 当前PTT
        `recent_songname`: 最近游玩曲名
        `recent_songlevel`: 最近游玩难度
        `recent_score`: 最近游玩分数
        `recent_ptt`: 最近游玩单曲PTT
    """
    name = query_recent['content']['name']
    ptt = query_recent['content']['rating']
    recent_play = query_recent['content']['recent_score']
    recent_songname = await ws_query_songname(song_id=recent_play['song_id'])
    recent_level = await level_to_text(recent_play['difficulty'])
    recent_score = recent_play['score']
    recent_ptt = recent_play['rating']
    return '\n'.join([f'称号: {name}',
                    f'当前PTT: {ptt}',
                    f'最近游玩: {recent_songname}',
                    f'难度: {recent_level}',
                    f'Score: {recent_score}',
                    f'PTT: {recent_ptt}'])

async def handle_recent_msg(query_recent: dict) -> str:
    name = query_recent['content']['name']
    recent_play = query_recent['content']['recent_score']
    recent_songname = await ws_query_songname(song_id=recent_play['song_id'])
    recent_level = await level_to_text(recent_play['difficulty'])
    recent_score = recent_play['score']
    recent_ptt = recent_play['rating']
    recent_shiny_perfect_count = recent_play['shiny_perfect_count']
    recent_perfect_count = recent_play['perfect_count']
    recent_near_count = recent_play['near_count']
    recent_miss_count = recent_play['miss_count']
    dt_ = datetime.fromtimestamp(recent_play['time_played'] / 1000)
    time_played = f"{datetime.strftime(dt_, '%F %X')}"
    return '\n'.join([f'称号: {name}',
                    f'最近游玩: {recent_songname}',
                    f'难度: {recent_level}',
                    f'Score: {recent_score}',
                    f'PTT: {recent_ptt}',
                    f'大P: {recent_shiny_perfect_count}',
                    f'小P: {recent_perfect_count - recent_shiny_perfect_count}',
                    f'count P: {recent_perfect_count}',
                    f'count FAR: {recent_near_count}',
                    f'count MISS: {recent_miss_count}',
                    f'Time: {time_played}'])

@arc.handle()
async def _arc_handle(bot: Bot, event: Event, state: T_State):

    if isinstance(event, MessageEvent):

        api1_uri_ws = 'wss://arc.estertion.win:616'
        api2_uri_http = None

        if api_config == 'estertion': # 默认公共 API ## 由于 API 资源不足，无法提供 songinfo 查询
            available = ['userinfo', 'b30', 'recent', 'allscores', 'chart']
            api_type: int = 1

        elif api_config[:4] == 'http': # 自建 API 请根据需求选择
            available = ['userinfo', 'b30', 'recent', 'songinfo', 'songbest']
            api_type: int = 2
            api2_uri_http = api_config

        elif api_config[:3] == 'mix': # 混合 API 进行全面查询
            # estertion -> b30 | allscores | chart
            # 自建 API  -> songinfo | recent
            try:
                api2_uri_http = api_config.split()[1]
                if api2_uri_http[:4] != 'http' or api2_uri_http[-3:-1] != '/v':
                    raise ValueError
                available = ['userinfo', 'b30', 'recent', 'songinfo', 'songbest', 'allscores', 'chart']
                api_type: int = 3
            except:
                logger.error('Assigning mix API config Error. Example: "mix http://127.0.0.1:8080/v3".')
                available = ['API 配置错误，请按照格式填写']
                api_type: int = -1
                await arc.finish('API 配置错误')
                return

        else:
            logger.error('Loding API config Error. Check the doc at https://github.com/iyume/nonebot-plugin-arcaea')
            available = ['API 配置错误，请按照格式填写']
            api_type: int = -1
            await arc.finish('API 配置错误')
            return


        rcmd = state['_prefix']['raw_command']
        commands = [f'{rcmd} {i}' for i in available + ['help', 'bind [code]', 'unbind']]
        prompt_msg = 'Arcaea 查分命令\n参数列表：\n' + '\n'.join(commands)

        state['avaiable'] = available
        state['prompt'] = prompt_msg

        try:
            cmd = state['argv'][0]
        except IndexError:
            await arc.finish(prompt_msg)
            return


        # 帮助命令
        if cmd in ['help', 'doc', '帮助']:
            await arc.finish(prompt_msg)
            return


        # 注册功能
        if cmd in ['bind', 'register', '绑定']:
            try:
                code = state['args'].code
            except AttributeError:
                logger.error('Executing bind with no Code. Finish.')
                await arc.finish('请携带 Arcaea Code 重输命令')
                return

            # 检查用户是否已存在
            await database.connect()
            query_code = await database.fetch_val(f"SELECT code FROM accounts WHERE user_id = {event.get_user_id()}")
            await database.disconnect()
            if query_code:
                if query_code == code:
                    await arc.finish(f'已绑定，您的 Code 为 {query_code}')
                    return
                else:
                    await arc.finish(f'您输入的 Code 为 {code}\n您在数据库的记录为 {query_code}\n如需更改请先 unbind')
                    return

            # 检查输入 Code 长度是否合法 ## 其实可以做个 str -> int -> str 转换更人性化（（
            if len(code) != 9:
                await arc.finish('Code 长度不合法\n注册命令示例\n//arc bind xxxxxxxxx')
                return

            # 检查输入 Code 是否正确 >>> 查询一次 recent
            if api_type == 1:
                query_recent = await ws_query_recent(code)
            elif api_type == 2 or api_type == 3:
                await arc.finish('功能未开发')
                return
            else:
                await arc.finish(prompt_msg)
                return

            if query_recent['status'] != 1:
                logger.error(f'{query_recent}')
                await arc.finish('Code 错误，请检查')
                return

            await database.connect()
            await database.execute("INSERT INTO accounts (user_id, code) VALUES (:qq,:code)",
                                    {'qq': int(event.get_user_id()),
                                    'code': code})
            await database.disconnect()
            recent_play = query_recent['content']['recent_score']
            try:
                userinfo_msg = await handle_userinfo_msg(query_recent)
            except:
                userinfo_msg = '查询用户信息失败\n请自行使用 userinfo 命令查询'
            await arc.finish('\n'.join(['绑定成功！', userinfo_msg]))
            return


        # 注销、删除账户功能
        if cmd == 'unbind':
            # 检查用户是否已存在
            await database.connect()
            if await database.fetch_val(f"SELECT code FROM accounts WHERE user_id = {event.get_user_id()}"):
                await database.execute(f"DELETE FROM accounts WHERE user_id = {event.get_user_id()}")
                await bot.send(message=f'已删除 {event.get_user_id()} 的记录', event=event)
            else:
                await bot.send(message='您尚未注册', event=event)
            await database.disconnect()
            await arc.finish()
            return


        ### 以下为功能区，进行账户验证同时 assign code 变量
        if code := await qq2code(event.get_user_id()):
            ...
        else:
            await arc.finish('您尚未注册，无法使用查分功能')
            return


        # 查询账户信息
        if cmd in ['userinfo', 'accountinfo']:
            if api_type == 1:
                try:
                    query_recent = await ws_query_recent(code)
                except:
                    await arc.finish('查询用户信息失败')
                    return
            elif api_type == 2 or api_type == 3:
                await arc.finish('功能未开发')
                return
            else:
                await arc.finish(prompt_msg)
                return

            userinfo_msg = await handle_userinfo_msg(query_recent)

            await arc.finish(userinfo_msg)
            return


        # 主功能区，由从接口统一的数据生成结果，数据格式参照 `api_` 开头的模块
        if cmd in available:

            if cmd == 'b30':
                if api_type == 1 or api_type == 3:
                    query_b30_dict = await ws_query_b30(code)
                elif api_type == 2:
                    await arc.finish('功能未开放')
                    return
                else:
                    await arc.finish('fill with b30 exception')
                    return

                if query_b30_dict['status'] == 1:
                    # 考虑到各种问题，b30 以图片返回是目前唯一做法
                    # 图片可 DIY
                    if img_b30 := await genb64img_b30_theme_inuchan(query_b30_dict):
                        await arc.finish(message=Message(f'[CQ:image,file=base64://{img_b30}]'))
                        return
                    else:
                        await arc.finish('未知错误')
                        return
                else:
                    await arc.finish('查询 b30 失败，请重试\n多次失败请联系 Master')
                    return

            if cmd == 'recent':
                if api2_uri_http:
                    # 待改进
                    query_recent_dict = await ws_query_recent(code)
                elif api1_uri_ws:
                    query_recent_dict = await ws_query_recent(code)
                else:
                    await arc.finish('fill with recent exception')
                    return

                if query_recent_dict['status'] == 1:
                    # 可以选择以 message 返回，也可以使用图片（图片可 DIY
                    recent_msg = await handle_recent_msg(query_recent_dict)
                    await arc.finish(recent_msg)
                    return
                else:
                    await arc.finish('查询 recent 失败，请重试\n多次失败请联系 Master')
                    return

            if cmd == 'songinfo':
                ...

            if cmd == 'allscores':
                ...

            if cmd == 'chart':
                ...

            logger.warning(f'{cmd} 测试阶段功能')
            await arc.finish('测试阶段，见到此消息代表无法查询')
            return

        logger.warning('无效查询命令')
        await arc.finish(prompt_msg)
        return


    else:

        logger.warning('Not supported Event type')
        await arc.finish()
        return



get_userlist = on_command('get_arcaea_userlist', permission=SUPERUSER, priority=10)

@get_userlist.handle()
async def _get_userlist(bot: Bot):
    await database.connect()
    data = await database.fetch_all("SELECT * FROM accounts")
    await database.disconnect()
    msg_head = ' ' * 5 + 'qqnum' + ' ' * 5 + 'code' + '\n'
    msg_main = '\n'.join([f'{i} {val[0]} {val[1]}' for i, val in enumerate(data)])
    msg_tail = f'\n用户总数: {len(data)}'
    await get_userlist.finish(msg_head + msg_main + msg_tail)

