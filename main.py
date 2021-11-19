import sys
class grammar:
    def __init__(self,file):
        self.file = open(file)
        self.terminals = []
        self.nonterminals = []
        self.production ={}
        self.initial=[]
    def parse_file(self):
        count=0

        for line in self.file:
            if count==0:

                self.initial.append(line.split(",")[0])
                for i in line.split(","):

                    self.nonterminals.append(i)
                self.nonterminals[-1]=self.nonterminals[-1][:-1]


            if count==1:
                for i in line.split(","):
                    self.terminals.append(i)
                self.terminals[-1] = self.terminals[-1][:-1]


            if count > 1:
                aux=0
                self.production[line.split(" -> ")[0]]=line.split(" -> ")[1][:-2]

            count = count + 1


    def print_info(self):

        print("Terminals: ",self.terminals)
        print("Non terminals: ",self.nonterminals)
        print("Production: ",self.production)
        print("Initial states: ",self.initial)


if __name__ == "__main__":
  gr=grammar("grammar.txt")
  gr.parse_file()
  gr.print_info()
