import sys

from structlog import get_logger

logger = get_logger()


class Yaplox:
    @staticmethod
    def run(source):
        logger.debug("Running line", source=source)

    @staticmethod
    def run_file(file):
        """
        Run yaplox with `file` as source input
        """
        with open(file) as f:
            content = f.readlines()
            Yaplox.run(content)

    @staticmethod
    def run_prompt():
        """
        Run a REPL prompt
        """
        while True:
            str_input = input("> ")


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
            Yaplox.run_file(sys.argv[1])
        else:
            Yaplox.run_prompt()
