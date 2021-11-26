class RecursiveDescendent:
    def __init__(self, grammar):
        self.grammar = grammar
        self.working_stack = [] # stores the way the parse is built
        self.input_stack = [] # part of the tree to be built
        self.state = "" # states: q - normal state, b - back state, f - final state, e - error state
        self.position = 0 # position of current symbol in input sequence

    def expand(self):
        # head of input stack is a nonterminal
        if self.position == self.input_stack.pop():
            pass

    def advance(self):
        # head of input stack is a terminal = current symbol from input
        self.position += 1
        pass

    def momentary_insuccess(self):
        # head of input stack is a terminal ≠ current symbol from input
        self.state = "b"
        return self.state

    def back(self):
        # head of working stack is a terminal
        if self.working_stack.pop() in self.grammar.terminals:
            pass
        self.position -= 1

    def another_try(self):
        # head of working stack is a nonterminal
        if self.working_stack.pop() in self.grammar.nonterminals:
            pass

    def success(self):
        self.state = "f"
        return self.state