from grammar import Grammar

def run_menu(gr):
    options = [gr.getNonTerminals, gr.getTerminals, gr.getProductions, gr.cfgCheck, gr.getProductionsForNonTerminal]
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
        elif choice == 5:
            nonTerminal = input("Non Terminal: ")
            productions = options[choice - 1](nonTerminal)
            print(productions)
        else:
            value = options[choice - 1]()
            print(value)

if __name__ == '__main__':
    grammar = Grammar('g1.in')
    run_menu(grammar)