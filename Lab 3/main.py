from analyzer import Analyzer

class Main():
    def __init__(self):
        self.analyzer = Analyzer('./input/p2.eduard', './input/token.in')

    def outputPIF(self, PIF):
        f = open("PIF.out", "w")
        f.write("Data structure:\nTwo lists: one with the keys and one with the values\n\n")

        for index in range(PIF.getSize()):
            pair = PIF.getPair(index)
            output = str(pair[0]) + " " + str(pair[1])
            f.write(output + "\n")
        f.close()

    def outputST(self, STIdentifiers, STConstants):
        hashMapIdentifiers = STIdentifiers.getHashTable()
        hashMapConstants = STConstants.getHashTable()

        f = open("ST.out", "w")
        f.write("Data structure : Hash Map\n\n")
        f.write("Identifiers:\n")

        for index in range(len(hashMapIdentifiers)):
            if hashMapIdentifiers[index] != None:
                f.write(str(index) + ' ' + str(hashMapIdentifiers[index]) + '\n')

        f.write("\nConstants:\n")

        for index in range(len(hashMapConstants)):
            if hashMapConstants[index] != None:
                f.write(str(index) + ' ' + str(hashMapConstants[index]) + '\n')

        f.close()

    def outputErrors(self):
        message = "Lexical errors were encountered!"
        f = open("ST.out", "w")
        g = open("PIF.out", "w")
        f.write(message)
        g.write(message)
        f.close()
        g.close()


    def main(self):
        returnedValue = self.analyzer.analyze()
        if returnedValue == False:
            self.outputErrors()
        else:
            self.outputPIF(returnedValue[0])
            self.outputST(returnedValue[1], returnedValue[2])


if __name__ == '__main__':
    main = Main()
    main.main()

