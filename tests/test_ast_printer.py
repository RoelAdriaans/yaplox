from yaplox import expr
from yaplox.ast_printer import AstPrinter
from yaplox.token import Token
from yaplox.token_type import TokenType


class TestAstPrinter:
    def test_astrinter(self):
        # This is the main/test function given in the chapter for the
        # ast_printer in chapter A (Not Very) pretty printer.
        # This code might be obsolete in the future, but it is a lot cleaner then
        # creating a main function to test our code.
        expression = expr.Binary(
            expr.Unary(Token(TokenType.MINUS, "-", None, 1), expr.Literal(123)),
            Token(TokenType.STAR, "*", None, 1),
            expr.Grouping(expr.Literal(45.67)),
        )

        result = AstPrinter().print(expression)
        assert result == "(* (- 123) (group 45.67))"

    def test_astrinter_nill(self):
        # Test a single edge case None
        expression = expr.Literal(None)

        result = AstPrinter().print(expression)
        assert result == "nil"
