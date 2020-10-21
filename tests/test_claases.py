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
