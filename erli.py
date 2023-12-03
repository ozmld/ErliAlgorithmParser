import ast

from grammar import Grammar


class ErliParser:
    class Situation:
        def __init__(self, left_part: str, right_part: str, read_num: int, cursor_pos: int):
            self.left_part: str = left_part
            self.right_part: str = right_part
            self.read_num: int = read_num
            self.cursor_pos: int = cursor_pos

        def __hash__(self):
            return hash(self.left_part + self.right_part + str(self.read_num) + str(self.cursor_pos))

        def __eq__(self, other):
            return self.left_part == other.left_part and self.right_part == other.right_part

        def __repr__(self):
            return self.left_part + "->" + self.right_part[0:self.cursor_pos] + "*" + self.right_part[self.cursor_pos:] + f" ({self.read_num})"

    class D:
        def __init__(self):
            self.situations_list: list[ErliParser.Situation] = []
            self.situations: set = set()

        def add_situation(self, situation):
            if situation not in self.situations:
                self.situations_list.append(situation)
                self.situations.add(situation)

    def __init__(self):
        self.grammar: Grammar = Grammar()
        self.blocks: list[ErliParser.D] = []

    def __scan(self, letter: str):
        if letter not in self.grammar.terminals:
            raise AttributeError(f"letter \"{letter}\" must be a terminal in grammar")
        next_block = ErliParser.D()
        for situation in self.blocks[-1].situations_list:
            if situation.cursor_pos >= len(situation.right_part):
                continue
            if situation.right_part[situation.cursor_pos] == letter:
                new_situation = situation
                new_situation.cursor_pos += 1
                if new_situation in next_block.situations:
                    continue
                next_block.situations_list.append(new_situation)
                next_block.situations.add(new_situation)
        self.blocks.append(next_block)

    def __complete(self, situation):
        if situation.cursor_pos != len(situation.right_part):
            return
        for situation_to_complete in self.blocks[situation.read_num].situations_list:
            if situation_to_complete.cursor_pos >= len(situation_to_complete.right_part):
                continue
            if situation_to_complete.right_part[situation_to_complete.cursor_pos] != situation.left_part:
                continue
            new_situation = ErliParser.Situation(situation_to_complete.left_part,
                                                 situation_to_complete.right_part,
                                                 situation_to_complete.read_num,
                                                 situation_to_complete.cursor_pos + 1)
            if new_situation not in self.blocks[-1].situations:
                self.blocks[-1].situations_list.append(new_situation)
                self.blocks[-1].situations.add(new_situation)

    def __predict(self, situation):
        if situation.cursor_pos >= len(situation.right_part):
            return
        if situation.right_part[situation.cursor_pos] not in self.grammar.non_terminals:
            return
        for rule in self.grammar[situation.right_part[situation.cursor_pos]]:
            new_situation = ErliParser.Situation(rule.left_part,
                                                 rule.right_part,
                                                 len(self.blocks) - 1,
                                                 0)
            if new_situation not in self.blocks[-1].situations:
                self.blocks[-1].situations_list.append(new_situation)
                self.blocks[-1].situations.add(new_situation)

    def fit(self, grammar: Grammar):
        self.grammar = grammar

    def predict(self, word: str) -> bool:
        new_block = ErliParser.D()
        new_block.add_situation(ErliParser.Situation(self.grammar.new_start,
                                                     self.grammar.start_non_terminal,
                                                     0,
                                                     0,))
        self.blocks = [new_block]
        i = 0
        while i < len(self.blocks[-1].situations_list):
            situation = self.blocks[-1].situations_list[i]
            self.__predict(situation)
            self.__complete(situation)
            i += 1
        for letter in word:
            self.__scan(letter)
            i = 0
            while i < len(self.blocks[-1].situations_list):
                situation = self.blocks[-1].situations_list[i]
                self.__predict(situation)
                self.__complete(situation)
                i += 1
        return ErliParser.Situation(self.grammar.new_start,
                                    self.grammar.start_non_terminal,
                                    0,
                                    1,) in self.blocks[-1].situations

