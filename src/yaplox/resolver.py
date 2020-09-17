from collections import deque
from typing import Any, List, Union

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
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.scopes = deque()
        self.stack = deque()

    def _resolve_statements(self, statements: List[Stmt]):
        for statement in statements:
            self._resolve_statement(statement)

    def _resolve_statement(self, statement: Stmt):
        statement.accept(self)

    def _resolve_expression(self, expression: Expr):
        expression.accept(self)

    def _begin_scope(self):
        self.scopes.append({})

    def _end_scope(self):
        self.scopes.pop()

    def _declare(self, name: Token):
        """
        Declare that a variable existsc
        Example is `var a;`
        """
        if len(self.scopes) == 0:
            return

        # Look at the last scope
        scope = self.scopes[-1]
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
        pass

    def visit_binary_expr(self, expr: Binary):
        pass

    def visit_call_expr(self, expr: Call):
        pass

    def visit_grouping_expr(self, expr: Grouping):
        pass

    def visit_literal_expr(self, expr: Literal):
        pass

    def visit_logical_expr(self, expr: Logical):
        pass

    def visit_unary_expr(self, expr: Unary):
        pass

    def visit_variable_expr(self, expr: Variable):
        pass

    def visit_block_stmt(self, stmt: Block):
        self._begin_scope()
        self._resolve_statements(stmt.statements)
        self._end_scope()

    def visit_expression_stmt(self, stmt: Expression):
        pass

    def visit_function_stmt(self, stmt: Function):
        pass

    def visit_if_stmt(self, stmt: If):
        pass

    def visit_print_stmt(self, stmt: Print):
        pass

    def visit_return_stmt(self, stmt: Return):
        pass

    def visit_var_stmt(self, stmt: Var):
        self._declare(stmt.name)

        if stmt.initializer is not None:
            self._resolve_expression(stmt.initializer)

        self._define(stmt.name)

    def visit_while_stmt(self, stmt: While):
        pass
