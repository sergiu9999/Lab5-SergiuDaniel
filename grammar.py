from collections import defaultdict

class Grammar:
    def __init__(self):
        self.starting_symbol = None
        self.non_terminals = []
        self.terminals = []
        self.productions = defaultdict(list)

    def get_starting_symbol(self):
        return self.starting_symbol

    def get_non_terminals(self):
        return self.non_terminals

    def get_terminals(self):
        return self.terminals

    def get_productions(self):
        return self.productions

    def read_grammar(self, file_name):
        f = open(file_name, "r")

        def current_line():
            return f.readline().strip()

        self.starting_symbol = current_line()
        self.terminals = current_line().split(',')
        self.non_terminals = current_line().split(',')
        if self.starting_symbol not in self.non_terminals:
            raise Exception("Starting symbol not in nonterminals")
        for raw_line in f.readlines():
            line = raw_line.strip()
            symbol_groups = line.split('->')
            if len(symbol_groups) != 2:
                raise Exception("Invalid production rule")
            left_side, right_side = symbol_groups
            left_symbols = left_side.strip().split(' ')
            if len(left_symbols) > 1:
                production_left = tuple(left_symbols)
            else:
                production_left = left_symbols[0]
            right_symbols = right_side.strip().split(' ')
            self.productions[production_left].append(right_symbols)

