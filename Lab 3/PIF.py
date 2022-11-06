class PIF:
    def __init__(self):
        self.__PIFKeys = []
        self.__PIFValues = []

    def getSize(self):
        return len(self.__PIFKeys)

    def getPair(self, index):
        return [self.__PIFKeys[index], self.__PIFValues[index]]

    def addPair(self, key, value):
        self.__PIFKeys.append(key)
        self.__PIFValues.append(value)

    def translateToPositions(self, STIdentifiers, STConstants):
        for index in range(len(self.__PIFKeys)):
            value = None

            if self.__PIFKeys[index] == 'identifier':
                value = STIdentifiers.addOrGet(self.__PIFValues[index])
                self.__PIFValues[index] = value
            elif self.__PIFKeys[index] == 'constant':
                value = STConstants.addOrGet(self.__PIFValues[index])
                self.__PIFValues[index] = value