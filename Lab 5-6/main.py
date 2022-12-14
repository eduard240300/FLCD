from grammar import Grammar
from recursiveDescendent import RecursiveDescendent

def run_menu(gr):
    options = [gr.getNonTerminals, gr.getTerminals, gr.getProductions, gr.cfgCheck, gr.getProductionsForNonTerminal]
    recursiveDescendent = RecursiveDescendent(gr.getProductions(), gr.getNonTerminals(), gr.getTerminals(), gr.getTransitions())

    while True:
        print("1. Show Non Terminals")
        print("2. Show Terminals")
        print("3. Show Productions")
        print("4. CFG Check ?")
        print("5. Show Productions For Non Terminal")
        print("0. Exit")

        choice = int(input(">> "))
        if choice > 5:
            print("Invalid command!\n")
        elif choice == 0:
            return
        elif choice == 4:
            input_sequence = input("Input sequence: ")
            productionString = recursiveDescendent.check(input_sequence)
            if productionString == None:
                pass
            else:
                print("Production string: " + productionString)
        elif choice == 5:
            nonTerminal = input("Non Terminal: ")
            productions = options[choice - 1](nonTerminal)
            print(productions)
        else:
            value = options[choice - 1]()
            print(value)

        print("")

if __name__ == "__main__":
    grammar = Grammar("g1.txt")
    run_menu(grammar)