from grammar import Grammar
from enum import Enum


class State(Enum):
    NORMAL = "q"
    BACK = "b"
    FINAL = "f"
    ERROR = "e"


class Recursive_descendent:
    def __init__(self, grammar: Grammar, sequence) -> None:
        self.state = State.NORMAL
        self.grammar = grammar
        self.sequence = sequence
        self.position = 0
        self.working_stack = []
        self.input_stack = [grammar.get_starting_symbol()]

    def expand(self):
        non_terminal = self.input_stack[0]
        production = self.grammar.productions[non_terminal][0]
        self.working_stack.append([non_terminal, 0])
        self.input_stack = production + self.input_stack[1:]

    def advance(self):
        self.position += 1
        self.working_stack.append(self.input_stack[0])
        self.input_stack = self.input_stack[1:]

    def momentary_insuccess(self):
        self.state = State.BACK

    def back(self):
        self.position -= 1
        self.input_stack = [self.working_stack[-1]] + self.input_stack
        self.working_stack.pop()

    def another_try(self):
        non_terminal, production_number = self.working_stack[-1]

        if production_number < len(self.grammar.productions[non_terminal]) - 1:

            pop_length = len(self.grammar.productions[non_terminal][production_number])
            self.input_stack = self.grammar.productions[non_terminal][production_number + 1] + self.input_stack[
                                                                                               pop_length:] #next production on input_stack
            self.working_stack[-1][1] += 1
            self.state = State.NORMAL

        else:
            if self.position == 0 and non_terminal == self.grammar.get_starting_symbol():
                self.state = State.ERROR
                return

            self.working_stack.pop()
            pop_length = len(self.grammar.productions[non_terminal][production_number])
            self.input_stack = [non_terminal] + self.input_stack[pop_length:]

    def success(self):
        self.state = State.FINAL

    def get_production_string(self):
        production_string = ""
        for elem in self.working_stack:
            if elem in self.grammar.get_terminals():
                continue
            production_string += f"{elem[0]}{elem[1]} "
        return production_string

    def start(self):
        while self.state not in [State.FINAL, State.ERROR]:

            if self.state == State.NORMAL:
                if self.position == len(self.sequence) and len(self.input_stack) == 0:
                    self.success()
                else:
                    if self.input_stack[0] in self.grammar.get_non_terminals():
                        self.expand()
                    else:
                        if self.position == len(self.sequence):
                            self.momentary_insuccess()
                        elif self.input_stack[0] == self.sequence[self.position]:
                            self.advance()
                        else:
                            self.momentary_insuccess()
            else:
                if self.state == State.BACK:
                    if self.working_stack[-1] in self.grammar.get_terminals():
                        self.back()
                    else:
                        self.another_try()

        if self.state == State.FINAL:
            return self.get_production_string(), "success"
        else:
            return [], "error"
