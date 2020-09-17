from yaplox.resolver import Resolver
from yaplox.token import Token
from yaplox.token_type import TokenType


class TestResolver:
    def test_declare(self, create_token_factory):
        # Test that the declare function does something we expect:
        resolver = Resolver(None)

        # First, we add a new scope:
        resolver._begin_scope()

        # Add a token:
        test_token = create_token_factory(
            token_type=TokenType.IDENTIFIER, lexeme="identifier"
        )
        resolver._declare(test_token)

        # Assert that the identifier token has been added
        assert "identifier" in resolver.scopes[0]
        assert resolver.scopes[0]["identifier"] is False

        # And define the token
        resolver._define(test_token)
        assert resolver.scopes[0]["identifier"] is True
