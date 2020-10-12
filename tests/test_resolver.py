from yaplox.resolver import Resolver
from yaplox.token_type import TokenType
from yaplox.yaplox import Yaplox


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

    def test_resolver(self, run_code_lines):
        lines = [
            'var a = "outer";',
            "{",
            '  var a = "inner";',
            "  print a;",
            "}",
        ]

        assert run_code_lines(lines).out == "inner\n"

    def test_function(self, capsys):
        lines = [
            'var a = "global";',
            "{",
            "  fun showA() {",
            "    print a;",
            "  }",
            "",
            "  showA();",
            '  var a = "block";',
            "  showA();",
            "}",
        ]
        lines = "\n".join(lines)

        Yaplox().run(lines)
        captured = capsys.readouterr()
        assert captured.out == "\n"
