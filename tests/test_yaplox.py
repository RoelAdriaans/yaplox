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

    def test_main_file_file_arg(self, monkeypatch):
        # Mustn't crash
        # We mock the file loading, that's part of integration testing

        @staticmethod
        def mocked_load_file(file):
            print("In mocked load file")
            assert file == "source.lox"
            return "print(3+4);"

        monkeypatch.setattr(Yaplox, "_load_file", mocked_load_file)

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
