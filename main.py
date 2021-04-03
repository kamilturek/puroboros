import sys

from puroboros import scan
from puroboros.defs import Token, TokenType


def init():
    scan.putback_c = None
    scan.infile = None
    scan.line = 1


tok_str = {
    TokenType.T_PLUS: '+',
    TokenType.T_MINUS: '-',
    TokenType.T_STAR: '*',
    TokenType.T_SLASH: '/',
    TokenType.T_INTLIT: 'intlit'
}


def scanfile():
    token = Token()
    while scan.scan(token):
        print(f'Token {tok_str[token.type]}', end='')
        if (token.type == TokenType.T_INTLIT):
            print(f', value {token.intvalue}', end='')
        print()


if __name__ == '__main__':
    init()

    with open(sys.argv[1], 'rt') as fi:
        scan.infile = fi
        scanfile()
