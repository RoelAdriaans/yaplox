from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List

from yaplox.yaplox_callable import YaploxCallable
from yaplox.yaplox_function import YaploxFunction
from yaplox.yaplox_instance import YaploxInstance

if TYPE_CHECKING:
    from yaplox.interpreter import Interpreter


class YaploxClass(YaploxCallable):
    def call(self, interpreter: Interpreter, arguments: List[Any]):
        instance = YaploxInstance(klass=self)
        return instance

    def arity(self) -> int:
        return 0

    def __init__(self, name: str, methods: Dict[str, YaploxFunction]):
        self.name = name
        self.methods = methods

    def __repr__(self):
        return self.name

    def find_method(self, name: str) -> YaploxFunction:
        try:
            return self.methods[name]
        except KeyError:
            return None
