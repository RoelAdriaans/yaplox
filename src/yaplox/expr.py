# This file has been auto-generated by tools/generate_ast.py
# Do not edit this file by hand. Or do, but it will be overwritten

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List

from yaplox.token import Token


class ExprVisitor(ABC):
    """This class is used as an Vistor for the Expr class"""

    @abstractmethod
    def visit_assign_expr(self, expr: Assign):
        raise NotImplementedError

    @abstractmethod
    def visit_binary_expr(self, expr: Binary):
        raise NotImplementedError

    @abstractmethod
    def visit_call_expr(self, expr: Call):
        raise NotImplementedError

    @abstractmethod
    def visit_get_expr(self, expr: Get):
        raise NotImplementedError

    @abstractmethod
    def visit_grouping_expr(self, expr: Grouping):
        raise NotImplementedError

    @abstractmethod
    def visit_literal_expr(self, expr: Literal):
        raise NotImplementedError

    @abstractmethod
    def visit_logical_expr(self, expr: Logical):
        raise NotImplementedError

    @abstractmethod
    def visit_set_expr(self, expr: Set):
        raise NotImplementedError

    @abstractmethod
    def visit_this_expr(self, expr: This):
        raise NotImplementedError

    @abstractmethod
    def visit_unary_expr(self, expr: Unary):
        raise NotImplementedError

    @abstractmethod
    def visit_variable_expr(self, expr: Variable):
        raise NotImplementedError


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor):
        raise NotImplementedError


class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value

    def accept(self, visitor: ExprVisitor):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_assign_expr(self)


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_binary_expr(self)


class Call(Expr):
    def __init__(self, callee: Expr, paren: Token, arguments: List[Expr]):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor: ExprVisitor):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_call_expr(self)


class Get(Expr):
    def __init__(self, obj: Expr, name: Token):
        self.obj = obj
        self.name = name

    def accept(self, visitor: ExprVisitor):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_get_expr(self)


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: ExprVisitor):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_grouping_expr(self)


class Literal(Expr):
    def __init__(self, value: Any):
        self.value = value

    def accept(self, visitor: ExprVisitor):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_literal_expr(self)


class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_logical_expr(self)


class Set(Expr):
    def __init__(self, obj: Expr, name: Token, value: Expr):
        self.obj = obj
        self.name = name
        self.value = value

    def accept(self, visitor: ExprVisitor):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_set_expr(self)


class This(Expr):
    def __init__(self, keyword: Token):
        self.keyword = keyword

    def accept(self, visitor: ExprVisitor):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_this_expr(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_unary_expr(self)


class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor: ExprVisitor):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_variable_expr(self)
