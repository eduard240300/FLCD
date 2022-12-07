from recursiveDescendant import RecursiveDescendant

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

    def cfgCheck(self):
        recursiveDescendant = RecursiveDescendant(self.__productions, self.__nonTerminals, self.__terminals, self.__transitions)
        return recursiveDescendant.check()

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