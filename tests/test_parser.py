import pytest

from yaplox.ast_printer import AstPrinter
from yaplox.expr import Binary
from yaplox.parser import Parser
from yaplox.scanner import Scanner
from yaplox.stmt import Expression
from yaplox.token import Token
from yaplox.token_type import TokenType


class TestParser:
    def test_parser(self, mocker):
        # A 'simple' string:
        # (4 + 4) * (1 / 4) != -3.0 == "FOO" == true != false != nil;
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
            Token(token_type=TokenType.EQUAL_EQUAL, lexeme="==", literal=None, line=1),
            Token(token_type=TokenType.TRUE, lexeme="true", literal=None, line=1),
            Token(token_type=TokenType.BANG_EQUAL, lexeme="!=", literal=None, line=1),
            Token(token_type=TokenType.FALSE, lexeme="false", literal=None, line=1),
            Token(token_type=TokenType.BANG_EQUAL, lexeme="!=", literal=None, line=1),
            Token(token_type=TokenType.NIL, lexeme="nil", literal=None, line=1),
            Token(token_type=TokenType.SEMICOLON, lexeme=";", literal=None, line=1),
            Token(token_type=TokenType.EOF, lexeme="", literal=None, line=1),
        ]

        parser = Parser(tokens, on_token_error=on_error_mock)
        statements = parser.parse()
        expr = statements[0].expression

        # There musn't be an error
        assert not on_error_mock.called

        # The first statement will be Binary
        assert isinstance(expr, Binary)
        # We can expand the whole tree by hand, or just simply convert it to
        # a string and validate that

        ast = AstPrinter().print(expr)
        expected = (
            "(!= (!= (== (== (!= (* (group (+ 4.0 4.0)) (group (/ 1.0 4.0))) "
            "(- 3.0)) FOO) True) False) nil)"
        )

        assert ast == expected

    def test_only_eof_list(self, mocker):
        # When a new line is entered, there aren't any statements, and the parser will
        # return an empty list. No errors are raised

        on_error_mock = mocker.MagicMock()
        test_token = Token(token_type=TokenType.EOF, lexeme="", literal=None, line=1)

        parser = Parser([test_token], on_token_error=on_error_mock)
        statements = parser.parse()

        assert statements == []

        # No errors
        assert not on_error_mock.called

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
        statements = parser.parse()

        # There will be an error. Scanner must be fine, but the error will be in the
        # parser. There will be no statements generated
        assert statements == []
        assert not on_scanner_error_mock.called
        assert on_parser_error_mock.called

        on_parser_error_mock.assert_called_once_with(
            tokens[-1], "Expect ')' after expression."
        )

    def test_parser_synchronize(self, mocker):
        on_scanner_error_mock = mocker.MagicMock()
        on_parser_error_mock = mocker.MagicMock()

        lines = [
            "var a = 4;",
            "print (4+3;",
            "a = 5;",
            "",
            "var a = (3/4",
            "print (a);",
        ]
        source = "\n".join(lines)
        scanner = Scanner(source, on_error=on_scanner_error_mock)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, on_token_error=on_parser_error_mock)
        statements = parser.parse()

        # We validate that the error is called, the real values are tested in
        # test_missing_closing_bracket
        assert not on_scanner_error_mock.called
        assert on_parser_error_mock.called

        # Assert that the third statement is sane and that the parser continues after
        # errors
        assert isinstance(statements[1], Expression)
        assert statements[1].expression.name.line == 3
        assert statements[1].expression.name.lexeme == "a"

    def test_invalid_assignment(self, mocker):
        """
        An identifiers must start with a letter [a-z], numbers are invalid and
        must raise an error
        """
        on_scanner_error_mock = mocker.MagicMock()
        on_parser_error_mock = mocker.MagicMock()

        expression = "var 0123foobar = 34;"

        scanner = Scanner(expression, on_error=on_scanner_error_mock)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, on_token_error=on_parser_error_mock)
        statements = parser.parse()

        assert statements == []
        assert not on_scanner_error_mock.called
        assert on_parser_error_mock.called

        on_parser_error_mock.assert_called_once_with(tokens[1], "Expect variable name.")
