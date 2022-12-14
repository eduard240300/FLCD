from recursiveDescendent import RecursiveDescendent

class Grammar:
    def __init__(self, fileName):
        file = open(fileName, "r")
        self.__nonTerminals = self.__parseLine(file.readline()[:-1])
        self.__terminals = self.__parseLine(file.readline()[:-1])
        self.__transitions = file.readline()[4:-1]
        self.__productions = self.__parseProductions(file.readlines())

    def __parseLine(self, line):
        line = line[0] + "@" + line[2:]
        return [value for value in line.split("@")[1][3:-1].split(", ")]

    def __parseProductions(self, lines):
        productions = {}

        for line in lines:
            key = line[5:-1].split("->")[0]
            value = line[5:-1].split("->")[1]
            if key in productions.keys():
                productions[key].append(value)
            else:
                productions[key] = [value]

        return productions

    def getNonTerminals(self):
        return self.__nonTerminals

    def getTerminals(self):
        return self.__terminals

    def getProductions(self):
        return self.__productions

    def getTransitions(self):
        return self.__transitions

    def __expand(self, config):
        pass

    def cfgCheck(self):
        recursiveDescendent = RecursiveDescendent(self.__productions, self.__nonTerminals, self.__terminals, self.__transitions)
        return recursiveDescendent.check()

    def getProductionsForNonTerminal(self, nonTerminal):
        result = ""
        if nonTerminal in self.__productions.keys():
            result += nonTerminal
            result += " -> "
            for elem in self.__productions[nonTerminal]:
                if result[-2] != ">":
                    result += "|"
                result += elem
            return result
        else:
            return nonTerminal + " is not a non terminal !"