from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from yaplox.yaplox_callable import YaploxCallable
from yaplox.yaplox_instance import YaploxInstance

if TYPE_CHECKING:
    from yaplox.interpreter import Interpreter


class YaploxClass(YaploxCallable):
    def call(self, interpreter: Interpreter, arguments: List[Any]):
        instance = YaploxInstance(klass=self)
        return instance

    def arity(self) -> int:
        return 0

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name
