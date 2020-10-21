from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from yaplox.token import Token
from yaplox.yaplox_runtime_error import YaploxRuntimeError

if TYPE_CHECKING:
    from yaplox.yaplox_class import YaploxClass


class YaploxInstance:
    def __init__(self, klass: YaploxClass):
        self.klass = klass
        self.fields: Dict[str, Any] = {}

    def __repr__(self):
        return f"{self.klass.name} instance"

    def get(self, name: Token):
        try:
            return self.fields[name.lexeme]
        except KeyError:
            YaploxRuntimeError(name, f"Undefined property '{name.lexeme}'.")
