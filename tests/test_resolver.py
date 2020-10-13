from yaplox.resolver import Resolver
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

    def test_resolver(self, run_code_block):
        lines = """
            var a = "outer";
            {
              var a = "inner";
              print a;
            }
        """

        assert run_code_block(lines).out == "inner\n"

    def test_function(self, run_code_block):
        lines = """
        var a = "global";
        {
          fun showA() {
            print a;
          }

          showA();
          var a = "block";
          showA();
        }
        """

        assert run_code_block(lines).out == "global\nglobal\n"

    def test_cannot_resolve_name(self, run_code_block):
        code = """
        {
            var a = a + 3;
        }
        """
        assert (
            "[line 3] Error  at 'a' : "
            "Cannot read local variable in its own initializer."
            in run_code_block(code).err
        )

    def test_limited_nested(self, run_code_block):
        """
        Limited test from test_nested in test_statement. Validated with clox and jlox,
        the result must be `inner a`.
        """

        source = """
        var a = "global a";
        var q = "global q";
        {
          var a = "outer a";
          var w = "outer w";
          {
            var a = "inner a";
            var e = "inner e";
            print a;
            print e;
            print w;
            print q;
          }
        }
        """

        assert "inner a\ninner e\nouter w\nglobal q\n" == run_code_block(source).out
