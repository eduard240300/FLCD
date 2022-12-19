class ParserOutput:
    def __init__(self, outFile, productions, transitions, terminals, nonTerminals):
        self.__outFileWriter = open(outFile, 'w')
        self.__terminals = terminals
        self.__nonTerminals = nonTerminals
        self.__productions = productions
        self.__transitions = transitions
        self.__currentLine = 0

    def print_line(self, line):
        print(line)
        self.__outFileWriter.write(line + "\n")
        self.__currentLine += 1

    def print_config(self, config, step_name):
        line = step_name
        if self.__currentLine > 0:
            line = "\n" + line
        self.print_line(line)
        self.print_line("State: '" + str(config["state"]) + "'")
        self.print_line("Position: '" + str(config["position"]) + "'")
        self.print_line("Working Stack: " + str(config["alpha"]))
        self.print_line("Input Stack: " + str(config["beta"]))
        self.print_line("Input Sequence: " + str(config["input_sequence"]))

    # w does belong to L(G) - HOW
    # Process alpha:
    #   From left to right (reverse if stored as stack)
    #   Skip terminal symbols
    #   Nonterminals - index of prod
    # Example: alpha = S1 a S2 a S3 c b S3 c
    def build_productions_string(self, config):
        productionString = ""
        i = 0

        while i < len(config["alpha"]):
            if config["alpha"][i][1] != -1:
                production_number = self.compute_production_number(config["alpha"][i])
                productionString += str(production_number) + " "
            i = i + 1

        self.print_line("Productions String: " + productionString)

        return productionString

    def compute_production_number(self, non_terminal_pair):
        non_terminal = non_terminal_pair[0]
        non_terminal_production = non_terminal_pair[1]
        keys = list(self.__productions.keys())
        production_number = 0

        i = 0
        while i < len(keys):
            if keys[i] == non_terminal:
                production_number += int(non_terminal_production)
                i = len(keys)
            else:
                production_number += len(self.__productions[keys[i]])
            i = i + 1

        return production_number

    def get_parse_tree(self, config):
        stack = []
        parseTree = []
        if type(self.__transitions) == str:
            stack.append(self.__transitions)
        else:
            for transition in self.__transitions:
                stack.append(transition)

        index = 0
        position = 0
        parent = -1
        nextProductions = []
        while len(stack) > 0:
            positionStack = 0
            leftSibling = -1
            for element in stack:
                parseTree.append([position, stack[positionStack], parent, leftSibling])
                if positionStack < len(stack) - 1:
                    leftSibling = index
                if stack[positionStack] in self.__nonTerminals:
                    parent = index
                    nextProductions.append([self.__productions[config["alpha"][index][0]][config["alpha"][index][1]], parent, index + 1])
                index += 1
                position += 1
                positionStack += 1

            stack = []
            if len(nextProductions) > 0:
                [nextProduction, parent, index] = nextProductions[0]
                nextProductions = nextProductions[1:]
                values = nextProduction.split(" ")
                for value in values:
                    stack.append(value)

        self.print_line("\nParse Tree:\nIndex      Info         Parent      Left Sibling")
        distances = [11, 13, 12]
        for row in parseTree:
            output = ""
            distance1 = distances[0] - len(str(row[0]))
            output += str(row[0])
            for i in range(distance1):
                output += " "

            distance2 = distances[1] - len(str(row[1]))
            output += str(row[1])
            for i in range(distance2):
                output += " "

            distance3 = distances[2] - len(str(row[2]))
            output += str(row[2])
            for i in range(distance3):
                output += " "

            output += str(row[3])
            self.print_line(output)

