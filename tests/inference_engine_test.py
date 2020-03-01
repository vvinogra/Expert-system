import os
import sys
import pytest
sys.path.append("./")

from expert_system.parser.parser import Parser
from expert_system.inference_engine.inference_engine import InferenceEngine


def test_basic_files(capsys):
    run_tests(get_test_files("./tests/examples/basic"), capsys)

# def test_basic_files():
#     run_tests(get_test_files("./tests/examples/error"))


def get_test_files(path):
    matches = []

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            matches.append(os.path.join(dirpath, filename))

    return matches


def run_tests(tests, capsys):
    for test in tests:
        captured = capsys.readouterr()

        print(test)
        parser = Parser(test)

        parser.tokenize_file()

        engine = InferenceEngine(verbose=False,
                                 graphic=False,
                                 interactive=False,
                                 queries=parser.queries,
                                 initial_facts=parser.initial_facts,
                                 rules=parser.rules)

        engine.resolve_queries()
