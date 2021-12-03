from grammar import Grammar
from recursive_descendent import Recursive_descendent

def main():
    grammar = Grammar()
    grammar.read_grammar("g1.txt")

    rd = Recursive_descendent(grammar, "aacbc")

    productions, result = rd.start()

    print(result)
    if result == "success":
        print(productions)

if __name__ == "__main__":
    main()
