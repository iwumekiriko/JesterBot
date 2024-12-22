from src.models import Member
import math


x = 50
y = 2


def get_exp_from_lvl(level: int) -> int:
    return x * (level ** y) - (x * level)


def get_level_from_exp(exp: int) -> int:
    return int((1 + math.sqrt(1 + (4 * exp) / x)) / y)


# def get_level_from_exp(exp: int, tolerance: float = 0.001) -> int:
#     if exp < 0:
#         raise ValueError()

#     level = int( (exp / x)**(1/y)) +1 if exp > x else 1

#     while True:
#         f = get_exp_from_lvl(level) - exp
#         df = x * y * (level ** (y - 1)) - x 

#         if df == 0:
#           return int(level)

#         new_level = level - f / df
#         if abs(new_level - level) < tolerance:
#             return int(round(new_level))
#         level = new_level


def is_new_lvl(member: Member, type: str) -> tuple[bool, int]:
    from src.config import cfg

    types = {
        "message": "exp_for_message",
        "voice": "exp_for_voice_minute" 
    }

    if not member.experience:
        return False, 0
    
    received_exp = getattr(cfg.exp_cfg(member.guild_id), types[type])
    if not received_exp:
        return False, 0

    exp_before = member.experience - int(received_exp)
    exp_now = member.experience

    level_before = get_level_from_exp(exp_before)
    level_now = get_level_from_exp(exp_now)

    coins = _coins(level_now)

    return level_before < level_now, coins


def _coins(level: int) -> int:
    return 300 + 15 * level