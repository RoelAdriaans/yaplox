from typing import List

from yaplox.expr import Binary, Expr, Grouping, Literal, Unary
from yaplox.token import Token
from yaplox.token_type import TokenType


class ParseError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message
        super().__init__(self.message)


class Parser:
    def __init__(self, tokens: List[Token], on_token_error=None):
        """
        Create a new parser that will parse the tokens in `tokens`
        'on_token_error' will be called when we encounter an error.
        """

        self.tokens = tokens
        self.on_token_error = on_token_error
        self.current = 0

    def parse(self):
        try:
            return self._expression()
        except ParseError:
            return None

    def _expression(self) -> Expr:
        return self._equality()

    def _equality(self) -> Expr:
        expr = self._comparison()

        while self._match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self._previous()
            right = self._comparison()
            expr = Binary(expr, operator, right)

        return expr

    def _comparison(self) -> Expr:
        expr = self._addition()

        while self._match(
            [
                TokenType.GREATER,
                TokenType.GREATER_EQUAL,
                TokenType.LESS,
                TokenType.LESS_EQUAL,
            ]
        ):
            operator = self._previous()
            right = self._addition()
            expr = Binary(expr, operator, right)

        return expr

    def _addition(self) -> Expr:
        expr = self._multiplication()

        while self._match([TokenType.MINUS, TokenType.PLUS]):
            operator = self._previous()
            right = self._multiplication()
            expr = Binary(expr, operator, right)

        return expr

    def _multiplication(self) -> Expr:
        expr = self._unary()

        while self._match([TokenType.SLASH, TokenType.STAR]):
            operator = self._previous()
            right = self._unary()
            expr = Binary(expr, operator, right)

        return expr

    def _unary(self) -> Expr:
        if self._match([TokenType.BANG, TokenType.MINUS]):
            operator = self._previous()
            right = self._unary()
            return Unary(operator, right)

        return self._primary()

    def _primary(self) -> Expr:
        if self._match([TokenType.FALSE]):
            return Literal(False)

        if self._match([TokenType.TRUE]):
            return Literal(True)

        if self._match([TokenType.NIL]):
            return Literal(None)

        if self._match([TokenType.NUMBER, TokenType.STRING]):
            return Literal(self._previous().literal)

        if self._match([TokenType.LEFT_PAREN]):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self._error(self._peek(), "Expect expression")

    def _match(self, types: List[TokenType]) -> bool:
        for tokentype in types:
            if self._check(tokentype):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, message: str):
        if self._check(token_type):
            return self._advance()
        self._error(self._peek(), message)

    def _check(self, tokentype: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().token_type == tokentype

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

    def _is_at_end(self) -> bool:
        return self._peek().token_type == TokenType.EOF

    def _error(self, token: Token, message: str):
        self.on_token_error(token, message)
        raise ParseError(token, message)

    def _synchronize(self):  # pragma: no cover
        """
        When the parser detects an error, try to recover and consume tokens until a
        ; or an statement is found.

        This is not yet functional, and thus excludede in coverage tests.
        """
        self._advance()

        while not self._is_at_end():
            if self._previous().token_type == TokenType.SEMICOLON:
                return

            if self._peek().token_type in [
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ]:
                return

            self._advance()
