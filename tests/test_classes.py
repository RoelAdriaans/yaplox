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
