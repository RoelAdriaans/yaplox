from collections import deque
from typing import Deque, List

from structlog import get_logger

from yaplox.expr import (
    Assign,
    Binary,
    Call,
    Expr,
    ExprVisitor,
    Grouping,
    Literal,
    Logical,
    Unary,
    Variable,
)
from yaplox.function_type import FunctionType
from yaplox.interpreter import Interpreter
from yaplox.stmt import (
    Block,
    Expression,
    Function,
    If,
    Print,
    Return,
    Stmt,
    StmtVisitor,
    Var,
    While,
)
from yaplox.token import Token

logger = get_logger()


class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter: Interpreter, on_error=None):
        self.interpreter = interpreter
        self.scopes: Deque = deque()
        self.on_error = on_error
        self.current_function = FunctionType.NONE

    def resolve(self, statements: List[Stmt]):
        self._resolve_statements(statements)

    def _resolve_statements(self, statements: List[Stmt]):
        for statement in statements:
            self._resolve_statement(statement)

    def _resolve_statement(self, statement: Stmt):
        statement.accept(self)

    def _resolve_expression(self, expression: Expr):
        expression.accept(self)

    def _resolve_local(self, expr: Expr, name: Token):
        for idx, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, idx)
                return
        # Not found. Assume it is global.

    def _resolve_function(self, function: Function, type: FunctionType):
        enclosing_function = self.current_function
        self.current_function = type

        self._begin_scope()
        for param in function.params:
            self._declare(param)
            self._define(param)

        self._resolve_statements(function.body)
        self._end_scope()
        self.current_function = enclosing_function

    def _begin_scope(self):
        self.scopes.append({})

    def _end_scope(self):
        self.scopes.pop()

    def _declare(self, name: Token):
        """
        Declare that a variable exists
        Example is `var a;`
        """
        if len(self.scopes) == 0:
            return

        # Look at the last scope
        scope = self.scopes[-1]
        if name.lexeme in scope:
            self.on_error(name, "Already variable with this name in this scope.")

        scope[name.lexeme] = False

    def _define(self, name: Token):
        """
        Declare that a variable is ready to use
        Example: `a = 42;`
        """

        if len(self.scopes) == 0:
            return

        scope = self.scopes[-1]
        scope[name.lexeme] = True

    def visit_assign_expr(self, expr: Assign):
        self._resolve_expression(expr.value)
        self._resolve_local(expr, expr.name)

    def visit_binary_expr(self, expr: Binary):
        self._resolve_expression(expr.left)
        self._resolve_expression(expr.right)

    def visit_call_expr(self, expr: Call):
        self._resolve_expression(expr.callee)

        for argument in expr.arguments:
            self._resolve_expression(argument)

    def visit_grouping_expr(self, expr: Grouping):
        self._resolve_expression(expr.expression)

    def visit_literal_expr(self, expr: Literal):
        """
        Since a literal expression doesn't mention any variables and doesn't
        contain any subexpressions, there is no work to do.
        """
        return

    def visit_logical_expr(self, expr: Logical):
        self._resolve_expression(expr.left)
        self._resolve_expression(expr.right)

    def visit_unary_expr(self, expr: Unary):
        self._resolve_expression(expr.right)

    def visit_variable_expr(self, expr: Variable):
        if len(self.scopes) != 0 and self.scopes[-1].get(expr.name.lexeme) is False:
            self.on_error(
                expr.name, "Cannot read local variable in its own initializer."
            )
        self._resolve_local(expr, expr.name)

    def visit_block_stmt(self, stmt: Block):
        self._begin_scope()
        self._resolve_statements(stmt.statements)
        self._end_scope()

    def visit_expression_stmt(self, stmt: Expression):
        self._resolve_expression(stmt.expression)

    def visit_function_stmt(self, stmt: Function):
        self._declare(stmt.name)
        self._define(stmt.name)

        self._resolve_function(stmt, FunctionType.FUNCTION)

    def visit_if_stmt(self, stmt: If):
        self._resolve_expression(stmt.condition)
        self._resolve_statement(stmt.then_branch)
        if stmt.else_branch:
            self._resolve_statement(stmt.else_branch)

    def visit_print_stmt(self, stmt: Print):
        self._resolve_expression(stmt.expression)

    def visit_return_stmt(self, stmt: Return):
        if self.current_function == FunctionType.NONE:
            self.on_error(stmt.keyword, "Can't return from top-level code.")

        if stmt.value:
            self._resolve_expression(stmt.value)

    def visit_var_stmt(self, stmt: Var):
        self._declare(stmt.name)

        if stmt.initializer is not None:
            self._resolve_expression(stmt.initializer)

        self._define(stmt.name)

    def visit_while_stmt(self, stmt: While):
        self._resolve_expression(stmt.condition)
        self._resolve_statement(stmt.body)
