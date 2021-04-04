from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    T_PLUS = 0
    T_MINUS = 1
    T_STAR = 2
    T_SLASH = 3
    T_INTLIT = 4
    T_EOF = 999


@dataclass
class Token:
    type: TokenType = None
    intvalue: int = None


class ASTNodeType(Enum):
    A_ADD = 0
    A_SUBTRACT = 1
    A_MULTIPLY = 2
    A_DIVIDE = 3
    A_INTLIT = 4


@dataclass
class ASTNode:
    op: ASTNodeType = None
    left: ASTNode = None
    right: ASTNode = None
    intvalue: int = None
