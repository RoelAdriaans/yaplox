from yaplox.token import Token
from yaplox.token_type import TokenType


def test_token_factory(create_token_factory):
    minus = create_token_factory(token_type=TokenType.MINUS)

    assert isinstance(minus, Token)
    assert minus.token_type == TokenType.MINUS
    assert minus.lexeme == "-"
    assert minus.line == 1
