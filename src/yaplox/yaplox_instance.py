from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yaplox.yaplox_class import YaploxClass


class YaploxInstance:
    def __init__(self, klass: YaploxClass):
        self.klass = klass

    def __repr__(self):
        return f"{self.klass.name} instance"
