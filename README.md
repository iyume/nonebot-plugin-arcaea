# nonebot-plugin-arcaea
[![pypi](https://img.shields.io/pypi/v/nonebot-plugin-arcaea.svg)](https://pypi.org/project/nonebot-plugin-arcaea/)
![python](https://img.shields.io/pypi/pyversions/nonebot-plugin-arcaea)
[![license](https://img.shields.io/github/license/iyume/nonebot-plugin-arcaea.svg)](https://raw.githubusercontent.com/iyume/nonebot-plugin-arcaea/main/LICENSE)

- 基于 [nonebot2](https://github.com/nonebot/nonebot2)，协议端 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

## 功能 Resume

[Arcaea](https://mzh.moegirl.org.cn/zh-hans/Arcaea) 查分器，可以实现 `best30` | `recent` | `songinfo` 之类的查询功能

## 特点 Feature

- 不配置的情况下也可使用 `b30` | `recent` 功能，默认配置下使用 [estertion](https://gist.github.com/esterTion/c673a5e2547cd54c202f129babaf601d) 维护的公开源作为查分来源

- API 可拓展性，只需编写额外的 Adapter

- 查分灵活性，可以为每个查分命令配置查分的源，见 [配置项](#可选配置项-Optional-Env)

- 以图片形式返回 `b30` | `recent`

- 抽象类为图片主题的编写提供了接口，只需要编写一个包并贡献至 `messages/themes/pkgs` 便可使用对应的图片主题，见 [开发一个主题](#准备开发-develop)

- `config` 命令允许用户设置自己查分的主题

- 为来自 [BotArcApi](https://github.com/TheSnowfield/BotArcAPI) 搭建的 API 做了适配

- `handler` 分离式设计，增加对命令处理的灵活性

## 快速开始 Quickstart

**注意**

1. 由于使用了 shell_like command，使用前请保证 `nonebot2` 处于 v2a9 以上的版本

2. 安装插件

```
(activate your virtualenv)
pip install nonebot-plugin-arcaea
```

或者

```
git clone https://github.com/iyume/nonebot-plugin-arcaea
activate your virtualenv
(cd ~/path/to/nonebot-plugin-arcaea && pip install .)
```

如果你使用的是 `nb plugin install`，此时 `bot.py` 会自动插入 `nonebot.load_plugin('nonebot_plugin_arcaea')`

若没有，请手动添加

## 指令 Command

- `/arc help` 帮助文档

- `/arc bind` 绑定账户

- `/arc info` 查询个人信息，需绑定账户，返回 文字

- `/arc recent` 查询最近游玩，返回 文字 / 图片

- `/arc b30` 查询玩家 best30，返回 文字 / 图片

- `/arc songinfo` 查询歌曲信息，返回 文字，无需注册

- `/arc config` 配置用户信息，可选 config.{$b30} / config.{$recent}

- `/arc current-config` 查询用户配置信息

## 可选配置项 Optional Env

> 大小写随意

- `ARCAEA_BOTARCAPI_URI`: 可选配置项，填写 BotArcApi 的服务器地址

- `ARCAEA_QUERY_CONFIG`: 可选配置项，填写命令查分源，格式为字典，源码有注释

- 更多设置请见源码

## 准备开发 Develop

### 准备

pip 开发模式安装 `nonebot-plugin-arcaea`

```
cd nonebot2
cd src/plugins/npa
git clone https://github.com/iyume/nonebot-plugin-arcaea
(activate virtualenv)
pip install -e .
```

插件加载单独写为一行

```
nonebot.load_plugins('src/plugins/npa')
```

### 主题开发

1. 在目录 `messages/themes/pkgs` 下新建目录，格式为 `theme_` + 你的主题名

2. 基类源码见 `messages/themes/_base.py`

3. 参数参照 `schema/api` 内的文件，也可直接查看 [BotArcApi](https://github.com/TheSnowfield/BotArcAPI/wiki) 给的传输示例，甚至因为类型提示的存在，你可以啥都不看就开始写

4. 在 `config.py` 中 `AVAILABLE_USER_CONFIG` 条目里加上你的主题包名

5. [PR](https://github.com/iyume/nonebot-plugin-arcaea/pulls)

**注意**

由于 ttf 文件会附带在源码内，请不要使用中文字体开发主题，尽量使用英文字体，后期可能会考虑限制字体类型

同样地，作为背景的图片尽量压缩 (500k以内)，不仅仅是减少源码的负担，在消息传输时过大的 `base64` 字符串容易也导致发送失败

## 特别感谢
- [Mrs4s / go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- [nonebot / nonebot2](https://github.com/nonebot/nonebot2)
- [TheSnowfield / BotArcAPI](https://github.com/TheSnowfield/BotArcAPI)
- [esterTion / arc-probe-server.php](https://gist.github.com/esterTion/c673a5e2547cd54c202f129babaf601d)
- [All Arcaea Player](https://arcaea.lowiro.com)

## 后期打算

查询 estertion 得到的 allscores 使用 fastapi 编写 endpoint 并挂载到 bot 上

为 recent 添加图片功能（包括人物之类的各种资源）

根据 estertion 中提供的查分历史配合 数据科学分析工具 来合成用户 ptt 走向

实现所有 botarcapi 中提供的 api
