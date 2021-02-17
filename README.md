# nonebot-plugin-arcaea
[![pypi](https://img.shields.io/pypi/v/nonebot-plugin-arcaea.svg)](https://pypi.org/project/nonebot-plugin-arcaea/)
![implementation](https://img.shields.io/pypi/implementation/nonebot-plugin-arcaea)
![wheel](https://img.shields.io/pypi/wheel/nonebot-plugin-arcaea)
![python](https://img.shields.io/pypi/pyversions/nonebot-plugin-arcaea)
[![license](https://img.shields.io/github/license/iyume/nonebot-plugin-arcaea.svg)](https://raw.githubusercontent.com/iyume/nonebot-plugin-arcaea/main/LICENSE)

- 基于 [nonebot2](https://github.com/nonebot/nonebot2)

## 功能 Resume
Arcaea 查分器，可以实现 `best30` | `recent` | `songinfo` 之类的查询功能

## 特点 Feature
- 可以添加自建 API，需要自己写 Adapter

- 以图片形式返回 `best30` | `recent`

- 图片可以自定义主题

## 快速开始 Quickstart
**注意**

1. 由于使用了 colon equal，使用前请保证 `python>=3.8`

2. 由于使用了 shell_like command，使用前请保证 `nonebot2` 处于 v2a9 以上的版本

3. 安装插件
```
pip install nonebot-plugin-arcaea
```
如果你使用的是 `nb plugin install`，此时 `bot.py` 会自动插入 `nonebot.load_plugin('nonebot_plugin_arcaea')`

若没有，请手动添加

**bot 指令**

- `/arc bind` 绑定账户

- `/arc recent` 查询最近游玩，返回文字

- `/arc b30` 查询 best30，返回图片

## 可选配置项 Optional Env
`ARCAEA_API`:
- `estertion`
- `http://127.0.0.1:616/v3`
- `mix http://127.0.0.1:616/v3`

本插件为来自 [BotArcApi](https://github.com/TheSnowfield/BotArcAPI) 搭建的 API 做了适配，只需要按照以上配置填写便可使用

`mix` 开头的配置项代表 API 混合查询，详情见源码

## 特别感谢
- [Mrs4s / go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- [nonebot / nonebot2](https://github.com/nonebot/nonebot2)
- [TheSnowfield / BotArcAPI](https://github.com/TheSnowfield/BotArcAPI)
- [All Arcaea Player](https://arcaea.lowiro.com)

## 优化建议
如有优化建议请积极提交 issues 或者 pull requests

## 碎碎念
在完成这个插件的中途，我 kou 框了

最近忙着帮大学教授做一个网站，在接下来至少一个星期我将不会对此项目进行更新，但是 pr 和 issue 是会看的，欢迎贡献您的代码

## 后期打算
使用 fastapi 实现 allscores 的查询

为 recent 添加图片查询功能

使用 pandas 结合 estertion 给出的查分记录完成 chart 分析

以及实现各种 BotArcApi 中可以获取的资源
