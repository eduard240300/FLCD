from recursiveDescendent import RecursiveDescendent
from parserOutput import ParserOutput

class Tests:
    def __init__(self):
        self.recursiveDescendent = RecursiveDescendent({"S":["a A"],"A":["b A", "c", "epsilon"]}, ["S", "A", "C"], ["a", "b", "c"], "S", "test.out")
        self.parserOutput = ParserOutput("test.out", {"S":["a A"],"A":["b A", "c", "epsilon"]})

        self.test_expand()
        self.test_advance()
        self.test_momentaryInsuccess()
        self.test_back()
        self.test_anotherTry()
        self.test_success()
        self.test_build_productions_string()

    def test_expand(self):
        input_config = {"state": "q", "position": 0, "alpha": [], "beta": ["S"], "input_sequence": ["a", "b", "b", "b", "c"]}
        expected_output_config = {"state": "q", "position": 0, "alpha": [["S", 0]], "beta": ["a", "A"], "input_sequence": ["a", "b", "b", "b", "c"]}

        assert expected_output_config == self.recursiveDescendent.expand(input_config)

    def test_advance(self):
        input_config = {"state": "q", "position": 0, "alpha": [["S", 0]], "beta": ["a", "A"], "input_sequence": ["a", "b", "b", "b", "c"]}
        expected_output_config = {"state": "q", "position": 1, "alpha": [["S", 0], ["a", -1]], "beta": ["A"], "input_sequence": ["a", "b", "b", "b", "c"]}

        assert expected_output_config == self.recursiveDescendent.advance(input_config)

    def test_momentaryInsuccess(self):
        input_config = {"state": "q", "position": 0, "alpha": [["S", 0]], "beta": ["a", "A"], "input_sequence": ["b", "b", "b"]}
        expected_output_config = {"state": "b", "position": 0, "alpha": [["S", 0]], "beta": ["a", "A"], "input_sequence": ["b", "b", "b"]}

        assert expected_output_config == self.recursiveDescendent.momentaryInsuccess(input_config)

    def test_back(self):
        input_config = {"state": "b", "position": 2, "alpha": [["S", 0], ["a", -1], ["A", 1], ["c", -1]], "beta": [], "input_sequence": ["a", "c", "b"]}
        expected_output_config = {"state": "b", "position": 1, "alpha": [["S", 0], ["a", -1], ["A", 1]], "beta": ["c"], "input_sequence": ["a", "c", "b"]}

        assert expected_output_config == self.recursiveDescendent.back(input_config)

    def test_anotherTry(self):
        input_config = {"state": "b", "position": 1, "alpha": [["S", 0], ["a", -1], ["A", 0]], "beta": ["b", "A"], "input_sequence": ["a", "c", "b"]}
        expected_output_config = {"state": "q", "position": 1, "alpha": [["S", 0], ["a", -1], ["A", 1]], "beta": ["c"], "input_sequence": ["a", "c", "b"]}

        assert expected_output_config == self.recursiveDescendent.anotherTry(input_config)

    def test_success(self):
        input_config = {"state": "q", "position": 4, "alpha": [["S", 0], ["a", -1], ["A", 0], ["b", -1], ["A", 0], ["b", -1], ["A", 1], ["c", -1]], "beta": [], "input_sequence": ["a", "b", "b", "c"]}
        expected_output_config = {"state": "f", "position": 4, "alpha": [["S", 0], ["a", -1], ["A", 0], ["b", -1], ["A", 0], ["b", -1], ["A", 1], ["c", -1]], "beta": [], "input_sequence": ["a", "b", "b", "c"]}

        assert expected_output_config == self.recursiveDescendent.success(input_config)

    def test_build_productions_string(self):
        input_config = {"state": "f", "position": 5, "alpha": [["S", 0], ["a", -1], ["A", 0], ["b", -1], ["A", 0], ["b", -1], ["A", 0], ["b", -1], ["A", 1], ["c", -1]], "beta": [], "input_sequence": ["a", "b", "b", "b", "c"]}
        expected_output_production_string = "0 1 1 1 2 "

        assert expected_output_production_string == self.parserOutput.build_productions_string(input_config)


if __name__ == "__main__":
    Tests()