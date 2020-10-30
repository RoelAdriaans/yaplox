class TestClassesInheretance:
    def test_class_circular(self, run_code_block):
        line = "class Oops < Oops {}"

        assert (
            run_code_block(line).err
            == "[line 1] Error  at 'Oops' : A class can't inherit from itself.\n"
        )
        assert run_code_block(line).out == ""

    def test_class_not_a_class(self, run_code_block):
        lines = """
        var NotAClass = "I am totally not a class";
        class Subclass < NotAClass {} // ?!
        """
        assert (
            run_code_block(lines).err == "Superclass must be a class. in line [line3]\n"
        )
        assert run_code_block(lines).out == ""

    def test_class_inheritance(self, run_code_block):
        lines = """
        class Doughnut {
          cook() {
            print "Fry until golden brown.";
          }
        }

        class BostonCream < Doughnut {}

        BostonCream().cook();
        """

        assert run_code_block(lines).err == ""
        assert run_code_block(lines).out == "Fry until golden brown.\n"

    def test_class_call_super(self, run_code_block):
        lines = """
        class Doughnut {
          cook() {
            print "Fry until golden brown.";
          }
        }

        class BostonCream < Doughnut {
          cook() {
            super.cook();
            print "Pipe full of custard and coat with chocolate.";
          }
        }

        BostonCream().cook();
        // Prints:
        // Fry until golden brown.
        // Pipe full of custard and coat with chocolate."""

        captured = run_code_block(lines)

        assert captured.err == ""
        assert (
            captured.out == "Fry until golden brown.\n"
            "Pipe full of custard and coat with chocolate.\n"
        )

    def test_multiple_inherit(self, run_code_block):
        lines = """
        class A {
            method() {
                print "A method";
            }
        }

        class B < A {
            method() {
                print "B method";
            }

            test() {
                super.method();
            }
        }

        class C < B {}

        C().test();
        """
        captured = run_code_block(lines)

        assert captured.err == ""
        assert captured.out == "A method\n"
