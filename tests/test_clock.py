import time

from yaplox.clock import Clock


class TestClock:
    def test_clock(self, monkeypatch):
        """
        Test the Clock class. This will return the time since the Unix epoch.
        Since we can't test that easily, we mock it.
        """
        test_value = 232323.43454

        def mocked_time():
            return test_value

        monkeypatch.setattr(time, "time", mocked_time)
        clock = Clock()

        result = clock.call(None, None)

        assert result == test_value
        assert clock.arity() == 0
        assert str(clock) == "<native fn>"
