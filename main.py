from erli import ErliParser
from grammar import Grammar
ANSWERS = {True: "Yes", False: "No"}
if __name__ == '__main__':
    non_terminals_num, terminals_num, rules_num = map(int, input().split())
    non_terminals = list(input())
    terminals = list(input())
    grammar = Grammar(terminals,
                      non_terminals,)
    for i in range(rules_num):
        rule = input().replace(" ", "")
        grammar.add_rule(rule)
    erli_parser = ErliParser()
    start_non_terminal = input()
    grammar.set_start_non_terminal(start_non_terminal)
    erli_parser.fit(grammar)
    words_num = int(input())
    for i in range(words_num):
        word = input()
        for letter in word:
            if letter not in grammar.terminals:
                raise AttributeError(f"letter \"{letter}\" of the word \"{word}\" must be a terminal in grammar")
        print(ANSWERS[erli_parser.predict(word)])
