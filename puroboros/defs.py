from dataclasses import dataclass
from enum import Enum


@dataclass
class Token:
    class Type(Enum):
        T_PLUS = 0
        T_MINUS = 1
        T_STAR = 2
        T_SLASH = 3
        T_INTLIT = 4
        T_EOF = 999

    type: Type = None
    intvalue: int = None


@dataclass
class ASTNode:
    class Type(Enum):
        A_ADD = 0
        A_SUBTRACT = 1
        A_MULTIPLY = 2
        A_DIVIDE = 3
        A_INTLIT = 4

    op: Type = None
    left: ASTNode = None
    right: ASTNode = None
    intvalue: int = None
