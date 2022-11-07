import re
from symbolTable import symbolTable
from PIF import PIF

class Analyzer:
    def __init__(self, __programFilename, __tokensFilename):
        self.__PIF = PIF()
        self.__STIdentifiers = symbolTable()
        self.__STConstants = symbolTable()
        self.__programFilename = __programFilename
        self.__tokensFilename = __tokensFilename
        self.__strings, self.__chars = [], []
        self.__lexicalErrors = []

        f = open(__tokensFilename, "r")
        self.tokens = [line.replace('\n', '') for line in f.readlines()]
        f.close()

    def __readFromFile(self):
        file = open(self.__programFilename, "r")
        lines = file.readlines()
        content = ""

        for line in lines:
            content += line

        return content

    def __addToSet(self, list, element):
        if element not in list:
            list.append(element)
            
        return list

    def __split(self, splitContents, splitValues, prefix):
        for indexValue in range(len(splitValues)):
            newSplitContents = []
            for contentPart in splitContents:
                if not contentPart.__contains__('token'):
                    parts = contentPart.split(splitValues[indexValue])
                else:
                    parts = [contentPart]

                for index in range(len(parts)):
                    newSplitContents.append(parts[index])
                    if index != len(parts) - 1:
                        newSplitContents.append(prefix + splitValues[indexValue])

            splitContents = newSplitContents

        return splitContents

    def __removeSeparators(self, splitContents):
        newSplitContents = []

        splitContents = self.__split(splitContents, ['\t', ' ', '\n'], '')
        for index in range(len(splitContents)):
            word = splitContents[index].replace('\t', '')\
                .replace('\n', '').replace(' ', '')
            if word != '':
                newSplitContents.append(word)

        return newSplitContents

    def __separateStringsAndChars(self, fileContents):
        currentString, currentChar, inString, inChar = '', '', False, False
        line = 1
        splitContents = [fileContents]

        for character in fileContents:
            if character == '\n':
                if inString:
                    currentString = ''
                    self.__lexicalErrors.append("line " + str(line) + ": double quotes were opened and not closed!")
                    inString = not inString
                if inChar:
                    if (len(currentChar) > 3):
                        self.__lexicalErrors.append("line " + str(line) + ": a char can't be longer than one character!")
                    currentChar = ''
                    self.__lexicalErrors.append("line " + str(line) + ": simple quotes were opened and note closed!")
                    inChar = not inChar
                line += 1
            elif character == '"':
                currentString += character
                if inString:
                    self.__strings = self.__addToSet(self.__strings, currentString)
                    currentString = ''
                inString = not inString
            elif character == "'":
                if inString:
                    currentString += character
                else:
                    currentChar += character
                    if inChar:
                        self.__chars = self.__addToSet(self.__chars, currentChar)
                        if (len(currentChar) > 3):
                            self.__lexicalErrors.append("line " + str(line) + ": a char can't be longer than one character!")
                        currentChar = ''
                    inChar = not inChar
            else:
                if inString:
                    currentString += character
                elif inChar:
                    currentChar += character

        splitContents = self.__split(splitContents, self.__strings, '')
        for indexString in range(len(self.__strings)):
            splitContents = [word.replace(self.__strings[indexString], 'str_' + str(indexString)) for word in splitContents]
        splitContents = self.__split(splitContents, self.__chars, '')
        for indexChar in range(len(self.__chars)):
            splitContents = [word.replace(self.__chars[indexChar], 'char_' + str(indexChar)) for word in splitContents]

        return splitContents

    def __addToSTAndPIF(self, type, word):
        if type == 'constant':
            self.__STConstants.addOrGet(word)
        elif type == 'identifier':
            self.__STIdentifiers.addOrGet(word)

        self.__PIF.addPair(type, word)

    def analyze(self):
        index = 0

        fileContents = self.__readFromFile()
        splitContents = self.__separateStringsAndChars(fileContents)
        splitContents = self.__split(splitContents, self.tokens, 'token_')
        splitContents = self.__removeSeparators(splitContents)

        for word in splitContents:
            if word.__contains__('token'):
                self.__PIF.addPair(word.replace('token_', ''), -1)
            else:
                if word.__contains__('str_'):
                    index = int(word.replace('str_', ''))
                    currentString = self.__strings[index]
                    self.__addToSTAndPIF('constant', currentString)
                elif word.__contains__('char'):
                    index = int(word.replace('char_', ''))
                    currentChar = self.__chars[index]
                    self.__addToSTAndPIF('constant', currentChar)
                else:
                    type = ''
                    if word in ['true', 'false']:  # boolean
                        type = 'constant'
                    elif re.search("^([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*$", word):  # identifier
                        type = 'identifier'
                    elif re.search("^([+]|-)?[1-9][0-9]*$", word) or word == '0':  # integer
                        type = 'constant'
                    else:
                        self.__lexicalErrors.append(word + " is not permitted as an identifier's name!")
                    self.__addToSTAndPIF(type, word)

        self.__PIF.translateToPositions(self.__STIdentifiers, self.__STConstants)

        if len(self.__lexicalErrors) > 0:
            print("Lexical errors:")
            for lexicalError in self.__lexicalErrors:
                print(lexicalError)
            return False

        return [self.__PIF, self.__STIdentifiers, self.__STConstants]