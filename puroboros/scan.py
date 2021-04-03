import string

from .defs import Token, TokenType


putback_c = None
infile = None
line = None


def next() -> str:
    global putback_c
    global line

    if putback_c:
        c = putback_c
        putback_c = 0
        return c

    c = infile.read(1)
    if ('\n' == c):
        line += 1

    return c


def putback(c: str) -> None:
    global putback_c
    putback_c = c


def skip() -> str:
    c = next()
    while len(c) > 0 and c in string.whitespace:
        c = next()
    return c


def scanint(c: str):
    val = 0
    while (k := '0123456789'.find(c)) >= 0:
        val = val * 10 + k
        c = next()
        if c == '':
            break
    putback(c)
    return val


def scan(token: Token) -> bool:
    c = skip()
    match c:
        case '':
            return False
        case '+':
            token.type = TokenType.T_PLUS
        case '-':
            token.type = TokenType.T_MINUS
        case '*':
            token.type = TokenType.T_STAR
        case '/':
            token.type = TokenType.T_SLASH
        case c if c.isdigit():
            token.intvalue = scanint(c)
            token.type = TokenType.T_INTLIT
        case _:
            print(f'Unrecognized character {c} on line {line}')
            return False
    return True
