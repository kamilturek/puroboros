from io import StringIO
from unittest.mock import patch

import pytest

from puroboros.context import Context
from puroboros.defs import ASTNode, ASTNodeType, Token, TokenType
from puroboros.exceptions import ParserError
from puroboros.expr2 import RecursiveDescentParser
from puroboros.scan import Scanner


@pytest.fixture
def parser():
    context = Context()
    scanner = Scanner(context)
    parser = RecursiveDescentParser(scanner)
    return parser


class TestPrimary:
    def test_primary_success(self, parser):
        token = Token(TokenType.T_INTLIT, 5)
        node = parser.primary(token)

        assert node.op == ASTNodeType.A_INTLIT
        assert node.intvalue == 5
        assert node.left is None
        assert node.right is None

    def test_primary_failure(self, parser):
        token = Token(TokenType.T_STAR)

        with pytest.raises(ParserError) as e:
            parser.primary(token)

        assert str(e.value) == 'Syntax error on line 1'


class TestArithmeticOperator:
    @pytest.mark.parametrize(
        'token_type,expected_node_type',
        [
            (TokenType.T_PLUS, ASTNodeType.A_ADD),
            (TokenType.T_MINUS, ASTNodeType.A_SUBTRACT),
            (TokenType.T_STAR, ASTNodeType.A_MULTIPLY),
            (TokenType.T_SLASH, ASTNodeType.A_DIVIDE),
        ]
    )
    def test_arithop_success(self, parser, token_type, expected_node_type):
        node_type = parser.arith_op(token_type)

        assert node_type == expected_node_type

    def test_arithop_failure(self, parser):
        with pytest.raises(ParserError) as e:
            parser.arith_op(TokenType.T_EOF)

        assert str(e.value) == 'Unknown token on line 1'


class TestMultiplicativeExpression:
    def test_int_literal(self, parser):
        with patch.object(parser.context, 'infile', StringIO('5')):
            node, op_token = parser.multiplicative_expr()

        assert node == ASTNode(
            op=ASTNodeType.A_INTLIT,
            intvalue=5,
        )
        assert op_token == Token(
            type=TokenType.T_EOF,
        )

    def test_int_literal_and_additive_expression(self, parser):
        with patch.object(parser.context, 'infile', StringIO('5 + 4')):
            node, op_token = parser.multiplicative_expr()

        assert node == ASTNode(
            op=ASTNodeType.A_INTLIT,
            intvalue=5,
        )
        assert op_token == Token(
            type=TokenType.T_PLUS,
        )

    def test_single_expression(self, parser):
        """
          *
         / \
        2   3
        """
        with patch.object(parser.context, 'infile', StringIO('2 * 3')):
            node, op_token = parser.multiplicative_expr()

        assert node == ASTNode(
            op=ASTNodeType.A_MULTIPLY,
            left=ASTNode(
                op=ASTNodeType.A_INTLIT,
                intvalue=2,
            ),
            right=ASTNode(
                op=ASTNodeType.A_INTLIT,
                intvalue=3,
            ),
        )
        assert op_token == Token(
            type=TokenType.T_EOF,
        )

    def test_double_expression(self, parser):
        """
            *
           / \
          *   4
         / \
        2   3
        """
        with patch.object(parser.context, 'infile', StringIO('2 * 3 * 4')):
            node, op_token = parser.multiplicative_expr()

        assert node == ASTNode(
            op=ASTNodeType.A_MULTIPLY,
            left=ASTNode(
                op=ASTNodeType.A_MULTIPLY,
                left=ASTNode(
                    op=ASTNodeType.A_INTLIT,
                    intvalue=2,
                ),
                right=ASTNode(
                    op=ASTNodeType.A_INTLIT,
                    intvalue=3,
                ),
            ),
            right=ASTNode(
                op=ASTNodeType.A_INTLIT,
                intvalue=4
            ),
        )
        assert op_token == Token(
            type=TokenType.T_EOF,
        )

    def test_mixed_expression(self, parser):
        """
            +
           / \
          *   4
         / \
        2   3
        """
        with patch.object(parser.context, 'infile', StringIO('2 * 3 + 4')):
            node, op_token = parser.multiplicative_expr()

        assert node == ASTNode(
            op=ASTNodeType.A_MULTIPLY,
            left=ASTNode(
                op=ASTNodeType.A_INTLIT,
                intvalue=2,
            ),
            right=ASTNode(
                op=ASTNodeType.A_INTLIT,
                intvalue=3,
            ),
        )
        assert op_token == Token(
            type=TokenType.T_PLUS,
        )


class TestAdditiveExpression:
    def test_int_literal(self, parser):
        """
        5
        """
        with patch.object(parser.context, 'infile', StringIO('5')):
            node = parser.additive_expr()

        assert node == ASTNode(
            op=ASTNodeType.A_INTLIT,
            intvalue=5,
        )

    def test_single_expression(self, parser):
        """
          +
         / \
        2   3
        """
        with patch.object(parser.context, 'infile', StringIO('2 + 3')):
            node = parser.additive_expr()

        assert node == ASTNode(
            op=ASTNodeType.A_ADD,
            left=ASTNode(
                op=ASTNodeType.A_INTLIT,
                intvalue=2,
            ),
            right=ASTNode(
                op=ASTNodeType.A_INTLIT,
                intvalue=3,
            ),
        )

    def test_double_expression(self, parser):
        """
            +
           / \
          +   4
         / \
        2   3
        """
        with patch.object(parser.context, 'infile', StringIO('2 + 3 + 4')):
            node = parser.additive_expr()

        assert node == ASTNode(
            op=ASTNodeType.A_ADD,
            left=ASTNode(
                op=ASTNodeType.A_ADD,
                left=ASTNode(
                    op=ASTNodeType.A_INTLIT,
                    intvalue=2,
                ),
                right=ASTNode(
                    op=ASTNodeType.A_INTLIT,
                    intvalue=3,
                ),
            ),
            right=ASTNode(
                op=ASTNodeType.A_INTLIT,
                intvalue=4,
            ),
        )

    def test_mixed_expression(self, parser):
        """
            +
           / \
          *   4
         / \
        2   3
        """
        with patch.object(parser.context, 'infile', StringIO('2 * 3 + 4')):
            node = parser.additive_expr()
# 
        assert node == ASTNode(
            op=ASTNodeType.A_ADD,
            left=ASTNode(
                op=ASTNodeType.A_MULTIPLY,
                left=ASTNode(
                    op=ASTNodeType.A_INTLIT,
                    intvalue=2,
                ),
                right=ASTNode(
                    op=ASTNodeType.A_INTLIT,
                    intvalue=3,
                ),
            ),
            right=ASTNode(
                op=ASTNodeType.A_INTLIT,
                intvalue=4,
            ),
        )
