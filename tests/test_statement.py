from yaplox.yaplox import Yaplox


class TestStatement:
    def test_statement(self, capsys):
        source = [
            "var a = 234;",
            "print(a);",
        ]
        source = "\n".join(source)

        Yaplox().run(source)
        captured = capsys.readouterr()
        assert captured.out == "234\n"

    def test_nested(self, capsys):
        """ Execute the example code from the book """
        source = """
        var a = "global a";
        var b = "global b";
        var c = "global c";
        {
          var a = "outer a";
          var b = "outer b";
          {
            var a = "inner a";
            print a;
            print b;
            print c;
          }
          print a;
          print b;
          print c;
        }
        print a;
        print b;
        print c;
        """

        Yaplox().run(source)
        captured = capsys.readouterr()
        expected = [
            "inner a",
            "outer b",
            "global c",
            "outer a",
            "outer b",
            "global c",
            "global a",
            "global b",
            "global c",
            "",  # Add empty line for terminating \n
        ]
        expected_str = "\n".join(expected)
        assert captured.out == expected_str
