class Grammar:
    def __init__(self, fileName):
        file = open(fileName, 'r')
        self.__nonTerminals = self.__parseLine(file.readline())
        self.__terminals = self.__parseLine(file.readline())
        self.__transitions = file.readline()[2:]
        self.__productions = self.__parseProductions(file.readline())

    def __parseLine(self, line):
        return [value for value in line.split('=')[1][1:-1].split(',')]

    def __parseProductions(self, line):
        parsedLine = self.__parseLine(line)
        productions = {}

        for elem in parsedLine:
            newElem = elem[1:-1]
            key = newElem.split('->')[0]
            value = [e for e in newElem.split('->')[1].split('|')]
            productions[key] = value

        return productions

    def getNonTerminals(self):
        return self.__nonTerminals

    def getTerminals(self):
        return self.__terminals

    def getProductions(self):
        return self.__productions

    def __expand(self, config):
        pass

    def cfgCheck(self, config):
        while (config['state'] != 'f') and (config['state'] != 'e'):
            if config['state'] == 'q':
                if (config['position'] == config['length'] + 1) and len(config['inputStack']) == 0:
                    config = self.__success(config)
                else:
                    if self.__head(config['inputStack']) == 'A':
                        config = self.__expand(config)
                    else:
                        if self.__head(config['inputStack'] == 'ai'):
                            config = self.__advance(config)
                        else:
                            config = self.__momentaryInsuccess(config)
            else:
                if config['state'] == 'b':
                    if head('workingState') == 'a':
                        config = self.__back(config)
                    else:
                        config = self.__anotherTry(config)
        if config['state'] == 'e':
            print('Error')
            return null
        else:
            print('Sequence accepted')
            return self.__buildStringOfProd(config['workingState'])



    def getProductionsForNonTerminal(self, nonTerminal):
        result = ""
        if nonTerminal in self.__productions.keys():
            result += nonTerminal
            result += " -> "
            for elem in self.__productions[nonTerminal]:
                if result[-2] != '>':
                    result += " | "
                result += + elem
            return result
        else:
            return nonTerminal + " is not a non terminal !"