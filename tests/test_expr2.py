from io import StringIO
from unittest.mock import patch

import pytest

from puroboros.context import Context
from puroboros.defs import ASTNode, ASTNodeType, Token, TokenType
from puroboros.exceptions import ParserError
from puroboros.expr2 import primary, arithop, bin_expr, multiplicative_expr, additive_expr
from puroboros.scan import Scanner


class TestPrimary:
    def test_primary_success(self):
        context = Context()
        token = Token(TokenType.T_INTLIT, 5)
        node = primary(token, context)

        assert node.op == ASTNodeType.A_INTLIT
        assert node.intvalue == 5
        assert node.left is None
        assert node.right is None

    def test_primary_failure(self):
        context = Context()
        token = Token(TokenType.T_STAR)

        with pytest.raises(ParserError) as e:
            primary(token, context)

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
    def test_arithop_success(self, token_type, expected_node_type):
        node_type = arithop(token_type, Context())

        assert node_type == expected_node_type

    def test_arithop_failure(self):
        with pytest.raises(ParserError) as e:
            arithop(TokenType.T_EOF, Context())

        assert str(e.value) == 'Unknown token in arithop() on line 1'


class TestMultiplicativeExpression:
    def test_int_literal(self):
        context = Context()
        scanner = Scanner(context)
        with patch.object(context, 'infile', StringIO('5')):
            node, op_token = multiplicative_expr(scanner, context)

        assert node == ASTNode(
            op=ASTNodeType.A_INTLIT,
            intvalue=5,
        )
        assert op_token == Token(
            type=TokenType.T_EOF,
        )

    def test_int_literal_and_additive_expression(self):
        context = Context()
        scanner = Scanner(context)
        with patch.object(context, 'infile', StringIO('5 + 4')):
            node, op_token = multiplicative_expr(scanner, context)

        assert node == ASTNode(
            op=ASTNodeType.A_INTLIT,
            intvalue=5,
        )
        assert op_token == Token(
            type=TokenType.T_PLUS,
        )

    def test_single_expression(self):
        """
          *
         / \
        2   3
        """
        context = Context()
        scanner = Scanner(context)
        with patch.object(context, 'infile', StringIO('2 * 3')):
            node, op_token = multiplicative_expr(scanner, context)

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

    def test_double_expression(self):
        """
            *
           / \
          *   4
         / \
        2   3
        """
        context = Context()
        scanner = Scanner(context)
        with patch.object(context, 'infile', StringIO('2 * 3 * 4')):
            node, op_token = multiplicative_expr(scanner, context)

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

    def test_mixed_expression(self):
        """
            +
           / \
          *   4
         / \
        2   3
        """
        context = Context()
        scanner = Scanner(context)
        with patch.object(context, 'infile', StringIO('2 * 3 + 4')):
            node, op_token = multiplicative_expr(scanner, context)

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
    def test_int_literal(self):
        """
        5
        """
        context = Context()
        scanner = Scanner(context)
        with patch.object(context, 'infile', StringIO('5')):
            node = additive_expr(scanner, context)

        assert node == ASTNode(
            op=ASTNodeType.A_INTLIT,
            intvalue=5,
        )

    def test_single_expression(self):
        """
          +
         / \
        2   3
        """
        context = Context()
        scanner = Scanner(context)
        with patch.object(context, 'infile', StringIO('2 + 3')):
            node= additive_expr(scanner, context)

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

    def test_double_expression(self):
        """
            +
           / \
          +   4
         / \
        2   3
        """
        context = Context()
        scanner = Scanner(context)
        with patch.object(context, 'infile', StringIO('2 + 3 + 4')):
            node = additive_expr(scanner, context)

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

    def test_mixed_expression(self):
        """
            +
           / \
          *   4
         / \
        2   3
        """
        context = Context()
        scanner = Scanner(context)
        with patch.object(context, 'infile', StringIO('2 * 3 + 4')):
            node = additive_expr(scanner, context)

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
