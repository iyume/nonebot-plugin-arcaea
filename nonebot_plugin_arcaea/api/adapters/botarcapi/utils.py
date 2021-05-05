def num2songrandom(num: str) -> int:
    """
    将用户输入的随机歌曲范围参数转为发送给 API 的数字
    Algorithm: (ratingNumber * 2) + (ratingPlus ? 1 : 0)
    Example: '9+' -> 19
    """
    return int(num.rstrip('+')) * 2 + (1 if num.endswith('+') else 0)
