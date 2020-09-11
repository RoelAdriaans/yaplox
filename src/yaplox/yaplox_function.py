from yaplox.environment import Environment
from yaplox.stmt import Function
from yaplox.yaplox_callable import YaploxCallable


class YaploxFunction(YaploxCallable):
    def __init__(self, declaration: Function):
        super().__init__()
        self.declaration = declaration

    def call(self, interpreter, arguments):
        environment = Environment(interpreter.globals)

        for declared_token, argument in zip(self.declaration.params, arguments):
            environment.define(declared_token.lexeme, argument)

        interpreter.execute_block(self.declaration.body, environment)

    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"
