import pytest

from yaplox.scanner import Scanner
from yaplox.token_type import TokenType


class TestScanner:
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

        # There musn't be an error
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
