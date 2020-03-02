import os
import sys
import pytest
sys.path.append("./")

from expert_system.parser.parser import Parser
from expert_system.parser.parser_exception import ParserException

from expert_system.inference_engine.inference_engine import InferenceEngine
from expert_system.inference_engine.inference_engine_exception import InferenceEngineException

def get_test_files(path):
    matches = []

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            matches.append(os.path.join(dirpath, filename))
    return matches


def test_parser_error():
    tests = get_test_files("./tests/examples/parser_error")

    for test in tests:
        with pytest.raises(ParserException):
            print("Testing file: {filename}".format(filename=test))
            parser = Parser(test)
            parser.tokenize_file()


def test_inference_engine_error():
    tests = get_test_files("./tests/examples/inference_engine_error")

    for test in tests:
        with pytest.raises(InferenceEngineException):
            print("Testing file: {filename}".format(filename=test))
            parser = Parser(test)
            parser.tokenize_file()

            engine = InferenceEngine(verbose=False,
                                     queries=parser.queries,
                                     initial_facts=parser.initial_facts,
                                     rules=parser.rules)

            engine.resolve_queries()
