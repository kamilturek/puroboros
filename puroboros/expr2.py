from .defs import ASTNode, ASTNodeType, Token, TokenType
from .exceptions import ParserError
from .scan import Scanner
from .tree import mkastleaf


class RecursiveDescentParser:
    """Alternative parser implementation"""

    def __init__(self, scanner: Scanner) -> None:
        self.scanner = scanner
        self.context = scanner.context

    def binary_expr(self) -> ASTNode:
        return self.additive_expr()

    def additive_expr(self) -> ASTNode:
        """
        Returns an AST tree whose root is a '+' or '-' binary operator
        """
        left_node, op_token = self.multiplicative_expr()

        while op_token.type in [TokenType.T_PLUS, TokenType.T_MINUS]:
            right_node, next_op_token = self.multiplicative_expr()
            left_node = ASTNode(
                op=self.arith_op(op_token.type),
                left=left_node,
                right=right_node,
            )
            op_token = next_op_token

        return left_node

    def multiplicative_expr(self) -> tuple[ASTNode, Token]:
        """
        Returns an AST tree whose root is a '*' or '/' binary operator
        and next not parsed token
        """
        left_token = self.scanner.scan()
        left_node = self.primary(left_token)
        op_token = self.scanner.scan()

        while op_token.type in [TokenType.T_STAR, TokenType.T_SLASH]:
            right_token = self.scanner.scan()
            right_node = self.primary(right_token)
            left_node = ASTNode(
                op=self.arith_op(op_token.type),
                left=left_node,
                right=right_node,
            )
            op_token = self.scanner.scan()

        return left_node, op_token

    def primary(self, token: Token) -> ASTNode:
        match token.type:
            case TokenType.T_INTLIT:
                return mkastleaf(ASTNodeType.A_INTLIT, token.intvalue)
            case _:
                raise ParserError(f'Syntax error on line {self.context.line}')

    def arith_op(self, token_type: TokenType) -> ASTNodeType:
        match token_type:
            case TokenType.T_PLUS:
                return ASTNodeType.A_ADD
            case TokenType.T_MINUS:
                return ASTNodeType.A_SUBTRACT
            case TokenType.T_STAR:
                return ASTNodeType.A_MULTIPLY
            case TokenType.T_SLASH:
                return ASTNodeType.A_DIVIDE
            case _:
                msg = f'Unknown token on line {self.context.line}'
                raise ParserError(msg)
