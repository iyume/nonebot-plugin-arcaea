from nonebot.rule import ArgumentParser


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('cmd')
    return parser
