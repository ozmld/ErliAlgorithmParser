import pytest
from erli import ErliParser
from grammar import Grammar

DIRECTORY_PATH_PREFIX = "./test_grammars/"
NUMBER_OF_BAD_GRAMMARS = 3
PREFIX_OF_BAD_GRAMMAR = DIRECTORY_PATH_PREFIX + "test_bad_grammar_"
NUMBER_OF_GOOD_GRAMMARS = 3
PREFIX_OF_GOOD_GRAMMAR = DIRECTORY_PATH_PREFIX + "test_good_grammar_"
ANSWERS = {True: "Yes", False: "No"}


def test_on_bad_grammars():
    for i in range(1, NUMBER_OF_BAD_GRAMMARS + 1):
        with open(PREFIX_OF_BAD_GRAMMAR + str(i) + ".txt", 'r') as f:
            non_terminals_num, terminals_num, rules_num = map(int, f.readline().split())
            non_terminals = list(f.readline().rstrip())
            terminals = list(f.readline().rstrip())
            grammar = Grammar(terminals,
                              non_terminals, )
            for _ in range(rules_num):
                with pytest.raises(AttributeError):
                    rule = f.readline().rstrip().replace(" ", "")
                    grammar.add_rule(rule)


def test_on_good_grammars():
    for i in range(1, NUMBER_OF_GOOD_GRAMMARS + 1):
        with open(PREFIX_OF_GOOD_GRAMMAR + str(i) + ".txt", 'r') as f:
            non_terminals_num, terminals_num, rules_num = map(int, f.readline().split())
            non_terminals = list(f.readline().rstrip())
            terminals = list(f.readline().rstrip())
            grammar = Grammar(terminals,
                              non_terminals, )
            for _ in range(rules_num):
                rule = f.readline().rstrip().replace(" ", "")
                grammar.add_rule(rule)
            erli_parser = ErliParser()
            start_non_terminal = f.readline().rstrip()
            grammar.set_start_non_terminal(start_non_terminal)
            erli_parser.fit(grammar)
            words_num = int(f.readline().rstrip())
            for _ in range(words_num):
                word, ans = map(str, f.readline().rstrip().split("-"))
                assert ANSWERS[erli_parser.predict(word)] == ans
