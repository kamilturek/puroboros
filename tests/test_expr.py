from io import StringIO
from unittest.mock import patch

import pytest

from puroboros.defs import ASTNode, ASTNodeType, Token, TokenType
from puroboros.context import Context
from puroboros.exceptions import ParserError
from puroboros.expr import arithop, binexpr, primary
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


class TestBinaryExpression:
    def test_one_level(self):
        context = Context()
        scanner = Scanner(context)
        with patch.object(context, 'infile', StringIO('5')):
            node = binexpr(scanner, context)

        assert node == ASTNode(
            op=ASTNodeType.A_INTLIT,
            intvalue=5,
        )

    def test_two_level(self):
        """
          +
         / \
        1   3
        """
        context = Context()
        scanner = Scanner(context)
        with patch.object(context, 'infile', StringIO('1 + 3')):
            node = binexpr(scanner, context)

        assert node == ASTNode(
            op=ASTNodeType.A_ADD,
            left=ASTNode(
                op=ASTNodeType.A_INTLIT,
                intvalue=1,
            ),
            right=ASTNode(
                op=ASTNodeType.A_INTLIT,
                intvalue=3,
            ),
        )

    def test_four_level(self):
        """
          *
         / \
        2   +
           / \
          3   *
             / \
            4   5
        """
        context = Context()
        scanner = Scanner(context)
        with patch.object(context, 'infile', StringIO('2 * 3 + 4 * 5')):
            node = binexpr(scanner, context)

        assert node == ASTNode(
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
                    op=ASTNodeType.A_MULTIPLY,
                    left=ASTNode(
                        op=ASTNodeType.A_INTLIT,
                        intvalue=4,
                    ),
                    right=ASTNode(
                        op=ASTNodeType.A_INTLIT,
                        intvalue=5,
                    ),
                ),
            ),
        )
