import string

from .context import Context
from .defs import Token, TokenType
from .exceptions import ScannerError


class Scanner:
    def __init__(self, context: Context) -> None:
        self.context = context

    def next(self) -> str:
        if c := self.context.putback_c:
            self.context.putback_c = None
            return c

        c = self.context.infile.read(1)
        if ('\n' == c):
            self.context.line += 1
        return c

    def putback(self, c: str) -> None:
        self.context.putback_c = c

    def skip(self) -> str:
        c = self.next()
        while c and c in string.whitespace:
            c = self.next()
        return c

    def scanint(self, c: str) -> int:
        val = 0
        while c and (pos := string.digits.find(c)) >= 0:
            val = val * 10 + pos
            c = self.next()
        self.putback(c)
        return val

    def scan(self) -> Token:
        c = self.skip()
        match c:
            case '':
                return Token(TokenType.T_EOF)
            case '+':
                return Token(TokenType.T_PLUS)
            case '-':
                return Token(TokenType.T_MINUS)
            case '*':
                return Token(TokenType.T_STAR)
            case '/':
                return Token(TokenType.T_SLASH)
            case c if c.isdigit():
                return Token(TokenType.T_INTLIT, self.scanint(c))
            case _:
                msg = (f'Unrecognized character "{c}"'
                       f' on line {self.context.line}')
                raise ScannerError(msg)
