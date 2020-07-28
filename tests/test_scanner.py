from yaplox.scanner import Scanner
from yaplox.token_type import TokenType


class TestScanner:
    def test_scanner(self, mocker):
        yaplox_mock = mocker.MagicMock()

        source = "+-*"
        scanner = Scanner(source, yaplox_mock)
        tokens = scanner.scan_tokens()
        assert tokens[0].token_type == TokenType.PLUS
        assert tokens[1].token_type == TokenType.MINUS
        assert tokens[2].token_type == TokenType.STAR

        # the EOF is automatically added
        assert tokens[3].token_type == TokenType.EOF

    def test_scanner_bad_char(self, mocker):
        source = "@"
        yaplox_mock = mocker.MagicMock()
        scanner = Scanner(source, yaplox_mock)
        tokens = scanner.scan_tokens()

        # Invalid character is not added, but the EOF marker is added
        assert tokens[0].token_type == TokenType.EOF
        assert tokens[0].line == 1

        # Assert that our error code has been called
        assert yaplox_mock.error.called
        yaplox_mock.error.assert_called_once_with(1, "Unexpected character: @")

