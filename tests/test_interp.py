from puroboros.defs import ASTNode
from puroboros.interp import interpret_ast


class TestInterpreter:
    def test_int_literal(self):
        node = ASTNode(
            op=ASTNode.Type.A_INTLIT,
            intvalue=5,
        )
        val = interpret_ast(node)

        assert val == 5

    def test_one_arithmetic_expression(self):
        """
        1 + 2
        """
        node = ASTNode(
            op=ASTNode.Type.A_ADD,
            left=ASTNode(
                op=ASTNode.Type.A_INTLIT,
                intvalue=1,
            ),
            right=ASTNode(
                op=ASTNode.Type.A_INTLIT,
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
            op=ASTNode.Type.A_MULTIPLY,
            left=ASTNode(
                op=ASTNode.Type.A_INTLIT,
                intvalue=2,
            ),
            right=ASTNode(
                op=ASTNode.Type.A_ADD,
                left=ASTNode(
                    op=ASTNode.Type.A_INTLIT,
                    intvalue=3,
                ),
                right=ASTNode(
                    op=ASTNode.Type.A_INTLIT,
                    intvalue=5,
                ),
            ),
        )
        val = interpret_ast(node)

        assert val == 16
