import math


x = 50
y = 2

def get_exp_from_lvl(level: int) -> int:
    return x * (level ** y) - (x * level)


def get_level_from_exp(exp: int) -> int:
    return int((1 + math.sqrt(1 + (4 * exp) / x)) / 2)