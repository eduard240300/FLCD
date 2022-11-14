class FiniteAutomata:
    def __init__(self, fileName):
        file = open(fileName, 'r')
        lines = [line.replace('\n', '') for line in file.readlines()]
        file.close()

        self.__states = lines[0].split(',')
        self.__alphabet = lines[1].split(',')
        self.__initialState = lines[2]
        self.__finalStates = lines[3].split(',')
        self.__transitions = []

        for index in range(4,len(lines)):
            splitTransition = lines[index].split('->')
            splitKey = splitTransition[0].split(',')
            self.__transitions.append([splitKey, splitTransition[1]])

    def getStates(self):
        return self.__states

    def getAlphabet(self):
        return self.__alphabet

    def getInitialState(self):
        return self.__initialState

    def getFinalStates(self):
        return self.__finalStates

    def getTransitions(self):
        return self.__transitions

    def isDFA(self):
        parsedTransitions = []
        for transition in self.__transitions:
            if transition[0] in parsedTransitions:
                return False
            parsedTransitions.append(transition[0])
        return True

    def isAccepted(self, sequence):
        if self.isDFA():
            sequence = sequence.replace('\n', '').split(',')
            state = self.__initialState
            for element in sequence:
                found = False
                index = 0
                while index < len(self.__transitions) and not found:
                    if [state, element] == self.__transitions[index][0]:
                        state = self.__transitions[index][1]
                        found = True
                    index = index + 1
                if not found:
                    break
            if state in self.__finalStates and found:
                return [True, 'Accepted']
            else:
                return [True, 'Not accepted']
        else:
            return [False, 'Not DFA']