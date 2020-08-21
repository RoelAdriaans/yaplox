from yaplox.interpreter import Interpreter
from yaplox.expr import Literal, Unary
from yaplox.token_type import TokenType
from yaplox.token import Token


class TestInterpreter:
    def test_visit_literal_expr(self):
        expr = Literal("42")

        result = Interpreter().visit_literal_expr(expr)

        assert result == "42"

    def test_visit_unary_expr_minus(self):
        token = Token(token_type=TokenType.MINUS, lexeme="-", literal=None, line=0)
        expr = Unary(token, right=Literal(34))

        result = Interpreter().visit_unary_expr(expr)

        assert result == -34.0

    def test_visit_unary_expr_minus(self):
        token = Token(token_type=TokenType.MINUS, lexeme="-", literal=None, line=0)
        expr = Unary(token, right=Literal(34))

        result = Interpreter().visit_unary_expr(expr)

        assert result == -34.0
