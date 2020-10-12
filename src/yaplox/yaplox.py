import sys

from structlog import get_logger

from yaplox.__version__ import __VERSION__
from yaplox.config import config  # noqa: F401
from yaplox.interpreter import Interpreter
from yaplox.parser import Parser
from yaplox.resolver import Resolver
from yaplox.scanner import Scanner
from yaplox.token import Token
from yaplox.token_type import TokenType
from yaplox.yaplox_runtime_error import YaploxRuntimeError

logger = get_logger()


class Yaplox:
    def __init__(self):
        self.had_error: bool = False
        self.had_runtime_error: bool = False
        self.interpreter: Interpreter = Interpreter()

    def run(self, source: str):
        logger.debug("Running line", source=source)

        scanner = Scanner(source, on_error=self.error)
        tokens = scanner.scan_tokens()

        for token in tokens:
            logger.debug("Running token", token=token)

        parser = Parser(tokens, on_token_error=self.token_error)
        statements = parser.parse()

        if self.had_error:
            logger.debug("Error after parsing")
            return

        resolver = Resolver(interpreter=self.interpreter, on_error=self.runtime_error)
        resolver.resolve(statements)

        self.interpreter.interpret(statements, on_error=self.runtime_error)

    def error(self, line: int, message: str):
        self.report(line, "", message)

    def runtime_error(self, error: YaploxRuntimeError):
        message = f"{str(error.message)} in line [line{error.token.line}]"
        logger.warning(message)
        print(message, file=sys.stderr)
        self.had_runtime_error = True

    def token_error(self, token: Token, message: str):
        if token.token_type == TokenType.EOF:
            self.report(token.line, " At end ", message)
        else:
            self.report(token.line, f" at '{token.lexeme}'", message)

    def report(self, line: int, where: str, message: str):
        message = f"[line {line}] Error {where} : {message}"
        logger.warning(message)
        print(message, file=sys.stderr)
        self.had_error = True

    @staticmethod
    def _load_file(file: str) -> str:
        with open(file) as f:
            content = f.readlines()
            lines = "\n".join(content)
            return lines

    def run_file(self, file: str):
        """
        Run yaplox with `file` as filename for the source input
        """
        lines = self._load_file(file)
        self.run(lines)

        # Indicate an error in the exit code
        if self.had_error:
            sys.exit(65)

        if self.had_runtime_error:
            sys.exit(70)

    def run_prompt(self):
        """
        Run a REPL prompt. This prompt can be quit by pressing CTRL-C or CTRL-D
        """
        print(f"Welcome to Yaplox {__VERSION__}")
        print("Press CTRL-C or CTRL-D to exit")

        while True:
            try:
                str_input = input("> ")
                if str_input and str_input[0] == chr(4):
                    # Catch ctrl-D and raise as error
                    raise EOFError

                self.run(str_input)
                self.had_error = False

            except (KeyboardInterrupt, EOFError):
                # Catch CTRL-C or CTRL-D (EOF)
                self.quit_gracefully()

    def quit_gracefully(self):
        print("So Long, and Thanks for All the Fish")
        sys.exit(0)

    @staticmethod
    def main():
        """
        Run Yaplox from the console. Accepts one argument as a file that will be
        executed, or no arguments to run in REPL mode.
        """
        if len(sys.argv) > 2:
            print(f"Usage: {sys.argv[0]} [script]")
            sys.exit(64)
        elif len(sys.argv) == 2:
            Yaplox().run_file(sys.argv[1])
        else:
            Yaplox().run_prompt()
