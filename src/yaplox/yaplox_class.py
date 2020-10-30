from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from yaplox.yaplox_callable import YaploxCallable
from yaplox.yaplox_function import YaploxFunction
from yaplox.yaplox_instance import YaploxInstance

if TYPE_CHECKING:
    from yaplox.interpreter import Interpreter


class YaploxClass(YaploxCallable):
    def call(self, interpreter: Interpreter, arguments: List[Any]):
        instance = YaploxInstance(klass=self)
        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance=instance).call(
                interpreter=interpreter, arguments=arguments
            )
        return instance

    def arity(self) -> int:
        initializer = self.find_method("init")
        if initializer is not None:
            return initializer.arity()
        else:
            return 0

    def __init__(
        self,
        name: str,
        superclass: Optional[YaploxClass],
        methods: Dict[str, YaploxFunction],
    ):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def __repr__(self):
        return self.name

    def find_method(self, name: str) -> Optional[YaploxFunction]:
        try:
            return self.methods[name]
        except KeyError:
            pass

        if self.superclass:
            return self.superclass.find_method(name)

        return None
