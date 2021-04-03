import sys

from puroboros.context import Context
from puroboros.defs import Token, TokenType
from puroboros.scan import Scanner


tok_str = {
    TokenType.T_PLUS: '+',
    TokenType.T_MINUS: '-',
    TokenType.T_STAR: '*',
    TokenType.T_SLASH: '/',
    TokenType.T_INTLIT: 'intlit'
}


def scanfile(context: Context) -> None:
    scanner = Scanner(context)
    token = Token()
    while scanner.scan(token):
        print(f'Token {tok_str[token.type]}', end='')
        if (token.type == TokenType.T_INTLIT):
            print(f', value {token.intvalue}', end='')
        print()


if __name__ == '__main__':
    context = Context()

    with open(sys.argv[1], 'rt') as fi:
        context.infile = fi
        scanfile(context)
