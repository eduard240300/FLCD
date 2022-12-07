class RecursiveDescendant:
    def __init__(self, productions, nonTerminals, terminals, transitions):
        self.__productions = productions
        self.__nonTerminals = nonTerminals
        self.__terminals = terminals
        self.__transitions = transitions

    def __expand(self, config):
        non_terminal = config["input_stack"][0]
        config["input_stack"] = config["working_stack"][1:]
        config["input_stack"].append(self.__productions[non_terminal][0])
        config["working_stack"].append([non_terminal, 0])

        return config

    def __advance(self, config):
        terminal = config['input_sequence'][config['position']]
        config['position'] = config['position'] + 1
        config['input_stack'] = config['input_stack'][1:]
        config['working_stack'].append([terminal, -1])

        return config

    def __momentaryInsuccess(self, config):
        config['state'] = 'b'

        return config

    def __back(self, config):
        config['position'] = config['position'] - 1
        terminal = config['working_stack'][-1]
        config['working_stack'] = config['working_stack'][:-1]
        config['input_stack'].insert(0, terminal)

        return config

    def __anotherTry(self, config):
        [non_terminal, non_terminal_position] = config['working_stack'][-1]
        if non_terminal_position + 1 < len(self.__productions[non_terminal]):
            config['status'] = 'q'
            config['working_stack'][-1] = [non_terminal, non_terminal_position + 1]
            config['input_stack'][0] = self.__productions[non_terminal][non_terminal_position + 1]
        elif config['position'] == 0 and non_terminal == 'S':
            config['status'] = 'e'
            config['working_stack'] = config['working_stack'][:-1]
            config['input_stack'] = config['input_stack'][1:]
        else:
            config['status'] = 'b'
            config['working_stack'] = config['working_stack'][:-1]
            config['input_stack'].insert(0, non_terminal)

        return config

    def __success(self, config):
        config['status'] = 'f'

        return config

    def __buildStringOfProd(self, config):
        prod = ''
        i = len(config['working_stack']) - 1

        while i >= 0:
            if config['working_stack'][i][1] != -1:
                prod += str(config['working_stack'][i][1])
                i = i - 1

        return prod

    def check(self, input):
        config = {"state": "q", "position": "0", "working_stack": [], "input_stack": [self.__transitions], "input_sequence": input}

        while (config['state'] != 'f') and (config['state'] != 'e'):
            if config['state'] == 'q':
                if (config['position'] == len(config['input_sequence'])) and len(config['inputStack']) == 0:
                    config = self.__success(config)
                else:
                    if config['input_stack'][0] in self.__nonTerminals:
                        config = self.__expand(config)
                    else:
                        if config['inputStack'][0] == config['input_sequence'][config['position']]:
                            config = self.__advance(config)
                        else:
                            config = self.__momentaryInsuccess(config)
            else:
                if config['state'] == 'b':
                    if config['working_stack'][0][0] in self.__terminals:
                        config = self.__back(config)
                    else:
                        config = self.__anotherTry(config)
        if config['state'] == 'e':
            print('Error')
            return null
        else:
            print('Sequence accepted')
            return self.__buildStringOfProd(config['workingState'])