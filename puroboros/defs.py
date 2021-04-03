from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    T_PLUS = 0
    T_MINUS = 1
    T_STAR = 2
    T_SLASH = 3
    T_INTLIT = 4


@dataclass
class Token:
    type: TokenType = None
    intvalue: int = None
