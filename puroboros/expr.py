from .context import Context
from .defs import ASTNode, ASTNodeType, Token, TokenType
from .exceptions import ParserError
from .scan import Scanner
from .tree import mkastleaf


def primary(tok: Token, context: Context) -> ASTNode:
    match tok.type:
        case TokenType.T_INTLIT:
            return mkastleaf(ASTNodeType.A_INTLIT, tok.intvalue)
        case _:
            raise ParserError(f'Syntax error on line {context.line}')


def arithop(tok: TokenType, context: Context) -> TokenType:
    match tok:
        case TokenType.T_PLUS:
            return ASTNodeType.A_ADD
        case TokenType.T_MINUS:
            return ASTNodeType.A_SUBTRACT
        case TokenType.T_STAR:
            return ASTNodeType.A_MULTIPLY
        case TokenType.T_SLASH:
            return ASTNodeType.A_DIVIDE
        case _:
            raise ParserError(f'Unknown token in arithop() on line {context.line}')


def binexpr(scanner: Scanner, context: Context) -> ASTNode:
    left_token = scanner.scan()
    left = primary(left_token, context)

    op_token = scanner.scan()
    if op_token.type == TokenType.T_EOF:
        return left
    nodetype = arithop(op_token.type, context)

    right = binexpr(scanner, context)

    return ASTNode(nodetype, left, right)
