from yaplox.yaplox_runtime_error import YaploxRuntimeError


class YaploxReturnException(YaploxRuntimeError):
    """
    This is a hack to return values from Lox functions.

    The original jlox name is Return, that clashes with the Stmt.Return.
    To make it easier, it has been renamed to this class.
    """

    def __init__(self, value):
        super().__init__(None, None)
        self.value = value
