import sys

from structlog import get_logger

from yaplox.__version__ import __VERSION__
from yaplox.scanner import Scanner

logger = get_logger()


class Yaplox:
    def __init__(self):
        self.had_error: bool = False

    def run(self, source: str):
        logger.debug("Running line", source=source)

        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            logger.info(token=token)

    def error(self, line: int, message: str):
        self.report(line, "", message)

    def report(self, line: int, where: str, message: str):
        message = f"[line {line}] Error {where} : {message}"
        logger.warning(message)
        self.had_error = True

    def run_file(self, file: str):
        """
        Run yaplox with `file` as filename for the source input
        """
        with open(file) as f:
            content = f.readlines()
            lines = "\n".join(content)
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
                if str_input[0] == chr(4):
                    # Catch ctrl-D
                    self.quit_gracefully()

                self.run(str_input)
                self.had_error = False

            except KeyboardInterrupt:
                # Catch CTRL-C
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
