from typing import Any, Dict, Optional

from yaplox.token import Token
from yaplox.yaplox_runtime_error import YaploxRuntimeError


class Environment:
    def __init__(self, enclosing: Optional["Environment"] = None):
        self.values: Dict[str, Any] = dict()
        self.enclosing = enclosing

    def define(self, name: str, value: Any):
        self.values[name] = value

    def _ancestor(self, distance: int) -> "Environment":
        environment = self

        for _ in range(distance):
            environment = environment.enclosing

        return environment

    def get_at(self, distance: int, name: str) -> Any:
        """
        Return a variable at a distance
        """
        return self._ancestor(distance=distance).values.get(name)

    def get(self, name: Token) -> Any:
        try:
            return self.values[name.lexeme]
        except KeyError:
            # We ignore this key error, if an nested Environment is available, test this
            # first.
            pass

        if self.enclosing:
            return self.enclosing.get(name)

        raise YaploxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: Any):
        """Assign a new value to an existing variable. Eg:
        var a = 3;
        a = 4  # This calls assign.
        """
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing:
            self.enclosing.assign(name, value)
            return

        raise YaploxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign_at(self, distance: int, name: Token, value: Any):
        self._ancestor(distance).values[name.lexeme] = value

