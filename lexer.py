import lexeme
from lexer_exception import LexerException


class Lexer:

    def __init__(self, filename):
        self._filename = filename

        self._parsed_initial_facts = False
        self._parsed_queries = False
        self._true_initial_facts = []
        self._queries = []

        self._p

    def tokenize_file(self):
        with open(self._filename, "r") as file:
            for line in file:
                # Removing comment
                line = line.partition("#")[0]

                split_line = line.split()

                if len(split_line) == 1:
                    first_elem = split_line[0]

                    if first_elem.startswith("="):
                        self._check_for_initial_facts(first_elem)
                    elif first_elem.startswith("?"):
                        self._check_for_queries(first_elem)
                elif len(split_line) > 1:
                    for elem in split_line:
                        for lexeme_type, type_value in lexeme.LEXEME_TYPES.items():
                            if lexeme_type == "FACT":
                                if elem in type_value:



                            # if elem in type_value:
                            #     print(elem)
                            #     break
                            # else:
                            #     print("Error! Elem = " + elem)


                # for lexeme_type, type_value in lexeme.LEXEME_TYPES.items():
                #     if type_value

                # print(split_line)
                pass

        print(self._queries)
        print(self._true_initial_facts)

    def _check_for_initial_facts(self, facts):
        if self._parsed_initial_facts:
            raise LexerException("Initial facts line occurred twice")

        for fact in facts[1:]:
            if fact in lexeme.LEXEME_TYPES["FACT"]:
                self._true_initial_facts.append(fact)
            else:
                raise LexerException("Invalid fact in initial facts")

        self._parsed_initial_facts = True

    def _check_for_queries(self, queries):
        if self._parsed_queries:
            raise LexerException("Line with queries occurred twice")

        if len(queries) == 1:
            raise LexerException("No queries are specified")

        for query in queries[1:]:
            if query in lexeme.LEXEME_TYPES["FACT"]:
                self._queries.append(query)
            else:
                raise LexerException("Invalid fact in queries")

        self._parsed_queries = True

    def _check_for_