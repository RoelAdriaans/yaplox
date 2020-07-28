from typing import List, Any
from yaplox.token_type import TokenType
from yaplox.token import Token


class Scanner:
    tokens: List
    start: int = 0
    current: int = 0
    line: int = 1

    def __init__(self, source: str, yaplox: "Yaplox"):
        self.source = source
        self.yaplox = yaplox
        self.tokens = []

    def scan_tokens(self) -> List[Token]:
        while not self._is_at_end():
            # We are at the beginning of the next lexeme.
            self.start = self.current
            self._scan_token()

        self.tokens.append(
            Token(token_type=TokenType.EOF, lexeme="", literal=None, line=self.line)
        )

        return self.tokens

    def _scan_token(self):
        """ Scan tokens"""
        c = self._advance()

        # In the orginal java implementation this is implemented with a switch
        # statement. Python does not have this construct (yet), the closest thing is an
        # dict:

        token_options = {
            "(": lambda: self._add_token(TokenType.LEFT_PAREN),
            ")": lambda: self._add_token(TokenType.RIGHT_PAREN),
            "{": lambda: self._add_token(TokenType.LEFT_BRACE),
            "}": lambda: self._add_token(TokenType.RIGHT_BRACE),
            ",": lambda: self._add_token(TokenType.COMMA),
            ".": lambda: self._add_token(TokenType.DOT),
            "-": lambda: self._add_token(TokenType.MINUS),
            "+": lambda: self._add_token(TokenType.PLUS),
            ";": lambda: self._add_token(TokenType.SEMICOLON),
            "*": lambda: self._add_token(TokenType.STAR),
        }
        try:
            option = token_options[c]
            option()
        except KeyError:
            self.yaplox.error(self.line, f"Unexpected character: {c}")

    def _is_at_end(self):
        return self.current >= len(self.source)

    def _advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def _add_token(self, token_type: TokenType, literal: Any = None):
        """
        In the java implementation this method is overloaded and depending on the
        literal parameter beeing there, or not. Because python doesn't have this
        construct the overloading is handled in the method itself. As it turns out,
        this is just the default value of '=None' for the 'literal' keyword.
        """
        text = self.source[self.start : self.current]

        self.tokens.append(
            Token(token_type=token_type, lexeme=text, literal=literal, line=self.line)
        )
