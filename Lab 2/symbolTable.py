class symbolTable:
    def __init__(self):
        self.__hashTable = []
        self.__positions = 16
        self.__occupiedPositions = 0
        for i in range(0, self.__positions):
            self.__hashTable.append(None)

    def getHashTable(self):
        return self.__hashTable

    def __resizeHashTable(self):
        oldPositions = self.__positions
        self.__positions *= 2
        oldHashMap = self.__hashTable
        self.__hashTable = []
        for i in range(0, self.__positions):
            self.__hashTable.append(None)
        self.__occupiedPositions = 0
        for i in range(0, oldPositions):
            if oldHashMap[i] is not None:
                self.add(oldHashMap[i])

    def __getHashPosition(self, symbol, index):
        hashValue = 0
        strSymbol = str(symbol)
        for i in range(0, len(strSymbol)):
            hashValue += ord(strSymbol[i])
        return ((hashValue % self.__positions) + index) % self.__positions

    def __find(self, symbol):
        index = 0
        while self.__hashTable[self.__getHashPosition(symbol, index)] != symbol:
            if self.__hashTable[self.__getHashPosition(symbol, index)] is None:
                return None
            index += 1
        return self.__getHashPosition(symbol, index)

    def add(self, symbol):
        if self.__find(symbol) is not None:
            return self.__find(symbol)
        else:
            index = 0
            while self.__hashTable[self.__getHashPosition(symbol, index)] is not None:
                index += 1
            position = self.__getHashPosition(symbol, index)
            self.__hashTable[position] = symbol
            self.__occupiedPositions += 1
            if self.__occupiedPositions > int(self.__positions * 3 / 4):
                self.__resizeHashTable()
                return self.__find(symbol)
            return position
