class TestClasses:
    def test_class(self, run_code_block):
        lines = """
        class DevonshireCream {
          serveOn() {
            return "Scones";
          }
        }

        print DevonshireCream; // Prints "DevonshireCream".
        """
        assert run_code_block(lines).out == "DevonshireCream\n"

    def test_class_instance_repr(self, run_code_block):
        lines = """
        class Bagel {}
        var bagel = Bagel();
        print bagel;
        """
        assert run_code_block(lines).out == "Bagel instance\n"

    def test_class_set_get(self, run_code_block):
        lines = """
        class Bagel {}
        var bagel = Bagel();
        bagel.sprinkles = "Chocolate";
        print bagel.sprinkles;
        """

        assert run_code_block(lines).err == ""
        assert run_code_block(lines).out == "Chocolate\n"

    def test_class_not_set_get(self, run_code_block):
        lines = """
        class Bagel {}
        var bagel = Bagel();
        print bagel.sprinkles;
        """

        assert (
            run_code_block(lines).err
            == "Undefined property 'sprinkles'. in line [line4]\n"
        )
        assert run_code_block(lines).out == ""

    def test_class_method_callable(self, run_code_block):
        lines = """
        class Bacon {
          eat() {
            print "Crunch crunch crunch!";
          }
        }

        Bacon().eat(); // Prints "Crunch crunch crunch!".
        """
        assert run_code_block(lines).err == ""
        assert run_code_block(lines).out == "Crunch crunch crunch!\n"

    def test_class_call_function_method(self, run_code_block):
        # We cannot call a method on a class itselve, we need an instance.
        # Lox does not support static methods
        lines = """
        class Foo {
            init() {
                print "Foo";
            }
        }
        print Foo.init();
        """
        assert (
            run_code_block(lines).err
            == "Only instances have properties. in line [line7]\n"
        )
        assert run_code_block(lines).out == ""

    def test_class_print_this(self, run_code_block):
        lines = """
        class Egotist {
          speak() {
            print this;
          }
        }

        var method = Egotist().speak;
        method();
        """
        assert run_code_block(lines).err == ""
        assert run_code_block(lines).out == "Egotist instance\n"

    def test_class_taste_cake(self, run_code_block):
        lines = """
            class Cake {
              taste() {
                var adjective = "delicious";
                print "The " + this.flavor + " cake is " + adjective + "!";
              }
            }

            var cake = Cake();
            cake.flavor = "German chocolate";
            cake.taste(); // Prints "The German chocolate cake is delicious!".
        """
        assert run_code_block(lines).err == ""
        assert run_code_block(lines).out == "The German chocolate cake is delicious!\n"

    def test_class_callback(self, run_code_block):
        lines = """
        class Thing {
          getCallback() {
            fun localFunction() {
              print this;
            }

            return localFunction;
          }
        }

        var callback = Thing().getCallback();
        callback();
        """
        assert run_code_block(lines).err == ""
        assert run_code_block(lines).out == "Thing instance\n"

    def test_this_outside_class(self, run_code_block):
        lines = "print this;"
        assert (
            run_code_block(lines).err
            == "[line 1] Error  at 'this' : Can't use 'this' outside of a class.\n"
        )
        assert run_code_block(lines).out == ""

    def test_this_in_fuction(self, run_code_block):
        lines = """
        fun foo() {
            print this;
        }
        """
        assert (
            run_code_block(lines).err
            == "[line 3] Error  at 'this' : Can't use 'this' outside of a class.\n"
        )
        assert run_code_block(lines).out == ""

    def test_class_init(self, run_code_block):
        lines = """
        class Foo {
          init() {
            print this;
          }
        }

        var foo = Foo();
        print foo.init();
        """
        assert run_code_block(lines).err == ""
        # Foo instance is printed 3 times, validated by jlox and clox:
        # 1st print statement is the init itselve
        # 2th is the print statement again, when running print foo.init()
        # 3th print is the return value of the init, the init instance
        assert run_code_block(lines).out == "Foo instance\nFoo instance\nFoo instance\n"

    def test_class_init_print_value(self, run_code_block):
        lines = """
        class Appelflap {
          init() {
            print "Appelflappen";
          }
        }

        var appelflap = Appelflap();
        print appelflap.init();
        """
        assert run_code_block(lines).err == ""
        # Foo instance is printed 3 times, validated by jlox and clox:
        # 1st print statement is the init itselve
        # 2th is the print statement again, when running print foo.init()
        # 3th print is the return value of the init, the init instance
        assert (
            run_code_block(lines).out
            == "Appelflappen\nAppelflappen\nAppelflap instance\n"
        )
