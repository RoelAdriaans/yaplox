import pytest

from yaplox.expr import Binary, Grouping, Literal, Unary
from yaplox.interpreter import Interpreter
from yaplox.parser import Parser
from yaplox.scanner import Scanner
from yaplox.token_type import TokenType


class TestInterpreter:
    def test_visit_grouping_expr(self):
        nested = Literal("18")
        expr = Grouping(nested)
        result = Interpreter().visit_grouping_expr(expr)

        assert result == nested.value

    def test_visit_literal_expr(self):
        expr = Literal("42")

        result = Interpreter().visit_literal_expr(expr)

        assert result == "42"

    @pytest.mark.parametrize(
        ("token_type", "literal", "expected"),
        [
            (TokenType.MINUS, 34, -34.0),
            (TokenType.MINUS, -42, 42.0),
            (TokenType.MINUS, -0, 0.0),
            (TokenType.MINUS, 0, -0.0),
            (TokenType.BANG, False, True),
            (TokenType.BANG, True, False),
            (TokenType.BANG, None, True),  # !None == True
            (TokenType.BANG, "Stringy", False),
            (TokenType.BANG, "", False),
            (TokenType.BANG, 0, False),
            (TokenType.BANG, "0", False),
        ],
    )
    def test_visit_unary_expr(
        self, create_token_factory, token_type, literal, expected
    ):
        token = create_token_factory(token_type=token_type)
        expr = Unary(token, right=Literal(literal))

        result = Interpreter().visit_unary_expr(expr)

        if isinstance(expected, bool):
            assert result is expected
        else:
            assert result == expected

    @pytest.mark.parametrize(
        ("left", "token_type", "right", "expected"),
        [
            (10, TokenType.GREATER, 7, True),
            (10, TokenType.GREATER_EQUAL, 10, True),
            (7, TokenType.LESS, 10, True),
            (7, TokenType.LESS_EQUAL, 7, True),
            (7, TokenType.BANG_EQUAL, 7, False),
            (7, TokenType.BANG_EQUAL, 10, True),
            (None, TokenType.BANG_EQUAL, None, False),  # None !=None
            (None, TokenType.EQUAL_EQUAL, None, True),  # None ==None
            (None, TokenType.BANG_EQUAL, 5, True),  # None != 5
            (None, TokenType.EQUAL_EQUAL, 5, False),  # None == 5
            (5, TokenType.EQUAL_EQUAL, None, False),  # 5 == None
            ("FooBar", TokenType.BANG_EQUAL, "BarFoo", True),
            ("FooBar", TokenType.EQUAL_EQUAL, "BarFoo", False),
            ("FooBar", TokenType.BANG_EQUAL, "FooBar", False),
            ("FooBar", TokenType.EQUAL_EQUAL, "FooBar", True),
            (10, TokenType.MINUS, 7, 3),
            (10, TokenType.MINUS, 20, -10),
            (10, TokenType.MINUS, 20, -10),
            (10, TokenType.SLASH, 2, 5),
            (10, TokenType.SLASH, 3, 3.3333333333333335),
            (5, TokenType.STAR, 5, 25),
            (5, TokenType.STAR, 0, 0),
            (2, TokenType.PLUS, 2, 4),
            ("Foo", TokenType.PLUS, "Bar", "FooBar"),
        ],
    )
    def test_visit_binary_expr(
        self, create_token_factory, left, token_type, right, expected
    ):
        operator = create_token_factory(token_type=token_type)
        expr_left = Literal(left)
        expr_right = Literal(right)
        expr = Binary(left=expr_left, operator=operator, right=expr_right)

        result = Interpreter().visit_binary_expr(expr)

        if isinstance(expected, bool):
            assert result is expected
        else:
            assert result == expected

    def test_nested_binary_expr(self, create_token_factory, mocker):
        """ Test nested binary expressions, 4 * 6 / 2 """
        on_scanner_error_mock = mocker.MagicMock()
        on_parser_error_mock = mocker.MagicMock()

        test_string = "4 * 6 / 2"
        scanner = Scanner(test_string, on_error=on_scanner_error_mock)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, on_token_error=on_parser_error_mock)
        expr = parser.parse()

        assert isinstance(expr, Binary)
        assert isinstance(expr.left, Binary)
        assert isinstance(expr.right, Literal)

        assert expr.operator.token_type == TokenType.SLASH
        assert expr.right.value == 2.0
        # Left will be 4 * 6
        assert expr.left.operator.token_type == TokenType.STAR
        assert expr.left.left.value == 4
        assert expr.left.right.value == 6

        result = Interpreter().visit_binary_expr(expr)

        assert result == 12
