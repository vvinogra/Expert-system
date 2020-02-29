import os
import sys
import pytest
sys.path.append("./")

from expert_system.parser.parser import Parser
from expert_system.parser.parser_exception import ParserException


def test_bad_files():
    run_tests(get_test_files("./tests/examples/bad_files"))


def get_test_files(path):
    matches = []

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            matches.append(filename)
    return matches


def run_tests(tests):
    for test in tests:
        with pytest.raises(ParserException):
            print("Testing file: {filename}".format(filename=test))
            parser = Parser(test)

