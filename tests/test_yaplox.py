import sys
from unittest.mock import patch

import pytest

from yaplox.yaplox import Yaplox


class TestMain:
    def test_main(self):
        # Mustn't crash
        with patch.object(sys, "argv", []):
            yaplox = Yaplox()
            yaplox.main()

    def test_main_file_arg(self):
        # Mustn't crash
        with patch.object(sys, "argv", ["yaplox.py"]):
            yaplox = Yaplox()
            yaplox.main()

    def test_main_file_file_arg(self):
        # Mustn't crash
        with patch.object(sys, "argv", ["yaplox.py", "source.lox"]):
            yaplox = Yaplox()
            yaplox.main()

    def test_main_file_too_many_arg(self):
        # Must crash
        with patch.object(sys, "argv", ["yaplox.py", "test2.lox", "test2.lox"]):
            with pytest.raises(SystemExit) as pytest_wrapped_e:
                yaplox = Yaplox()
                yaplox.main()
            assert pytest_wrapped_e.value.code == 64
            assert pytest_wrapped_e.type == SystemExit
