from yaplox.environment import Environment
from yaplox.stmt import Function
from yaplox.yaplox_callable import YaploxCallable
from yaplox.yaplox_return_exception import YaploxReturnException


class YaploxFunction(YaploxCallable):
    def __init__(self, declaration: Function, closure: Environment):
        super().__init__()
        self.closure = closure
        self.declaration = declaration

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)

        for declared_token, argument in zip(self.declaration.params, arguments):
            environment.define(declared_token.lexeme, argument)
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except YaploxReturnException as yaplox_return:
            return yaplox_return.value

    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"
