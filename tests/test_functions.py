from yaplox.yaplox import Yaplox


class TestFunctions:
    def test_say_hi(self, capsys):
        """ "
        The example function that is in chapter 10.4.1
        """
        statement = [
            "fun sayHi(first, last) {",
            '  print "Hi, " + first + " " + last + "!";',
            "}",
            "",
            'sayHi("Dear", "Reader");',
        ]
        source = "\n".join(statement)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()
        assert captured.out == "Hi, Dear Reader!\n"

    def test_clock(self, capsys):
        """
        Test the clock function, should return a time.
        Since this will return the actual time, we just validate that it's an number
        """
        source = "print clock();"
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()
        # Remove the newlines
        time_float = float(captured.out)
        assert isinstance(time_float, float)

    def test_no_arguments(self, capsys):
        statement = [
            "fun say_no_args() {",
            '  print "Hi, I have no arguments";',
            "}",
            "",
            "say_no_args();",
        ]
        source = "\n".join(statement)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()
        assert captured.out == "Hi, I have no arguments\n"

    def test_no_arguments_still_arguments_given(self, capsys):
        statement = [
            "fun say_no_args() {",
            '  print "Hi, I have no arguments";',
            "}",
            "",
            'say_no_args("But", "here", "We", "Are");',
        ]
        source = "\n".join(statement)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert yaplox.had_runtime_error

        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == "Expected 0 arguments but got 4. in line [line5]\n"

    def test_arguments_but_none_given(self, capsys):
        statement = [
            "fun sayHi(first, last) {",
            '  print "Hi, " + first + " " + last + "!";',
            "}",
            "",
            "// Prince doesn't have a last name...",
            'sayHi("Prince");',
        ]

        source = "\n".join(statement)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert yaplox.had_runtime_error

        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == "Expected 2 arguments but got 1. in line [line6]\n"

    def test_too_many_parameters_in_definition(self, capsys):
        parameters = ", ".join([f"arg_{n:03}" for n in range(256)])

        statement = [
            f"fun sayHi({parameters}) {{",
            '  print "Hi!";',
            "}",
        ]

        source = "\n".join(statement)
        yaplox = Yaplox()
        yaplox.run(source)

        # This should give a parse error
        assert yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()
        assert captured.out == ""
        # This must give the error about too many parameters.
        assert (
            "[line 1] Error  at 'arg_255' : Cannot have more than 255 parameters."
            in captured.err
        )

    def test_too_many_arguments_in_call(self, capsys):
        arguments = ", ".join([f"arg_{n:03}" for n in range(256)])

        statement = ["fun sayHi() {", '  print "Hi!";', "}" "", f"sayHi({arguments});"]

        source = "\n".join(statement)
        yaplox = Yaplox()
        yaplox.run(source)

        # This should give a parse error
        assert yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()
        assert captured.out == ""
        # This must give the error about too many arguments.
        assert (
            "[line 4] Error  at 'arg_255' : Cannot have more than 255 arguments."
            in captured.err
        )

    def test_print_function(self, capsys):
        """ Test printing a function, and test if an empty body works """
        statement = [
            "fun my_function() {}",
            "",
            "print my_function;",
        ]
        source = "\n".join(statement)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()
        assert captured.out == "<fn my_function>\n"

    def test_recursion(self, capsys):
        """
        Test that a function can all itself.
        This code example is also from the crafting interpreters book
        """
        statement = [
            "fun count(n) {",
            "  if (n > 1) count(n - 1);",
            "  print n;",
            "}",
            "",
            "count(3);",
        ]
        source = "\n".join(statement)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()
        assert captured.out == "1\n2\n3\n"
