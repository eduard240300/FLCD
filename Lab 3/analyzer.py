import re
from symbolTable import symbolTable

class Analyzer:
    def __init__(self):
        self.__tokenFile = "./input/token.in"
        f = open(self.__tokenFile, "r")

        self.__tokens = f.readlines()
        for i in range(len(self.__tokens)):
            self.__tokens[i] = self.__tokens[i].replace('\n', '')

        f.close()
        
        self.__PIFKeys = []
        self.__PIFValues = []
        self.__STIdentifiers = symbolTable()
        self.__STConstants = symbolTable()

    def outputPIF(self):
        f = open("PIF.out", "w")
        for index in range(len(self.__PIFKeys)):
            output = str(self.__PIFKeys[index]) + " " + str(self.__PIFValues[index])
            f.write(output + "\n")
        f.close()

    def outputST(self):
        hashMapIdentifiers = self.__STIdentifiers.getHashTable()
        hashMapConstants = self.__STConstants.getHashTable()

        f = open("ST.out", "w")
        f.write("Data structure : Hash Map\n\n")
        f.write("Identifiers:\n\n")

        for index in range(len(hashMapIdentifiers)):
            if hashMapIdentifiers[index] != None:
                f.write(str(index) + ' ' + str(hashMapIdentifiers[index]) + '\n')

        f.write("\nConstants:\n\n")

        for index in range(len(hashMapConstants)):
            if hashMapConstants[index] != None:
                f.write(str(index) + ' ' + str(hashMapConstants[index]) + '\n')

        f.close()

    def addToSTAndPIF(self, word, type):
        if type == 'constant':
            self.__STConstants.add(word)
        elif type == 'identifier':
            self.__STIdentifiers.add(word)

        self.__PIFKeys.append(type)
        self.__PIFValues.append(word)

    def getWords(self, fileContents):
        initialReadWords = re.split(' |\n|\t', fileContents)
        readWords = []
        for word in initialReadWords:
            if word != '':
                readWords.append(word)

        return readWords

    def readFromFile(self, fileName):
        file = open(fileName, "r")
        lines = file.readlines()
        content = ""

        for line in lines:
            content += line

        return content

    def checkProgram(self, fileName):
        error = False
        quotes = False
        index = 0

        fileContents = self.readFromFile(fileName)
        readWords = self.getWords(fileContents)

        quote = False
        stringWord = ""

        for word in readWords:
            if word in self.__tokens:
                self.__PIFKeys.append(word)
                self.__PIFValues.append(-1)
            else:
                if word[0] == '"': # string
                    quote = True
                    stringWord = word
                elif quote:
                    stringWord += " " + word
                    if word[-1] == '"':
                        quote = False
                        self.addToSTAndPIF(stringWord, 'constant')
                else:
                    type = ''
                    if re.search("^([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*$", word): # identifier
                        type = 'identifier'
                    elif word == 'true' or word == 'false': # boolean
                        type = 'constant'
                    elif re.search("^([+]|-)?[1-9][0-9]*$", word) or word == '0': # integer
                        type = 'constant'
                    elif re.search("^'([a-z]|[A-Z]|[0-9])'$", word): # char
                        type = 'constant'
                    self.addToSTAndPIF(word, type)

        for index in range(len(self.__PIFKeys)):
            realPifValue = None
            if self.__PIFKeys[index] == 'constant':
                realPifValue = self.__STConstants.add(self.__PIFValues[index])
                self.__PIFValues[index] = realPifValue
            elif self.__PIFKeys[index] == 'identifier':
                realPifValue = self.__STIdentifiers.add(self.__PIFValues[index])
                self.__PIFValues[index] = realPifValue

        self.outputPIF()
        self.outputST()