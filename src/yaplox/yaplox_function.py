from __future__ import annotations

from yaplox.environment import Environment
from yaplox.stmt import Function
from yaplox.yaplox_callable import YaploxCallable
from yaplox.yaplox_instance import YaploxInstance
from yaplox.yaplox_return_exception import YaploxReturnException


class YaploxFunction(YaploxCallable):
    def __init__(
        self,
        declaration: Function,
        closure: Environment,
        is_initializer: bool,
    ):
        super().__init__()
        self.closure = closure
        self.declaration = declaration
        self.is_initializer = is_initializer

    def bind(self, instance: YaploxInstance) -> YaploxFunction:
        environment = Environment(self.closure)
        environment.define("this", instance)
        return YaploxFunction(self.declaration, environment, self.is_initializer)

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)

        for declared_token, argument in zip(self.declaration.params, arguments):
            environment.define(declared_token.lexeme, argument)
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except YaploxReturnException as yaplox_return:
            if self.is_initializer:
                # When we're in init(), return this as an early return
                return self.closure.get_at(0, "this")
            return yaplox_return.value

        if self.is_initializer:
            # When init() is called directly on a class
            return self.closure.get_at(0, "this")

    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"
