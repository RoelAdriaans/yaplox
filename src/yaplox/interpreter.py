from yaplox.expr import Binary, Expr, ExprVisitor, Grouping, Literal, Unary
from yaplox.token_type import TokenType


class Interpreter(ExprVisitor):
    @staticmethod
    def _binary_plus(left, right):
        if isinstance(left, (float, int)) and isinstance(right, (float, int)):
            return left + right

        if isinstance(left, str) and isinstance(right, str):
            return str(left + right)

        raise ValueError(f"Unknown operands {left} and/or {right}")

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
            TokenType.PLUS: lambda: self._binary_plus(left, right),
        }
        option = choices[expr.operator.token_type]
        result = option()

        return result

    def visit_grouping_expr(self, expr: Grouping):
        return self._evaluate(expr.expression)

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_unary_expr(self, expr: Unary):
        right = self._evaluate(expr.right)

        choices = {
            TokenType.MINUS: lambda slf: -float(right),
            TokenType.BANG: lambda slf: not Interpreter._is_truthy(right),
        }

        option = choices[expr.operator.token_type]
        result = option(self)

        return result

    @staticmethod
    def _is_truthy(obj):
        if obj is None:
            return False

        if isinstance(obj, bool):
            return obj

        return True

    def _evaluate(self, expr: Expr):
        return expr.accept(self)
