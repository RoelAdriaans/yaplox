import sys


class Yaplox:
    @staticmethod
    def run_file(file):
        """
        Run yaplox with `file` as source input
        """
        print(f"Running file {file}")

    @staticmethod
    def run_prompt():
        """
        Run a REPL prompt
        """
        print("Running Prompt")

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
