def num2diffstr(num: int) -> str:
    return { 0: 'PST', 1: 'PRS', 2: 'FTR', 3: 'BYD' }.get(num, 'unknown')
