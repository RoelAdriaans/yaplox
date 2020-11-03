"""
Test Yaplox against the upstream test files.

The test files are added as is. This will make it easy to update these files in the
future. Some tests are not possible to run, they are skipped in this test.
"""
from pathlib import Path
import re
from typing import Dict, Tuple, List

import pytest
from yaplox.yaplox import Yaplox

root_dir = Path(__file__).parent

OUTPUT_EXPECT = re.compile(r"// expect: ?(.*)")
ERROR_EXPECT = re.compile(r"// (Error.*)")
ERROR_LINE_EXPECT = re.compile(r"// \[((java|c) )?line (\d+)\] (Error.*)")
RUNTIME_ERROR_EXPECT = re.compile(r"// expect runtime error: (.+)")
SYNTAX_ERROR_RE = re.compile(r"\[.*line (\d+)\] (Error.+)")
STACK_TRACE_RE = re.compile(r"\[line (\d+)\]")
NONTEST_RE = re.compile(r"// nontest")


def get_upstream_tests():
    for path in Path(root_dir).rglob("*.lox"):
        yield str(path)


class TestUpstream:
    @pytest.mark.parametrize("filename", get_upstream_tests())
    def test_upstream_tests(self, filename, capsys):
        with open(filename) as f:
            test_code = f.readline()

        # We run a new instance of yaplox every time
        yaplox = Yaplox()
        yaplox.run_file(filename)
        captured = capsys.readouterr()

    def _parse_file(self, test_code):
        # Parse the file, see if we expect runtime or compile errors
        ...

    def _run_code(self, test_code: List[str], filename: str) -> Dict[str, str]:
        """

        Args:
            test_code ():
            filename ():

        Returns:

        """
        # Run the code, and return the result.
        # Return the output, and/or errors that have been thrown
        #
        ...
