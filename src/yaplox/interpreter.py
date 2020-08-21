from yaplox.expr import ExprVisitor, Expr, Binary, Grouping, Literal, Unary
from yaplox.token_type import TokenType


class Interpreter(ExprVisitor):
    def visit_binary_expr(self, expr: Binary):
        pass

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
