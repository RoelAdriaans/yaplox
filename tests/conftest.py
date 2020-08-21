import pytest

from yaplox.token_type import TokenType
from yaplox.token import Token


@pytest.fixture
def create_token(token_type: TokenType, lexime=None, literal=None, line=None):

    tokens = {
        TokenType.MINUS: {"token_type": TokenType.MINUS, "lexime": "-"},
    }

    values = tokens[token_type]

    token = Token(**values)
    return token
