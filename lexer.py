import lexeme
from lexer_exception import LexerException
import networkx as nx


class Lexer:

    def __init__(self, filename):
        self._filename = filename

        self._parsed_initial_facts = False
        self._parsed_queries = False
        self._true_initial_facts = []
        self._queries = []

        self._graph = nx.DiGraph()
        # self._graph.add_node(1)
        # self._graph.add_edge(1, 2)
        # print(self._graph)

    def tokenize_file(self):
        with open(self._filename, "r") as file:
            for line in file:
                # Removing comment
                line = line.partition("#")[0]

                # split_line = line.split()
                #
                # if len(split_line) == 1:
                #     first_elem = split_line[0]
                #
                #     if first_elem.startswith("="):
                #         self._check_for_initial_facts(first_elem)
                #     elif first_elem.startswith("?"):
                #         self._check_for_queries(first_elem)
                # elif len(split_line) > 1:
                self._add_rule(line)
                    # self._add_rule_to_graph(split_line)




                            # if elem in type_value:
                            #     print(elem)
                            #     break
                            # else:
                            #     print("Error! Elem = " + elem)


                # for lexeme_type, type_value in lexeme.LEXEME_TYPES.items():
                #     if type_value

                # print(split_line)
                pass

        # print(self._queries)
        # print(self._true_initial_facts)

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

    def _add_rule_to_graph(self, split_line):
        pass
        # for elem in split_line:
        #     if elem in lexeme.LEXEME_SEP_OPERATORS.value():
        #         pass

            # for lexeme_type, type_value in lexeme.LEXEME_TYPES.items():
            #     if lexeme_type == "FACT":
            #         if elem in type_value:
            #             pass
            #     else:
            #         pass

    def _create_rule(self, line):
        lexemes_list = []

        # split_line = line.split()

        # operands_count = 0
        braces_count = 0
        # conclusion_op = 0

        for i in range(len(line)):
            if line[i].isspace():
                continue
            elif line[i] in lexeme.LEXEME_TYPES["FACT"]:
                lexemes_list.append(lexeme.Lexeme(lexeme.LEXEME_TYPES["FACT"], line[i]))
            elif line[i] == lexeme.LEXEME_TYPES["LEFT_BRACE"]:
                braces_count += 1
                lexemes_list.append(lexeme.Lexeme(lexeme.LEXEME_TYPES["LEFT_BRACE"], line[i]))
            elif line[i] == lexeme.LEXEME_TYPES["RIGHT_BRACE"]:
                lexemes_list.append(lexeme.Lexeme(lexeme.LEXEME_TYPES["RIGHT_BRACE"], line[i]))
            else:
                cut_line = line[i:]

                for l_type, l_value in lexeme.LEXEME_OPERATORS.items():
                    if cut_line.startswith(l_value):
                        lexemes_list.append(lexeme.Lexeme(l_type, l_value))
                        break

        for i in lexemes_list:
            print(i._value)

        return lexemes_list
