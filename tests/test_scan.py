from io import StringIO
from unittest.mock import patch

import pytest

from puroboros.context import Context
from puroboros.defs import Token, TokenType
from puroboros.scan import Scanner


class TestScan:

    @pytest.mark.parametrize(
        'infile_value,expected_token',
        [
            ('+', Token(TokenType.T_PLUS)),
            ('-', Token(TokenType.T_MINUS)),
            ('*', Token(TokenType.T_STAR)),
            ('/', Token(TokenType.T_SLASH)),
            ('1', Token(TokenType.T_INTLIT, 1)),
            ('21', Token(TokenType.T_INTLIT, 21)),
            ('321', Token(TokenType.T_INTLIT, 321)),
            ('4321', Token(TokenType.T_INTLIT, 4321)),
            ('54321', Token(TokenType.T_INTLIT, 54321)),
        ]
    )
    def test_scan(self, infile_value, expected_token):
        context = Context()
        scanner = Scanner(context)
        token = Token()
        with patch.object(context, 'infile', StringIO(infile_value)):
            scanner.scan(token)

        assert token == expected_token
