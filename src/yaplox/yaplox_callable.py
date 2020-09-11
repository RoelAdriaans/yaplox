from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, List

# This is a hack to prevent circular imports; since Interpreter imports from this file,
# we will only import it during the type_checking run from mypy
if TYPE_CHECKING:
    from yaplox.interpreter import Interpreter


class YaploxCallable(ABC):
    @abstractmethod
    def call(self, interpreter: Interpreter, arguments: List[Any]):
        raise NotImplementedError

    @abstractmethod
    def arity(self) -> int:
        raise NotImplementedError
