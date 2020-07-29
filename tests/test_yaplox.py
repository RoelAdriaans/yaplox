import sys
from unittest.mock import patch

import pytest

from yaplox.yaplox import Yaplox


class TestMain:
    @pytest.mark.skip("@TODO: Test input")
    def test_main(self):
        # Mustn't crash
        with patch.object(sys, "argv", []):
            yaplox = Yaplox()
            yaplox.main()

    @pytest.mark.skip("@TODO: Test input")
    def test_main_file_arg(self, mocker):
        # Mustn't crash
        with patch.object(sys, "argv", ["yaplox.py"]):
            yaplox = Yaplox()
            yaplox.main()

    def test_main_file_file_arg(self, mocker):
        # Mustn't crash
        # We mock the file loading, that's part of integration testing
        mocker_load_file = mocker.patch("yaplox.yaplox.Yaplox._load_file")
        with patch.object(sys, "argv", ["yaplox.py", "source.lox"]):
            yaplox = Yaplox()
            yaplox.main()
        assert mocker_load_file.called

    def test_main_file_too_many_arg(self):
        # Must crash
        with patch.object(sys, "argv", ["yaplox.py", "test2.lox", "test2.lox"]):
            with pytest.raises(SystemExit) as pytest_wrapped_e:
                yaplox = Yaplox()
                yaplox.main()
            assert pytest_wrapped_e.value.code == 64
            assert pytest_wrapped_e.type == SystemExit
