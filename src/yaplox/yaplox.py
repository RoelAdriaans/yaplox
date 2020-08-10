import sys

from structlog import get_logger

from yaplox.__version__ import __VERSION__
from yaplox.ast_printer import AstPrinter
from yaplox.parser import Parser
from yaplox.scanner import Scanner
from yaplox.token import Token
from yaplox.token_type import TokenType

logger = get_logger()


class Yaplox:
    def __init__(self):
        self.had_error: bool = False

    def run(self, source: str):
        logger.debug("Running line", source=source)

        scanner = Scanner(source, on_error=self.error)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, on_token_error=self.token_error)
        expr = parser.parse()

        for token in tokens:
            logger.debug("Running token", token=token)

        if self.had_error:
            print("There was a fatal error")
            return

        ast = AstPrinter().print(expr)
        logger.debug("Generated ast", ast=ast)

    def error(self, line: int, message: str):
        self.report(line, "", message)

    def token_error(self, token: Token, message: str):
        if token.token_type == TokenType.EOF:
            self.report(token.line, " At end ", message)
        else:
            self.report(token.line, f" at '{token.lexeme}'", message)

    def report(self, line: int, where: str, message: str):
        message = f"[line {line}] Error {where} : {message}"
        logger.warning(message)
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
        print("Welcome to yaplox.py")
        if len(sys.argv) > 2:
            print(f"Usage: {sys.argv[0]} [script]")
            sys.exit(64)
        elif len(sys.argv) == 2:
            Yaplox().run_file(sys.argv[1])
        else:
            Yaplox().run_prompt()
