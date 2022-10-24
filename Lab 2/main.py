from symbolTable import symbolTable


def main():
    symbolTableConstants = symbolTable()
    symbolTableIdentifiers = symbolTable()
    while True:
        chosenSymbolTable = None
        firstChoice = input("( 1:constants / 2:identifiers / 3:exit ): ")
        if firstChoice == '1':
            chosenSymbolTable = symbolTableConstants
        elif firstChoice == '2':
            chosenSymbolTable = symbolTableIdentifiers
        elif firstChoice == '3':
            break

        secondChoice = input("( 1:add / 2:list ): ")
        if secondChoice == '1':
            symbol = input("> ")
            print("Position: " + str(chosenSymbolTable.add(symbol)))
        elif secondChoice == '2':
            output = 'List:\n'
            hashTable = chosenSymbolTable.getHashTable()
            for i in range(len(hashTable)):
                output += str(i) + ' -> ' + str(hashTable[i]) + '\n'
            print(output)


if __name__ == "__main__":
    main()
