from puroboros.defs import ASTNode, ASTNodeType
from puroboros.interp import interpret_ast


class TestInterpreter:
    def test_int_literal(self):
        node = ASTNode(
            op=ASTNodeType.A_INTLIT,
            intvalue=5,
        )
        val = interpret_ast(node)

        assert val == 5

    def test_one_arithmetic_expression(self):
        """
        1 + 2
        """
        node = ASTNode(
            op=ASTNodeType.A_ADD,
            left=ASTNode(
                op=ASTNodeType.A_INTLIT,
                intvalue=1,
            ),
            right=ASTNode(
                op=ASTNodeType.A_INTLIT,
                intvalue=2,
            ),
        )
        val = interpret_ast(node)

        assert val == 3

    def test_two_arithmetic_expressions(self):
        """
        2 * 3 + 5
        """
        node = ASTNode(
            op=ASTNodeType.A_MULTIPLY,
            left=ASTNode(
                op=ASTNodeType.A_INTLIT,
                intvalue=2,
            ),
            right=ASTNode(
                op=ASTNodeType.A_ADD,
                left=ASTNode(
                    op=ASTNodeType.A_INTLIT,
                    intvalue=3,
                ),
                right=ASTNode(
                    op=ASTNodeType.A_INTLIT,
                    intvalue=5,
                ),
            ),
        )
        val = interpret_ast(node)

        assert val == 16
