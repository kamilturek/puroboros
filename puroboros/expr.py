from typing import NoReturn

from .defs import ASTNode, Token
from .exceptions import ParserError
from .scan import Scanner


class Parser:
    OP_PRECEDENCE = {
        Token.Type.T_PLUS: 10,
        Token.Type.T_MINUS: 10,
        Token.Type.T_STAR: 20,
        Token.Type.T_SLASH: 20,
    }

    def __init__(self, scanner: Scanner) -> None:
        self.scanner = scanner
        self.context = scanner.context

    def raise_syntax_error(self) -> NoReturn:
        msg = f'Syntax error on line {self.context.line}'
        raise ParserError(msg)

    def primary(self, token: Token) -> ASTNode:
        match token.type:
            case Token.Type.T_INTLIT:
                return ASTNode(
                    op=ASTNode.Type.A_INTLIT,
                    intvalue=token.intvalue,
                )
            case _:
                self.raise_syntax_error()

    def arith_op(self, token_type: Token.Type) -> ASTNode.Type:
        match token_type:
            case Token.Type.T_PLUS:
                return ASTNode.Type.A_ADD
            case Token.Type.T_MINUS:
                return ASTNode.Type.A_SUBTRACT
            case Token.Type.T_STAR:
                return ASTNode.Type.A_MULTIPLY
            case Token.Type.T_SLASH:
                return ASTNode.Type.A_DIVIDE
            case _:
                self.raise_syntax_error()

    def op_precedence(self, token_type: Token.Type) -> int:
        try:
            return self.OP_PRECEDENCE[token_type]
        except KeyError:
            self.raise_syntax_error()

    def bin_expr(self, precedence: int = 0) -> ASTNode:
        left_token = self.scanner.scan()
        left_node = self.primary(left_token)
        op_token = self.scanner.scan()

        while (
            op_token.type != Token.Type.T_EOF and
            self.op_precedence(op_token.type) > precedence
        ):
            right_node, next_op_token = self.bin_expr(self.op_precedence(op_token.type))
            left_node = ASTNode(
                op=self.arith_op(op_token.type),
                left=left_node,
                right=right_node,
            )
            op_token = next_op_token

        return left_node, op_token
