from typing import Optional

import pytest

from yaplox.token import Token
from yaplox.token_type import TokenType


@pytest.fixture
def create_token_factory():
    """
    Create a token_factory. Since fixtures cannot use parametes, this
    fixture created the token_factory function and returns it. See test_conftest.py
    for the usage of this fixture.
    """

    def token_factory(
        token_type: TokenType,
        lexeme: Optional[str] = None,
        literal: Optional[str] = None,
        line: Optional[int] = 1,
    ) -> Token:
        values = {
            "token_type": token_type,
            "lexeme": lexeme,
            "literal": literal,
            "line": line,
        }
        tokens = {
            TokenType.MINUS: {"lexeme": "-"},
            TokenType.BANG: {"lexeme": "!"},
            TokenType.SLASH: {"lexeme": "/"},
            TokenType.STAR: {"lexeme": "*"},
            TokenType.PLUS: {"lexeme": "+"},
        }

        values.update(tokens.get(token_type, []))

        token = Token(**values)
        return token

    return token_factory