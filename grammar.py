class Grammar:
    new_start = "&"

    class Rule:
        def __init__(self, left_part, right_part):
            self.left_part = left_part
            self.right_part = right_part

    parts_spliter = "->"

    def __init__(self, terminals: list[str]=[],
                 non_terminals: list[str]=[],
                 start_non_terminal: str="",
                 rules=None,
                 parts_spliter="->",):
        self.terminals = terminals
        self.non_terminals = non_terminals
        if rules is None:
            self.rules = []
        else:
            self.rules = rules
        self.parts_spliter = parts_spliter
        self.start_non_terminal = start_non_terminal

    def set_start_non_terminal(self, start_non_terminal):
        if start_non_terminal not in self.non_terminals:
            raise AttributeError(f"\"{start_non_terminal}\" not in non-terminal list")
        self.start_non_terminal = start_non_terminal

    def add_rule(self, rule: str):
        if self.parts_spliter not in rule:
            raise AttributeError(f"rule should contain \"{self.parts_spliter}\"")
        rule_parts = rule.split("->")
        if len(rule_parts) == 0:
            raise AttributeError("rule's left part can not be empty")
        if len(rule_parts) > 2:
            raise AttributeError(f"rule should contain exactly one \"{self.parts_spliter}\"")
        if rule_parts[0] not in self.non_terminals:
            raise AttributeError("rule's left part should consist of non-terminal")
        if len(rule_parts) == 1:
            self.rules.append(self.Rule(rule_parts[0], ""))
        self.rules.append(self.Rule(rule_parts[0], rule_parts[1]))

    def __getitem__(self, left_part: str) -> list[Rule]:
        rules_to_return: list[Grammar.Rule] = []
        for rule in self.rules:
            if rule.left_part == left_part:
                rules_to_return.append(rule)
        return rules_to_return
