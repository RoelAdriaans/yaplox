from typing import Any
from yaplox.token_type import TokenType


class Token:
    """
    Store parsed tokens
    """

    def __init__(self, token_type: TokenType, lexeme: str, literal: Any, line: int):
        """
        Create a new Token. In the Lox documentation `token_type` is called `type`.
        It has been renamed since `type` is a reserved keyword
        :param token_type:
        :type token_type:
        :param lexeme:
        :type lexeme:
        :param literal:
        :type literal:
        :param line:
        :type line:
        """
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"{self.token_type} {self.lexeme} {self.literal}"
