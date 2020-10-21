from typing import Any, Callable, Dict, List

from yaplox.token import Token
from yaplox.token_type import TokenType


class Scanner:
    tokens: List
    start: int = 0
    current: int = 0
    line: int = 1
    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source: str, on_error=None):
        """
        Create a new scanner that will scan the variable 'source'.
        'on_error' will be called when we encounter an error.
        """
        self.source = source
        self.on_error = on_error
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

    def _operator_slash(self):
        if self._match("/"):
            # A comment goes until the the of the line
            while self._peek() != "\n" and not self._is_at_end():
                self._advance()
        else:
            self._add_token(TokenType.SLASH)

    def _operator_newline(self):
        self.line += 1

    def _string(self):
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                self.line += 1
            self._advance()

        # Unterminated string
        if self._is_at_end():
            self.on_error(self.line, "Unterminated string.")
            return

        # The closing "
        self._advance()

        # Trim the surrounding "
        string_value = self.source[self.start + 1 : self.current - 1]
        self._add_token(TokenType.STRING, string_value)

    def _number(self):
        while self._peek().isdigit():
            self._advance()

        # Look for a fractional part
        if self._peek() == "." and self._peek_next().isdigit():
            # Consume the '.'
            self._advance()
            # Consume the fraction
            while self._peek().isdigit():
                self._advance()

        number_value = self.source[self.start : self.current]
        self._add_token(TokenType.NUMBER, float(number_value))

    def _identifier(self):
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()

        # See if the identifier is a reserved word
        text = self.source[self.start : self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)

        self._add_token(token_type=token_type)

    def _scan_token(self):
        """ Scan tokens"""
        c = self._advance()

        # In the original java implementation this is implemented with a switch
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
            "!": lambda: self._add_token(
                TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
            ),
            "=": lambda: self._add_token(
                TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
            ),
            "<": lambda: self._add_token(
                TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
            ),
            ">": lambda: self._add_token(
                TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
            ),
            "/": self._operator_slash,
            # These statements do nothing and are ignored. Since we need something that
            # is callable, a empty callable is returned. This is a little bit faster
            # than calling `lambda: None`
            " ": type(None),
            "\r": type(None),
            "\t": type(None),
            "\n": self._operator_newline,
            '"': self._string,
        }  # type: Dict[str, Callable]

        try:
            option = token_options[c]
            option()
        except KeyError:
            # This is the 'default' case in the Java switch statement
            if c.isdigit():
                # An digit encountered, consume the number
                self._number()
            elif c.isalpha() or c == "_":
                # An letter encoutered
                self._identifier()
            elif self.on_error:
                # If we have an on_error callback, run this, otherwise raise the
                # error again
                self.on_error(self.line, f"Unexpected character: {c}")
            else:
                raise

    def _is_at_end(self):
        return self.current >= len(self.source)

    def _advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def _peek(self):
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _add_token(self, token_type: TokenType, literal: Any = None):
        """
        In the java implementation this method is overloaded and depending on the
        literal parameter beeing there, or not. Because python doesn't have this
        construct the overloading is handled in the method itself. As it turns out,
        this is just the default value of '=None' for the 'literal' keyword.

        @TODO Define 'literal' better, Any is probably too broad
        """
        text = self.source[self.start : self.current]

        self.tokens.append(
            Token(token_type=token_type, lexeme=text, literal=literal, line=self.line)
        )

    def _match(self, expected: str):
        if self._is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1

        return True
