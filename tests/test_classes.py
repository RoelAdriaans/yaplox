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
