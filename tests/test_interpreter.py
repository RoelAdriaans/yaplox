import pytest

from yaplox.expr import Binary, Grouping, Literal, Unary
from yaplox.interpreter import Interpreter
from yaplox.parser import Parser
from yaplox.scanner import Scanner
from yaplox.stmt import Expression
from yaplox.token_type import TokenType
from yaplox.yaplox_runtime_error import YaploxRuntimeError


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

    def test_visit_unary_sad_flow(self, create_token_factory):
        # -"Foo" Should result in an error
        token = create_token_factory(token_type=TokenType.MINUS)
        expr = Unary(token, right=Literal("Foo"))
        with pytest.raises(YaploxRuntimeError) as excinfo:
            Interpreter().visit_unary_expr(expr)

        assert "Foo must be a number" in str(excinfo.value)

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

    @pytest.mark.parametrize(
        ("left", "token_type", "right"),
        [
            (10, TokenType.MINUS, "String"),
            (10, TokenType.GREATER, "Foo"),
            ("43", TokenType.PLUS, 18),
            (43, TokenType.PLUS, "18"),
        ],
    )
    def test_binary_expression_failing(
        self, create_token_factory, left, token_type, right
    ):
        operator = create_token_factory(token_type=token_type)
        expr_left = Literal(left)
        expr_right = Literal(right)
        expr = Binary(left=expr_left, operator=operator, right=expr_right)
        with pytest.raises(YaploxRuntimeError):
            Interpreter().visit_binary_expr(expr)

    def test_nested_binary_expr(self, create_token_factory, mocker):
        """ Test nested binary expressions, 4 * 6 / 2 """
        on_scanner_error_mock = mocker.MagicMock()
        on_parser_error_mock = mocker.MagicMock()

        test_string = "4 * 6 / 2;"
        scanner = Scanner(test_string, on_error=on_scanner_error_mock)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, on_token_error=on_parser_error_mock)
        statements = parser.parse()
        expr: Expression = statements[0].expression

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

    def test_unknown_operator(self, create_token_factory):
        operator = create_token_factory(token_type=TokenType.EOF)
        expr_left = Literal(None)
        expr_right = Literal(None)
        expr = Binary(left=expr_left, operator=operator, right=expr_right)
        with pytest.raises(YaploxRuntimeError):
            Interpreter().visit_binary_expr(expr)

    @pytest.mark.parametrize(
        ("expression", "result"),
        [("4 * 6 / 2", "12"), ("12 < 6", "False"), ("12 > 6", "True"), ("3+3", "6")],
    )
    def test_interpret(self, mocker, expression, result):
        on_scanner_error_mock = mocker.MagicMock()
        on_parser_error_mock = mocker.MagicMock()

        scanner = Scanner(expression, on_error=on_scanner_error_mock)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, on_token_error=on_parser_error_mock)
        expr = parser.parse()

        result = Interpreter().interpret(expr)

        assert result == result

    def test_interpret_error(self, mocker):
        on_scanner_error_mock = mocker.MagicMock()
        on_parser_error_mock = mocker.MagicMock()
        on_interpret_error_mock = mocker.MagicMock()

        expression = '0 + "Foo"'

        scanner = Scanner(expression, on_error=on_scanner_error_mock)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, on_token_error=on_parser_error_mock)
        expr = parser.parse()

        Interpreter().interpret(expr, on_error=on_interpret_error_mock)

        # There will be an error
        assert on_interpret_error_mock.called
        assert "Operands must be two numbers or two strings" in str(
            on_interpret_error_mock.call_args
        )
