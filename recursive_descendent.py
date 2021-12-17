from grammar import Grammar
from enum import Enum

from tree import LabeledTree


class State(Enum):
    NORMAL = "q"
    BACK = "b"
    FINAL = "f"
    ERROR = "e"


class RecursiveDescendent:
    def __init__(self, grammar: Grammar, sequence) -> None:
        self.state = State.NORMAL
        self.grammar = grammar
        self.sequence = sequence
        self.position = 0
        self.working_stack = []
        self.input_stack = [grammar.get_starting_symbol()]
        self.f = open("out1.txt", "a")

    def expand(self):
        self.f.write("expand" + '\n')
        non_terminal = self.input_stack[0]
        production = self.grammar.productions[non_terminal][0]
        self.working_stack.append([non_terminal, 0])
        self.input_stack = production + self.input_stack[1:]

    def advance(self):
        self.f.write("advance" + '\n')
        self.position += 1
        self.working_stack.append(self.input_stack[0])
        self.input_stack = self.input_stack[1:]

    def momentary_insuccess(self):
        self.f.write("momentary insuccess" + '\n')
        self.state = State.BACK

    def back(self):
        self.f.write("back" + '\n')
        self.position -= 1
        self.input_stack = [self.working_stack[-1]] + self.input_stack
        self.working_stack.pop()

    def another_try(self):
        self.f.write("another_try" + '\n')
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
        self.f.write("success" + '\n')
        self.state = State.FINAL

    def get_production_string(self):
        production_string = ""
        for elem in self.working_stack:
            if elem in self.grammar.get_terminals():
                continue
            production_string += f"{elem[0]}{elem[1]} "
        return production_string

    def get_parsing_tree(self):
        production_tree = LabeledTree()
        for node_index, elem in enumerate(self.working_stack):
            if elem in self.grammar.get_terminals():
                production_tree.add_label(node_index, elem)
                continue
            production_tree.add_label(node_index, elem[0])
            children_labels = self.grammar.productions[elem[0]][elem[1]]
            for child_index, child in enumerate(children_labels):
                production_tree.add_son(node_index, node_index + child_index)
        return production_tree.get_table()

    def start(self):
        while self.state not in [State.FINAL, State.ERROR]:

            self.f.write('\n' + f"state {self.state}" + "\n")
            self.f.write(f"position:{self.position}" + "\n")
            self.f.write(f"working stack: {self.working_stack}" + "\n")
            self.f.write(f"input stack: {self.input_stack}" + "\n")
            self.f.write("\n")

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
