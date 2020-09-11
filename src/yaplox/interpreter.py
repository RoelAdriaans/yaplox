from typing import Any, List

from structlog import get_logger

from yaplox.clock import Clock
from yaplox.environment import Environment
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
from yaplox.token_type import TokenType
from yaplox.yaplox_callable import YaploxCallable
from yaplox.yaplox_function import YaploxFunction
from yaplox.yaplox_return_exception import YaploxReturnException
from yaplox.yaplox_runtime_error import YaploxRuntimeError

logger = get_logger()


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals

        self.globals.define("clock", Clock())

    def interpret(self, statements: List[Stmt], on_error=None) -> Any:
        try:
            res = None
            for statement in statements:
                logger.debug("Executing", statement=statement)
                res = self._execute(statement)
            # The return in the interpreter is not default Lox. It's added for now
            # to make testing and debugging easier.
            return res
        except YaploxRuntimeError as excp:
            on_error(excp)

    def _execute(self, stmt: Stmt):
        return stmt.accept(self)

    @staticmethod
    def _stringify(obj) -> str:
        if obj is None:
            return "nil"

        if isinstance(obj, float):
            # Print floats and remove trailing zero's, and if the dot is at the right
            # part, remove it too. Decimal precision is set to 6 positions
            return f"{obj:0.6f}".rstrip("0").rstrip(".")

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

    def visit_call_expr(self, expr: Call):
        function = self._evaluate(expr.callee)

        arguments = [self._evaluate(argument) for argument in expr.arguments]

        if not isinstance(function, YaploxCallable):
            raise YaploxRuntimeError(expr.paren, "Can only call functions and classes.")

        # function = YaploxCallable(callee)
        if len(arguments) != function.arity():
            raise YaploxRuntimeError(
                expr.paren,
                f"Expected {function.arity()} arguments but got {len(arguments)}.",
            )
        return function.call(self, arguments)

    def visit_grouping_expr(self, expr: Grouping):
        return self._evaluate(expr.expression)

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_logical_expr(self, expr: Logical):
        left = self._evaluate(expr.left)
        if expr.operator.token_type == TokenType.OR:
            if self._is_truthy(left):
                return left
        else:
            if not self._is_truthy(left):
                return left
        return self._evaluate(expr.right)

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

    def visit_variable_expr(self, expr: "Variable") -> Any:
        return self.environment.get(expr.name)

    def visit_assign_expr(self, expr: "Assign") -> Any:
        value = self._evaluate(expr.value)

        self.environment.assign(expr.name, value)

        return value

    # statement stuff
    def visit_expression_stmt(self, stmt: Expression) -> None:
        return self._evaluate(stmt.expression)

    def visit_function_stmt(self, stmt: Function) -> None:
        function = YaploxFunction(stmt)
        self.environment.define(stmt.name.lexeme, function)

    def visit_if_stmt(self, stmt: If) -> None:
        if self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self._execute(stmt.else_branch)

    def visit_while_stmt(self, stmt: While) -> None:
        while self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.body)

    def visit_print_stmt(self, stmt: Print) -> None:
        value = self._evaluate(stmt.expression)
        print(self._stringify(value))

    def visit_return_stmt(self, stmt: Return) -> None:
        value = None
        if stmt.value:
            value = self._evaluate(stmt.value)
        raise YaploxReturnException(value=value)

    def visit_var_stmt(self, stmt: "Var") -> None:
        value = None
        if stmt.initializer is not None:
            value = self._evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)

    def visit_block_stmt(self, stmt: "Block") -> None:
        self.execute_block(stmt.statements, Environment(self.environment))

    def execute_block(self, statements: List[Stmt], environment: Environment):
        previous_env = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self._execute(statement)
        finally:
            self.environment = previous_env
