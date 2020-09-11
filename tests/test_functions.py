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

    def test_return(self, capsys):
        """
        Test that a function can all itself.
        This code example is also from the crafting interpreters book
        """
        statement = [
            "fun add(a, b) {",
            "    var result =  (a - 1) + (b - 1);",
            "    return result + 2 ;",
            "}",
            "",
            "print add(3, 5);",
        ]
        source = "\n".join(statement)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()
        assert captured.out == "8\n"

    def test_recursive_fibonacci(self, capsys):
        """
        Example from crafting interpreters, a recursive Fibonacci function
        """
        statement = [
            "fun fib(n) {",
            "  if (n <= 1) return n;",
            "  return fib(n - 2) + fib(n - 1);",
            "}",
            "",
            "for (var i = 0; i < 20; i = i + 1) {",
            "  print fib(i);",
            "}",
        ]
        source = "\n".join(statement)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()

        # We expect the first 20 numbers:
        # fmt: off
        fibonacci = [
            0, 1, 1, 2, 3,
            5, 8, 13, 21, 34,
            55, 89, 144, 233, 377,
            610, 987, 1597, 2584, 4181,
        ]
        # fmt: on

        expected_str_output = "\n".join([str(nr) for nr in fibonacci]) + "\n"
        assert captured.out == expected_str_output

    def test_return_nothing(self, capsys):
        """
        Test a function that returns nothing
        """
        statement = [
            "fun return_nothing() { }",
            "print return_nothing();",
        ]
        source = "\n".join(statement)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()
        assert captured.out == "nil\n"

    def test_call_string(self, capsys):
        """
        Try to call a string. This must fail cleanly
        """
        source = '"ThisIsAstring"();'
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert yaplox.had_runtime_error

        captured = capsys.readouterr()
        assert captured.err == "Can only call functions and classes. in line [line1]\n"

    def test_return_in_the_middle(self, capsys):
        """
        Test that we can return from a function in the middle of a loop.
        It runs until 100, but will exit when n == 3, before printing n
        """
        statement = [
            "fun count(n) {",
            "  while (n < 100) {",
            "    if (n == 3) return n; // <--",
            "    print n;",
            "    n = n + 1;",
            "  }",
            "}",
            "",
            "count(1);",
        ]
        source = "\n".join(statement)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()
        assert captured.out == "1\n2\n"

    def test_empty_return(self, capsys):
        """
        This test looks like test_return_in_the_middle, but instead or returning n, it
        will return nothing.
        """
        statement = [
            "fun count(n) {",
            "  while (n < 100) {",
            "    if (n == 3) return; // <--",
            "    print n;",
            "    n = n + 1;",
            "  }",
            "}",
            "",
            "print count(1);",
        ]
        source = "\n".join(statement)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()
        assert captured.out == "1\n2\nnil\n"

    def test_closures(self, capsys):
        """
        Test closures, where a function in a function must have access to variables that
        are created in the first function.

        """
        statement = [
            "fun makeCounter() {",
            "  var i = 0;",
            "  fun count() {",
            "    i = i + 1;",
            "    print i;",
            "  }",
            "",
            "  return count;",
            "}",
            "",
            "var counter = makeCounter();",
            "counter(); // 1.",
            "counter(); // 2.",
        ]
        source = "\n".join(statement)
        yaplox = Yaplox()
        yaplox.run(source)

        assert not yaplox.had_error
        assert not yaplox.had_runtime_error

        captured = capsys.readouterr()
        assert captured.out == "1\n2\n"
