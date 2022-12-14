class ParserOutput:
    def __init__(self, outFile, productions):
        self.__outFileWriter = open(outFile, 'w')
        self.__productions = productions

    def print_line(self, line):
        print(line)
        self.__outFileWriter.write(line + "\n")

    def print_config(self, config, step_name):
        self.print_line("\n" + step_name)
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