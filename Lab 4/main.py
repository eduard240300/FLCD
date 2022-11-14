from FA import FiniteAutomata

def run_menu(fa):
    options = [fa.getStates, fa.getAlphabet, fa.getInitialState, fa.getFinalStates, fa.getTransitions]
    while True:
        print("1. Show States")
        print("2. Show Alphabet")
        print("3. Show Initial State")
        print("4. Show Final States")
        print("5. Show Transitions")
        print("6. Is a sequence accepted?")
        print("0. Exit")

        choice = int(input(">> "))
        if choice > 6:
            print("Invalid command!\n")
        if choice == 0:
            return
        if choice == 6:
            sequence = input("Sequence: ")
            returnPair = fa.isAccepted(sequence)
            print(returnPair[1])
        elif choice == 5:
            transitions = options[choice - 1]()
            for transition in transitions:
                print('(' + transition[0][0] + ", " + transition[0][1] + ") -> " + transition[1])
        else:
            value = options[choice - 1]()
            print(value)


if __name__ == '__main__':
    finite_automata = FiniteAutomata('fa.in')
    run_menu(finite_automata)
