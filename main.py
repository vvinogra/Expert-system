#!/usr/bin/env python3

import sys
from lexer import Lexer


def check_python_version():
    assert sys.version_info >= (3, 0)


def validate_arguments(arguments):
    if len(arguments) != 2:
        print("Invalid number of arguments!")
        exit(1)


if __name__ == "__main__":
    check_python_version()
    validate_arguments(sys.argv)

    parser = Lexer(sys.argv[1])
    parser.tokenize_file()
