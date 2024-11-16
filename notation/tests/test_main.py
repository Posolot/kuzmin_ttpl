from ..notation.main import prefix_to_infix


class TestPrefix:
    def test_good(self):
        assert prefix_to_infix("+ - 13 4 55") == "((13 - 4) + 55)"
        assert prefix_to_infix("+ 2 * 2 - 2 1") == "(2 + (2 * (2 - 1)))"
        assert prefix_to_infix("+ + 10 20 30") == "((10 + 20) + 30)"

    def test_bad(self):
        assert prefix_to_infix("- - 1 2") == "Нехватка операндов для оператора - в выражении (- - 1 2)"
        assert prefix_to_infix("2 + 2 2") == "Некорректное количество операндов или операторов в выражении (2 + 2 2)"

    def test_hard(self):
        assert prefix_to_infix("/ + 3 10 * + 2 3 - 3 5") == "((3 + 10) / ((2 + 3) * (3 - 5)))"
