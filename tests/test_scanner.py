import pytest

from yaplox.scanner import Scanner
from yaplox.token_type import TokenType


class TestScanner:
    def test_always_fail(self):
        assert False

    def test_scanner(self, mocker):
        on_error_mock = mocker.MagicMock()

        source = "+-\n*"
        scanner = Scanner(source, on_error=on_error_mock)
        tokens = scanner.scan_tokens()
        assert tokens[0].token_type == TokenType.PLUS
        assert tokens[1].token_type == TokenType.MINUS
        assert tokens[2].token_type == TokenType.STAR

        # the EOF is automatically added
        assert tokens[3].token_type == TokenType.EOF

        # The newline char (\n) doesn't add a token, but increments the line counter
        assert scanner.line == 2

        # There mustn't be an error
        assert not on_error_mock.called

    @pytest.mark.parametrize(
        ("source", "expected_output_list"),
        [
            ("+-*", [TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.EOF]),
            ("!=", [TokenType.BANG_EQUAL, TokenType.EOF]),
            ("!", [TokenType.BANG, TokenType.EOF]),
            ("==", [TokenType.EQUAL_EQUAL, TokenType.EOF]),
            ("=", [TokenType.EQUAL, TokenType.EOF]),
            ("===", [TokenType.EQUAL_EQUAL, TokenType.EQUAL, TokenType.EOF]),
            (">", [TokenType.GREATER, TokenType.EOF]),
            (">=", [TokenType.GREATER_EQUAL, TokenType.EOF]),
            ("<", [TokenType.LESS, TokenType.EOF]),
            ("<=", [TokenType.LESS_EQUAL, TokenType.EOF]),
            ("/", [TokenType.SLASH, TokenType.EOF]),
            (" ", [TokenType.EOF]),
            ("\n", [TokenType.EOF]),
            (
                "*// This is a comment\n=",
                [TokenType.STAR, TokenType.EQUAL, TokenType.EOF],
            ),
            # Testcases/Examples from the book
            ("// this is a comment", [TokenType.EOF]),
            (
                "(( )){} // grouping stuff",
                [
                    TokenType.LEFT_PAREN,
                    TokenType.LEFT_PAREN,
                    TokenType.RIGHT_PAREN,
                    TokenType.RIGHT_PAREN,
                    TokenType.LEFT_BRACE,
                    TokenType.RIGHT_BRACE,
                    TokenType.EOF,
                ],
            ),
            (
                "!*+-/=<> <= == // operators",
                [
                    TokenType.BANG,
                    TokenType.STAR,
                    TokenType.PLUS,
                    TokenType.MINUS,
                    TokenType.SLASH,
                    TokenType.EQUAL,
                    TokenType.LESS,
                    TokenType.GREATER,
                    TokenType.LESS_EQUAL,
                    TokenType.EQUAL_EQUAL,
                    TokenType.EOF,
                ],
            ),
        ],
    )
    def test_scanner_operator(self, source, expected_output_list, mocker):
        on_error_mock = mocker.MagicMock()

        scanner = Scanner(source, on_error=on_error_mock)
        tokens = scanner.scan_tokens()

        # Retrieve the token_types from the created tokens
        token_types = [token.token_type for token in tokens]

        assert token_types == expected_output_list
        assert not on_error_mock.called

    def test_scanner_bad_char(self, mocker):
        source = "@"
        on_error_mock = mocker.MagicMock()
        scanner = Scanner(source, on_error=on_error_mock)
        tokens = scanner.scan_tokens()

        # Invalid character is not added, but the EOF marker is added
        assert tokens[0].token_type == TokenType.EOF
        assert tokens[0].line == 1

        # Assert that our error code has been called
        assert on_error_mock.called
        on_error_mock.assert_called_once_with(1, "Unexpected character: @")

    def test_scanner_bad_char_without_callback(self):
        source = "@"
        scanner = Scanner(source)
        with pytest.raises(KeyError):
            scanner.scan_tokens()

    def test_scanner_with_string(self, mocker):
        source = '+"This is a String"'
        on_error_mock = mocker.MagicMock()
        scanner = Scanner(source, on_error=on_error_mock)
        tokens = scanner.scan_tokens()

        assert tokens[0].token_type == TokenType.PLUS
        assert tokens[1].token_type == TokenType.STRING
        assert tokens[1].literal == "This is a String"
        assert tokens[2].token_type == TokenType.EOF

        assert not on_error_mock.called

    def test_scanner_with_unterminated_string(self, mocker):
        source = '+"This is a Unterminated String'
        on_error_mock = mocker.MagicMock()
        scanner = Scanner(source, on_error=on_error_mock)

        tokens = scanner.scan_tokens()

        # Validate that all the default tokens have been added
        assert tokens[0].token_type == TokenType.PLUS
        assert tokens[1].token_type == TokenType.EOF

        # Assert that our error code has been called
        assert on_error_mock.called
        on_error_mock.assert_called_once_with(1, "Unterminated string.")

    def test_scanner_with_multiline_string(self, mocker):
        source = "This is an \nMulti-\nline-string"
        source_input = f'"{source}"'

        on_error_mock = mocker.MagicMock()
        scanner = Scanner(source_input, on_error=on_error_mock)

        tokens = scanner.scan_tokens()
        assert tokens[0].token_type == TokenType.STRING
        assert tokens[0].literal == source
        assert not on_error_mock.called

        # We have traveled three lines
        assert scanner.line == 3

    def test_scanner_with_number(self, mocker):
        source = "123 12.23 3+5 13."

        on_error_mock = mocker.MagicMock()
        scanner = Scanner(source, on_error=on_error_mock)

        tokens = scanner.scan_tokens()
        assert tokens[0].token_type == TokenType.NUMBER
        assert tokens[0].literal == 123.0

        assert tokens[1].token_type == TokenType.NUMBER
        assert tokens[1].literal == 12.23

        assert tokens[2].token_type == TokenType.NUMBER
        assert tokens[2].literal == 3.0

        assert tokens[3].token_type == TokenType.PLUS

        assert tokens[4].token_type == TokenType.NUMBER
        assert tokens[4].literal == 5.0

        assert tokens[5].token_type == TokenType.NUMBER
        assert tokens[5].literal == 13.0

        assert not on_error_mock.called

    def test_scanner_identifier(self, mocker):
        source = "appelflap or nil if while _foo_bar_1_2"

        on_error_mock = mocker.MagicMock()
        scanner = Scanner(source, on_error=on_error_mock)

        tokens = scanner.scan_tokens()

        assert tokens[0].token_type == TokenType.IDENTIFIER
        assert tokens[0].lexeme == "appelflap"

        assert tokens[1].token_type == TokenType.OR
        assert tokens[2].token_type == TokenType.NIL
        assert tokens[3].token_type == TokenType.IF
        assert tokens[4].token_type == TokenType.WHILE

        assert tokens[5].token_type == TokenType.IDENTIFIER
        assert tokens[5].lexeme == "_foo_bar_1_2"

        assert not on_error_mock.called

    def test_scanner_invalid_identifier(self, mocker):
        # The bit of source code below is completely wrong, and identifies and
        # numbers in here will not result in valid tokens, but not the tokens you
        # would expect. This is not a problem of the scanner, it just does as it's
        # told.
        source = "123foo_bar bar-stool spam_egg_1.3_chickens"

        on_error_mock = mocker.MagicMock()
        scanner = Scanner(source, on_error=on_error_mock)

        tokens = scanner.scan_tokens()

        assert tokens[0].literal == 123.0

        assert tokens[1].lexeme == "foo_bar"
        assert tokens[1].token_type == TokenType.IDENTIFIER

        assert tokens[2].lexeme == "bar"
        assert tokens[2].token_type == TokenType.IDENTIFIER

        assert tokens[3].token_type == TokenType.MINUS

        assert tokens[4].lexeme == "stool"
        assert tokens[5].lexeme == "spam_egg_1"
        assert tokens[6].token_type == TokenType.DOT

        # This token did not consume the 1 before, since that was still part of the
        # valid identifier. The dot broke the identifier, and then a number started
        assert tokens[7].token_type == TokenType.NUMBER
        assert tokens[7].literal == 3.0

        assert tokens[8].lexeme == "_chickens"

        assert not on_error_mock.called
