from grammar import Grammar
from recursive_descendent import RecursiveDescendent

def main():
    f = open("out1.txt", "w")
    grammar = Grammar()
    grammar.read_grammar("g1.txt")

    rd = RecursiveDescendent(grammar, "aca")

    productions, result = rd.start()

    f.write(result + '\n')

    if result == "success":
        f.write(productions + '\n')
    for i in rd.get_parsing_tree():
        f.write(str(i) + '\n')
    f.close()

if __name__ == "__main__":
    main()
