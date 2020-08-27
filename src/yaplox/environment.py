from typing import Any

from yaplox.token import Token
from yaplox.yaplox_runtime_error import YaploxRuntimeError


class Environment:
    def __init__(self):
        self.values = dict()

    def define(self, name: str, value: Any):
        self.values[name] = value

    def get(self, name: Token) -> Any:
        try:
            return self.values[name.lexeme]
        except KeyError:
            raise YaploxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: Any):
        """ Assign a new value to an existing variable. Eg:
        var a = 3;
        a = 4  # This calls assign.
        """
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        raise YaploxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
