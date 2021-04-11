from io import StringIO
from unittest.mock import patch

import pytest

from puroboros.context import Context
from puroboros.defs import ASTNode, Token
from puroboros.exceptions import ParserError
from puroboros.expr import Parser
from puroboros.scan import Scanner


@pytest.fixture
def parser():
    context = Context()
    scanner = Scanner(context)
    parser = Parser(scanner)
    return parser


class TestParserSyntaxError:
    def test_raises_syntax_error(self, parser):
        parser.context.line = 10
        with pytest.raises(ParserError) as e:
            parser.raise_syntax_error()
        
        assert str(e.value) == 'Syntax error on line 10'


class TestPrimary:
    def test_primary_success(self, parser):
        token = Token(Token.Type.T_INTLIT, 5)
        node = parser.primary(token)

        assert node.op == ASTNode.Type.A_INTLIT
        assert node.intvalue == 5
        assert node.left is None
        assert node.right is None

    def test_primary_failure(self, parser):
        token = Token(Token.Type.T_STAR)

        with pytest.raises(ParserError) as e:
            parser.primary(token)

        assert str(e.value) == 'Syntax error on line 1'


class TestArithmeticOperator:
    @pytest.mark.parametrize(
        'token_type,expected_node_type',
        [
            (Token.Type.T_PLUS, ASTNode.Type.A_ADD),
            (Token.Type.T_MINUS, ASTNode.Type.A_SUBTRACT),
            (Token.Type.T_STAR, ASTNode.Type.A_MULTIPLY),
            (Token.Type.T_SLASH, ASTNode.Type.A_DIVIDE),
        ]
    )
    def test_arithop_success(self, parser, token_type, expected_node_type):
        node_type = parser.arith_op(token_type)

        assert node_type == expected_node_type

    def test_arithop_failure(self, parser):
        with pytest.raises(ParserError) as e:
            parser.arith_op(Token.Type.T_EOF)

        assert str(e.value) == 'Syntax error on line 1'


class TestBinaryExpression:
    def test_int_literal(self, parser):
        with patch.object(parser.context, 'infile', StringIO('1')):
            node, op_token = parser.bin_expr()
    
        assert node == ASTNode(
            op=ASTNode.Type.A_INTLIT,
            intvalue=1,
        )
        assert op_token == Token(
            type=Token.Type.T_EOF,
        )

    def test_additive_expr(self, parser):
        """
          +
         / \
        1   2
        """
        with patch.object(parser.context, 'infile', StringIO('1 + 2')):
            node, op_token = parser.bin_expr()

        assert node == ASTNode(
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
        assert op_token == Token(
            type=Token.Type.T_EOF,
        )

    def test_double_additive_expr(self, parser):
        """
            +
           / \
          +   3
         / \
        1   2
        """
        with patch.object(parser.context, 'infile', StringIO('1 + 2 + 3')):
            node, op_token = parser.bin_expr()
        
        assert node == ASTNode(
            op=ASTNode.Type.A_ADD,
            left=ASTNode(
                op=ASTNode.Type.A_ADD,
                left=ASTNode(
                    op=ASTNode.Type.A_INTLIT,
                    intvalue=1,
                ),
                right=ASTNode(
                    op=ASTNode.Type.A_INTLIT,
                    intvalue=2,
                ),
            ),
            right=ASTNode(
                op=ASTNode.Type.A_INTLIT,
                intvalue=3,
            ),
        )
        assert op_token == Token(
            type=Token.Type.T_EOF,
        )

    def test_multiplicative_expr(self, parser):
        """
          *
         / \
        1   2
        """
        with patch.object(parser.context, 'infile', StringIO('1 * 2')):
            node, op_token = parser.bin_expr()

        assert node == ASTNode(
            op=ASTNode.Type.A_MULTIPLY,
            left=ASTNode(
                op=ASTNode.Type.A_INTLIT,
                intvalue=1,
            ),
            right=ASTNode(
                op=ASTNode.Type.A_INTLIT,
                intvalue=2,
            ),
        )
        assert op_token == Token(
            type=Token.Type.T_EOF,
        )

    def test_double_multiplicative_expr(self, parser):
        """
            *
           / \
          *   3
         / \
        1   2
        """
        with patch.object(parser.context, 'infile', StringIO('1 * 2 * 3')):
             node, op_token = parser.bin_expr()

        assert node == ASTNode(
            op=ASTNode.Type.A_MULTIPLY,
            left=ASTNode(
                op=ASTNode.Type.A_MULTIPLY,
                left=ASTNode(
                    op=ASTNode.Type.A_INTLIT,
                    intvalue=1,
                ),
                right=ASTNode(
                    op=ASTNode.Type.A_INTLIT,
                    intvalue=2,
                ),
            ),
            right=ASTNode(
                op=ASTNode.Type.A_INTLIT,
                intvalue=3
            ),
        )
        assert op_token == Token(
            type=Token.Type.T_EOF,
        )

    def test_mixed_expr(self, parser):
        """
            +
           / \
          *   3
         / \
        1   2
        """
        with patch.object(parser.context, 'infile', StringIO('1 * 2 + 3')):
            node, op_token = parser.bin_expr()

        assert node == ASTNode(
            op=ASTNode.Type.A_ADD,
            left=ASTNode(
                op=ASTNode.Type.A_MULTIPLY,
                left=ASTNode(
                    op=ASTNode.Type.A_INTLIT,
                    intvalue=1,
                ),
                right=ASTNode(
                    op=ASTNode.Type.A_INTLIT,
                    intvalue=2,
                ),
            ),
            right=ASTNode(
                op=ASTNode.Type.A_INTLIT,
                intvalue=3,
            )
        )
