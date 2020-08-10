import pytest

from yaplox.ast_printer import AstPrinter
from yaplox.expr import Binary
from yaplox.parser import Parser
from yaplox.scanner import Scanner
from yaplox.token import Token
from yaplox.token_type import TokenType


class TestParser:
    def test_parser(self, mocker):
        # A 'simple' string:
        # (4 + 4) * (1 / 4) != -3.0 == "FOO" <= 7 == true != false != nil
        on_error_mock = mocker.MagicMock()

        tokens = [
            Token(token_type=TokenType.LEFT_PAREN, lexeme="(", literal=None, line=1),
            Token(token_type=TokenType.NUMBER, lexeme="4", literal=4.0, line=1),
            Token(token_type=TokenType.PLUS, lexeme="+", literal=None, line=1),
            Token(token_type=TokenType.NUMBER, lexeme="4", literal=4.0, line=1),
            Token(token_type=TokenType.RIGHT_PAREN, lexeme=")", literal=None, line=1),
            Token(token_type=TokenType.STAR, lexeme="*", literal=None, line=1),
            Token(token_type=TokenType.LEFT_PAREN, lexeme="(", literal=None, line=1),
            Token(token_type=TokenType.NUMBER, lexeme="1", literal=1.0, line=1),
            Token(token_type=TokenType.SLASH, lexeme="/", literal=None, line=1),
            Token(token_type=TokenType.NUMBER, lexeme="4", literal=4.0, line=1),
            Token(token_type=TokenType.RIGHT_PAREN, lexeme=")", literal=None, line=1),
            Token(token_type=TokenType.BANG_EQUAL, lexeme="!=", literal=None, line=1),
            Token(token_type=TokenType.MINUS, lexeme="-", literal=None, line=1),
            Token(token_type=TokenType.NUMBER, lexeme="3.0", literal=3.0, line=1),
            Token(token_type=TokenType.EQUAL_EQUAL, lexeme="==", literal=None, line=1),
            Token(token_type=TokenType.STRING, lexeme='"FOO"', literal="FOO", line=1),
            Token(token_type=TokenType.LESS_EQUAL, lexeme="<=", literal=None, line=1),
            Token(token_type=TokenType.NUMBER, lexeme="7", literal=7.0, line=1),
            Token(token_type=TokenType.EQUAL_EQUAL, lexeme="==", literal=None, line=1),
            Token(token_type=TokenType.TRUE, lexeme="true", literal=None, line=1),
            Token(token_type=TokenType.BANG_EQUAL, lexeme="!=", literal=None, line=1),
            Token(token_type=TokenType.FALSE, lexeme="false", literal=None, line=1),
            Token(token_type=TokenType.BANG_EQUAL, lexeme="!=", literal=None, line=1),
            Token(token_type=TokenType.NIL, lexeme="nil", literal=None, line=1),
            Token(token_type=TokenType.EOF, lexeme="", literal=None, line=1),
        ]

        parser = Parser(tokens, on_token_error=on_error_mock)
        expr = parser.parse()

        # There musn't be an error
        assert not on_error_mock.called

        assert isinstance(expr, Binary)
        # We can expand the whole tree by hand, or just simply convert it to
        # a string and validate that

        ast = AstPrinter().print(expr)
        expected = (
            "(!= (!= (== (== (!= (* (group (+ 4.0 4.0)) (group (/ 1.0 4.0))) "
            "(- 3.0)) (<= FOO 7.0)) True) False) nil)"
        )

        assert ast == expected

    def test_only_eof_list(self, mocker):
        # When a new line is entered, the parser expected a expression and will crash,
        # for now.
        on_error_mock = mocker.MagicMock()
        test_token = Token(token_type=TokenType.EOF, lexeme="", literal=None, line=1)

        parser = Parser([test_token], on_token_error=on_error_mock)
        expr = parser.parse()

        assert expr is None
        # There will be an error
        assert on_error_mock.called
        on_error_mock.assert_called_once_with(test_token, "Expect expression")

    def test_empty_list(self):
        # Test an empty list. This will raise an IndexError, since it's not supported,
        # and the calling party should fix this.

        parser = Parser([], on_token_error=None)

        with pytest.raises(IndexError):
            parser.parse()

    def test_missing_closing_bracket(self, mocker):
        on_scanner_error_mock = mocker.MagicMock()
        on_parser_error_mock = mocker.MagicMock()

        source = "(23+34"

        scanner = Scanner(source, on_error=on_scanner_error_mock)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, on_token_error=on_parser_error_mock)
        expr = parser.parse()

        # There will be an error. Scanner must be fine, but the error will be in the
        # parser. It will thus not return a valid expression
        assert expr is None
        assert not on_scanner_error_mock.called
        assert on_parser_error_mock.called

        on_parser_error_mock.assert_called_once_with(
            tokens[-1], "Expect ')' after expression."
        )
