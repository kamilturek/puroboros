from io import StringIO
from unittest.mock import patch

import pytest

from puroboros.context import Context
from puroboros.defs import Token
from puroboros.exceptions import ScannerError
from puroboros.scan import Scanner


class TestScan:
    @pytest.mark.parametrize(
        'infile_value,expected_token',
        [
            ('', Token(Token.Type.T_EOF)),
            ('+', Token(Token.Type.T_PLUS)),
            ('-', Token(Token.Type.T_MINUS)),
            ('*', Token(Token.Type.T_STAR)),
            ('/', Token(Token.Type.T_SLASH)),
            ('1', Token(Token.Type.T_INTLIT, 1)),
            ('21', Token(Token.Type.T_INTLIT, 21)),
            ('321', Token(Token.Type.T_INTLIT, 321)),
            ('4321', Token(Token.Type.T_INTLIT, 4321)),
            ('54321', Token(Token.Type.T_INTLIT, 54321)),
        ]
    )
    def test_scan(self, infile_value, expected_token):
        context = Context()
        scanner = Scanner(context)
        with patch.object(context, 'infile', StringIO(infile_value)):
            token = scanner.scan()

        assert token == expected_token

    def test_scan_newline(self):
        context = Context()
        scanner = Scanner(context)
        with patch.object(context, 'infile', StringIO('\n')):
            scanner.scan()
        
        assert context.line == 2

    def test_raises_scanner_error_on_unrecognized_character(self):
        context = Context()
        scanner = Scanner(context)
        with (
            patch.object(context, 'infile', StringIO('#')),
            pytest.raises(ScannerError) as e
        ):
            scanner.scan()

        assert str(e.value) == 'Unrecognized character "#" on line 1'
