"""
Recursive Descent Parser
Alternative, not used parser implementation
"""

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


def multiplicative_expr(scanner: Scanner, context: Context) -> tuple[ASTNode, TokenType]:
    """
    Returns an AST tree whose root is a '*' or '/' binary operator
    and next not parsed token
    """
    left_token = scanner.scan()
    left_node = primary(left_token, context)

    op_token = scanner.scan()
    if op_token.type == TokenType.T_EOF:
        return left_node, op_token

    while op_token.type in [TokenType.T_STAR, TokenType.T_SLASH]:
        right_token = scanner.scan()
        right_node = primary(right_token, context)
        left_node = ASTNode(
            arithop(op_token.type, context),
            left_node, right_node,
        )
        op_token = scanner.scan()

    return left_node, op_token


def additive_expr(scanner: Scanner, context: Context) -> ASTNode:
    """
    Returns an AST tree whose root is a '+' or '-' binary operator
    """
    left_node, op_token = multiplicative_expr(scanner, context)
    if op_token.type == TokenType.T_EOF:
        return left_node
    
    while op_token.type in [TokenType.T_PLUS, TokenType.T_MINUS]:
        right_node, next_op_token = multiplicative_expr(scanner, context)
        left_node = ASTNode(
            arithop(op_token.type, context),
            left_node, right_node
        )
        op_token = next_op_token

    return left_node


def bin_expr(scanner: Scanner, context: Context) -> ASTNode:
    return additive_expr(scanner, context)
