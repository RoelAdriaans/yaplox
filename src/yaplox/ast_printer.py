from yaplox.expr import Binary, Expr, ExprVisitor, Grouping, Literal, Unary


class AstPrinter(ExprVisitor):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_grouping_expr(self, expr: Grouping):
        return self._parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary):
        return self._parenthesize(expr.operator.lexeme, expr.right)

    def visit_binary_expr(self, expr: Binary):
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def _parenthesize(self, name: str, *args: Expr):
        expressions = ["(", name]

        for expr in args:
            expressions.append(" ")
            expressions.append(expr.accept(self))

        expressions.append(")")

        return "".join(expressions)
