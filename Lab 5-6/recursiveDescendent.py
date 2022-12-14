class RecursiveDescendent:
    def __init__(self, productions, nonTerminals, terminals, transitions):
        self.__productions = productions # P
        self.__nonTerminals = nonTerminals # N
        self.__terminals = terminals # E
        self.__transitions = transitions # S

    # Formal model
    # Configuration: (s, i, alpha, beta)
    # Where:
    # s = state of the parsing, can be:
    #   q = normal state
    #   b = back state
    #   f = final state - corresponding to success: w does belong to L(G)
    #   e = error state - corresponding to insuccess: w does not belong to L(G)
    # i = position of current symbol in input sequence
    #   w = a0 a1 ... an, i does belong to {0, 1, ..., n}
    # alpha = working stack, stores the way the parse is built
    # beta  = input stack, part of the tree to be built
    # Initial configuration : (q, 0, epsilon, S)
    # Final configuration   : (f, n, alpha,   epsilon)


    # When: head of input stack is a nonterminal
    # (q, i, alpha, A beta) |- (q, i, alpha A0, gamma-0 beta)
    # where: A -> gamma-0|gamma-1|... represents the productions corresponding to A
    # 0 = first prod of A
    def expand(self, config):
        non_terminal = config["beta"][0]
        terminal = self.__productions[non_terminal][0]
        if terminal != "epsilon":
            terminals = terminal.split(" ")

            config["beta"] = config["beta"][1:]
            i = len(terminals) - 1
            while i >= 0:
                config["beta"].insert(0, terminals[i])
                i = i - 1

        config["alpha"].append([non_terminal, 0])

        return config

    # When: head of input stack is a terminal = current symbol from input
    # (q, i, alpha, ai beta) |- (q, i+1, alpha ai, beta)
    def advance(self, config):
        terminal = config["beta"][0]
        config["beta"] = config["beta"][1:]
        config["alpha"].append([terminal, -1])
        config["position"] = config["position"] + 1

        return config

    # When: head of input stack is a terminal != current symbol from input
    # (q, i, alpha, ai beta) |- (b, i, alpha, ai beta)
    def momentaryInsuccess(self, config):
        config["state"] = "b"

        return config

    # When: head of working stack is a terminal
    # (b, i, alpha a, beta) |- (b, i-1, alpha, a beta)
    def back(self, config):
        config["position"] = config["position"] - 1
        terminal = config["alpha"][-1][0]
        config["alpha"] = config["alpha"][:-1]
        config["beta"].insert(0, terminal)

        return config

    # When: head of working stack is a nonterminal
    # (b, i, alpha Aj, gamma-j beta) |- (q, i, alpha Aj+1, gamma-j+1 beta  ), if exists A -> gamma-j+1
    #                                   (b, i, alpha,      A beta          ), otherwise with the exception
    #                                   (e, i, alpha,      beta            ), if i = 0, A = S, ERROR
    def anotherTry(self, config):
        [non_terminal, non_terminal_position] = config["alpha"][-1]

        config["alpha"] = config["alpha"][:-1]
        terminal = self.__productions[non_terminal][non_terminal_position]
        if terminal == "epsilon":
            length = 0
        else:
            terminals = terminal.split(" ")
            length = len(terminals)
        config["beta"] = config["beta"][length:]

        if non_terminal_position + 1 < len(self.__productions[non_terminal]):
            config["state"] = "q"
            config["alpha"].append([non_terminal, non_terminal_position + 1])
            terminal = self.__productions[non_terminal][non_terminal_position + 1]
            if terminal != "epsilon":
                terminals = terminal.split(" ")
                i = len(terminals) - 1
                while i >= 0:
                    config["beta"].insert(0, terminals[i])
                    i = i - 1
        elif config["position"] == 0 and non_terminal == "S":
            config["state"] = "e"
        else:
            config["state"] = "b"
            config["beta"].insert(0, non_terminal)

        return config

    # (q, n, alpha, epsilon) |- (f, n, alpha, epsilon)
    def success(self, config):
        config["state"] = "f"

        return config

    # w does belong to L(G) - HOW
    # Process alpha:
    #   From left to right (reverse if stored as stack)
    #   Skip terminal symbols
    #   Nonterminals - index of prod
    # Example: alpha = S1 a S2 a S3 c b S3 c
    def buildStringOfProd(self, config):
        prod = ""
        i = 0

        while i < len(config["alpha"]):
            if config["alpha"][i][1] != -1:
                production_number = self.compute_production_number(config["alpha"][i])
                prod += str(production_number) + " "
            i = i + 1

        return prod

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

    def check(self, input_sequence):
        if type(input_sequence) != list:
            input_string = input_sequence

            length = len(input_string)
            if length == 0:
                print("Length 0 is not permitted!")
                return None

            input_sequence = input_string.split(" ")

        for sign in input_sequence:
            if sign not in self.__terminals:
                print(sign + " is not a terminal!")
                return None

        return self.__check(input_sequence)


    # Algorithm Descendent Recursive
    # INPUT: G, w = a0 a1 ... an
    # initial configuration (s, i, alpha, beta)
    def __check(self, input_sequence):
        config = {"state": "q", "position": 0, "alpha": [], "beta": [self.__transitions], "input_sequence": input_sequence}

        while (config["state"] != "f") and (config["state"] != "e"):
            if config["state"] == "q":
                if (config["position"] == len(config["input_sequence"])) and (len(config["beta"]) == 0):
                    config = self.success(config)
                else:
                    if (len(config["beta"]) > 0) and (config["beta"][0] in self.__nonTerminals):
                        config = self.expand(config)
                    else:
                        if (len(config["beta"]) > 0) and (config["beta"][0] == config["input_sequence"][int(config["position"])]):
                            config = self.advance(config)
                        else:
                            config = self.momentaryInsuccess(config)
            else:
                if config["state"] == "b":
                    if (len(config["alpha"]) > 0) and (config["alpha"][-1][0] in self.__terminals):
                        config = self.back(config)
                    elif (len(config["alpha"]) > 0):
                        config = self.anotherTry(config)
                    else:
                        print("The sequence was not accepted!")
                        return None
        if config["state"] == "e" or len(config["beta"]) > 0:
            print("The sequence was not accepted!")
            return None
        else:
            return self.buildStringOfProd(config)