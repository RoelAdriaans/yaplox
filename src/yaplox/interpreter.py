from structlog import get_logger

from yaplox.expr import Any, Binary, Expr, ExprVisitor, Grouping, Literal, Unary
from yaplox.token import Token
from yaplox.token_type import TokenType
from yaplox.yaplox_runtime_error import YaploxRuntimeError

logger = get_logger()


class Interpreter(ExprVisitor):
    def interpret(self, expression: Expr, on_error=None):
        try:
            value = self._evaluate(expression)
            str_value = self._stringify(value)
            logger.debug("Inteprenter result", value=str_value)
            return str_value

        except YaploxRuntimeError as excp:
            on_error(excp)

    @staticmethod
    def _stringify(obj) -> str:
        if obj is None:
            return "nil"

        if isinstance(obj, float):
            # Remove trailing zero's. No need to make a hack as in Java.
            return f"{obj:g}"

        return str(obj)

    @staticmethod
    def _binary_plus(expr, left, right):
        if isinstance(left, (float, int)) and isinstance(right, (float, int)):
            return left + right

        if isinstance(left, str) and isinstance(right, str):
            return str(left + right)

        raise YaploxRuntimeError(
            expr.operator, "Operands must be two numbers or two strings"
        )

    @staticmethod
    def _is_equal(a, b) -> bool:
        if a is None and b is None:
            return True

        if a is None:
            return False

        return a == b

    def visit_binary_expr(self, expr: Binary):
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)
        token_type = expr.operator.token_type

        # Validate that for the following Tokens the operands are numeric.
        # Orginal jpox does this in a switch statement. Since python does not
        # have this statement, the dict method is chosen. To not duplicate this line
        # over and over, the check is done seperately.
        if token_type in (
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.MINUS,
            TokenType.SLASH,
            TokenType.STAR,
        ):
            self._check_number_operands(expr.operator, left, right)

        choices = {
            # Comparison operators
            TokenType.GREATER: lambda: float(left) > float(right),
            TokenType.GREATER_EQUAL: lambda: float(left) >= float(right),
            TokenType.LESS: lambda: float(left) < float(right),
            TokenType.LESS_EQUAL: lambda: float(left) <= float(right),
            # Equality
            TokenType.BANG_EQUAL: lambda: not self._is_equal(left, right),
            TokenType.EQUAL_EQUAL: lambda: self._is_equal(left, right),
            # Arithmetic operators
            TokenType.MINUS: lambda: float(left) - float(right),
            TokenType.SLASH: lambda: float(left) / float(right),
            TokenType.STAR: lambda: float(left) * float(right),
            TokenType.PLUS: lambda: self._binary_plus(expr, left, right),
        }

        try:
            option = choices[token_type]
            result = option()
            return result

        except KeyError:
            raise YaploxRuntimeError(
                expr.operator, f"Unknown operator {expr.operator.lexeme}"
            )

    def visit_grouping_expr(self, expr: Grouping):
        return self._evaluate(expr.expression)

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_unary_expr(self, expr: Unary):
        right = self._evaluate(expr.right)

        token_type = expr.operator.token_type
        if token_type == TokenType.MINUS:
            self._check_number_operand(expr.operator, right)
            return -float(right)
        elif token_type == TokenType.BANG:
            return not Interpreter._is_truthy(right)

    @staticmethod
    def _check_number_operand(operator: Token, operand: Any):
        if isinstance(operand, (float, int)):
            return
        raise YaploxRuntimeError(operator, f"{operand} must be a number.")

    @staticmethod
    def _check_number_operands(operator: Token, left: Any, right: Any):
        if isinstance(left, (float, int)) and isinstance(right, (float, int)):
            return
        raise YaploxRuntimeError(operator, "Operands must be numbers.")

    @staticmethod
    def _is_truthy(obj):
        if obj is None:
            return False

        if isinstance(obj, bool):
            return obj

        return True

    def _evaluate(self, expr: Expr):
        return expr.accept(self)
