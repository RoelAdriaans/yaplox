from yaplox.yaplox import Yaplox


class TestControl:
    def test_if_else(self, capsys):
        statement = [
            "var a = 4;",
            "if (a == 4) {",
            '    print "a == 4";',
            "}",
            "if (a != 5) {",
            '    print "a != 5";',
            "} else {",
            '    print "a == 5";',
            "}",
        ]
        source = "\n".join(statement)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()
        assert captured.out == "a == 4\na != 5\n"

    def test_if_or(self, capsys):
        statement = [
            "var a = 4;",
            "var b = 3;",
            'if (a == 3 or b == 3) { print "or b == 3"; } ',
            'if (a == 3 or b == 4) { print ""; } else { print "both false"; } ',
            'if (a == 4 or b == 3) { print "or true"; } else { print ""; } ',
            'if (a == 4 or b == 4) { print "only a true"; } else { print ""; } ',
            'if (a == 4 and b == 3) { print "a and b"; } else { print ""; } ',
            'if (a == 3 and b == 3) { print ""; } else { print "a != 3"; } ',
        ]
        source = "\n".join(statement)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()
        assert captured.out == (
            "or b == 3\n"
            "both false\n"
            "or true\n"
            "only a true\n"
            "a and b\n"
            "a != 3\n"
        )

    def test_empty_else(self, capsys):
        statement = [
            "var a = 4;",
            "if (a == 4) {} else {}",
            "if (a == 5) {} else {}",
            "if (a) {} else {}",
            "if (!a) {} else {}",
        ]
        source = "\n".join(statement)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

    def test_missing_paren(self, capsys):
        """ Test missing ( and ) in if statements"""
        complete_statement = [
            "var a = 4;" "if (a == 4) {",
            '    print "Four!";',
            "}",
        ]

        source = "\n".join(complete_statement)
        left_missing = source.replace("(", "")
        right_missing = source.replace(")", "")

        # Test a valid statement
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()
        assert captured.out == "Four!\n"

        # Test with left ( missing error, on a clean yaplox instance
        yaplox = Yaplox()
        yaplox.run(left_missing)

        assert yaplox.had_error

        captured = capsys.readouterr()
        assert "Expect '(' after 'if'." in captured.err

        # Test with right ) missing error, on a clean yaplox instance
        yaplox = Yaplox()
        yaplox.run(right_missing)

        assert yaplox.had_error

        captured = capsys.readouterr()
        assert "Expect ')' after if condition." in captured.err

    def test_simple_while(self, capsys):
        source = [
            "var a = 0;",
            "",
            "while (a < 10) {",
            "    print a;",
            "    a = a + 1;",
            "}",
        ]

        source = "\n".join(source)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()
        expected_str_output = "\n".join([str(n) for n in range(10)]) + "\n"

        assert captured.out == expected_str_output

    def test_fibonacci_sequence(self, capsys):
        """ Compute fibonacci numbers """
        source = [
            "var a = 0;",
            "var b = 1;",
            "",
            "while (a < 10000) {",
            "  print a;",
            "  var temp = a;",
            "  a = b;",
            "  b = temp + b;",
            "}",
        ]
        source = "\n".join(source)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()

        # We expect the first 21 numbers:
        # fmt: off
        fibonacci = [
            0, 1, 1, 2, 3,
            5, 8, 13, 21, 34,
            55, 89, 144, 233, 377,
            610, 987, 1597, 2584, 4181,
            6765,
        ]
        # fmt: on
        expected_str_output = "\n".join([str(nr) for nr in fibonacci]) + "\n"

        assert captured.out == expected_str_output

    def test_for(self, capsys):
        source = [
            "for(var a = 0;  a <= 5; a = a + 1) {",
            "    print a;",
            "}",
        ]
        source = "\n".join(source)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()
        expected_str_output = "\n".join([str(n) for n in range(6)]) + "\n"

        assert captured.out == expected_str_output

    def test_for_empty_init(self, capsys):
        source = [
            "var a = 0;",
            "for(; a <= 5; a = a + 1) {",
            "    print a;",
            "}",
        ]
        source = "\n".join(source)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()
        expected_str_output = "\n".join([str(n) for n in range(6)]) + "\n"

        assert captured.out == expected_str_output

    def test_for_expression_init(self, capsys):
        source = [
            "var a;",
            "for(a = 0; a <= 5; a = a + 1) {",
            "    print a;",
            "}",
        ]
        source = "\n".join(source)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()
        expected_str_output = "\n".join([str(n) for n in range(6)]) + "\n"

        assert captured.out == expected_str_output
