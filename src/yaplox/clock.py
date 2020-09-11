import time

from yaplox.yaplox_callable import YaploxCallable


class Clock(YaploxCallable):
    """This class is used in the Interpreter.

    In jlox this is an anonymous class. Since python does not have this
    concept, a real class is created

    @TODO Maybe rename it to CallableClock?
    """

    def call(self, interpreter, arguments):
        """
        Return the time in seconds since the epoch as a floating point number
        """
        return time.time()

    def arity(self) -> int:
        """ "
        Since we do not have any arguments, return 0
        """
        return 0

    def __str__(self):
        return "<native fn>"
