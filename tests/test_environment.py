import pytest

from yaplox.environment import Environment
from yaplox.token_type import TokenType
from yaplox.yaplox_runtime_error import YaploxRuntimeError


class TestEnvironment:
    def test_environment(self, create_token_factory):
        env = Environment()
        foo_token = create_token_factory(token_type=TokenType.VAR, lexeme="Foo")
        bar_token = create_token_factory(token_type=TokenType.VAR, lexeme="Bar")

        env.define("Foo", "Bar")

        assert env.get(foo_token) == "Bar"

        # This token isn't present
        with pytest.raises(YaploxRuntimeError):
            env.get(bar_token)

        # Test assign
        # Assign a new value to an existing key
        env.assign(foo_token, "New_value")

        assert env.get(foo_token) == "New_value"

        # Assigning to a new value is not possible
        with pytest.raises(YaploxRuntimeError):
            env.assign(bar_token, "Foo")

    @pytest.mark.parametrize("falsy_values", [0.0, 0, False, None])
    def test_falsy_values(self, create_token_factory, falsy_values):
        # Set a key with the value 0.0.
        # In python this is evaluated as false, but we want this value back!
        env = Environment()
        foo_token = create_token_factory(token_type=TokenType.VAR, lexeme="Foo")

        env.define("Foo", falsy_values)

        if isinstance(falsy_values, bool):
            assert env.get(foo_token) is falsy_values
        else:
            assert env.get(foo_token) == falsy_values
