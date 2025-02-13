from src.models import Member
from enum import Enum
import math


BASE_COINS = 300
COINS_GRADATION = 15
EXP_COEFF = 50
LEVEL_EXPONENT = 2


class ExpTypes(str, Enum):
    MESSAGE = "exp_for_message"
    VOICE = "exp_for_voice_minute"

    def __str__(self) -> str:
        return self.value


def get_exp_from_lvl(level: int) -> int:
    return EXP_COEFF * (level ** LEVEL_EXPONENT) - (EXP_COEFF * level)


def get_level_from_exp(exp: int) -> int:
    return int((1 + math.sqrt(1 + (4 * exp) / EXP_COEFF)) / LEVEL_EXPONENT)


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


def is_new_lvl(member: Member, type: ExpTypes) -> tuple[bool, int]:
    from src.config import cfg

    if not member.experience:
        return False, 0

    received_exp = getattr(cfg.exp_cfg(member.guild_id), str(type))
    if not received_exp:
        return False, 0

    exp_before = member.experience - int(received_exp)
    exp_now = member.experience

    level_before = get_level_from_exp(exp_before)
    level_now = get_level_from_exp(exp_now)

    coins = _coins(level_now)

    return level_before < level_now, coins


def _coins(level: int) -> int:
    return BASE_COINS + COINS_GRADATION * level
