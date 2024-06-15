from Fcal import compute_first, compute_follow
from TerminalColors import bcolors


def create_parsing_table(grammar: dict, start_symbol):
    # Initialize the parsing table
    parsing_table = {nonterminal: {} for nonterminal in grammar}
    all_follow_set = compute_follow(grammar, start_symbol)
    all_first_set = compute_first(grammar)

    for nonterminal, productions in grammar.items():
        for production in productions:
            first_set = compute_first_set(production, all_first_set)

            for first_terminal in first_set:
                if first_terminal != 'ε':
                    if first_terminal not in parsing_table[nonterminal].keys():
                        parsing_table[nonterminal][first_terminal] = []
                    parsing_table[nonterminal][first_terminal].append(production)
                else:
                    for terminal in all_follow_set[nonterminal]:
                        if terminal not in parsing_table[nonterminal].keys():
                            parsing_table[nonterminal][terminal] = []
                        parsing_table[nonterminal][terminal].append(production)
                        if "$" in all_follow_set[nonterminal]:
                            parsing_table[nonterminal]["$"] = []
                            parsing_table[nonterminal]["$"].append(production)

    # Add synchronizing tokens for error handling
    for nonterminal, follow_set in all_follow_set.items():
        for terminal in follow_set:
            if terminal not in parsing_table[nonterminal]:
                parsing_table[nonterminal][terminal] = "synch"

    return parsing_table


def compute_first_set(production, first):
    result = set()
    if not production:  # Empty production
        result.add('ε')
    else:
        for symbol in production:
            if symbol in first:
                result.update(first[symbol])
                if 'ε' not in first[symbol]:
                    break
            else:
                result.add(symbol)
                break
    return result


def print_parsing_table(parsing_table):
    with open("parsing_table.txt", "w") as f:
        print("Parsing Table:")
        for nonterminal, rules in parsing_table.items():
            for terminal, production in rules.items():
                print(f"{bcolors.WARNING}M[{nonterminal}, {terminal}]{bcolors.ENDC} = {bcolors.OKCYAN}{production}{bcolors.ENDC}")
                f.write(f"M[{nonterminal}, {terminal}] = {production}\n")
                if len(production) > 1 and production != "synch":
                    print(f"{bcolors.FAIL}WARNING: The Grammar is Ambiguous!{bcolors.ENDC}")
                    print(f"{bcolors.WARNING}The previous entry in the parsing table has more than one element.{bcolors.ENDC}")
                    f.write(f"WARNING: The Grammar is Ambiguous!\n")
                    f.write(f"The previous entry in the parsing table has more than one element.\n")


def pretty_print_parsing_table(parsing_table):
    print(f"{bcolors.OKBLUE}Parsing Table:{bcolors.ENDC}")
    for nonterminal, rules in parsing_table.items():
        for terminal, production in rules.items():
            print(f"{bcolors.WARNING}M[{nonterminal}, {terminal}]: {bcolors.ENDC}", end="")

            if production != "synch":
                for prod in production:
                    print(f"{bcolors.OKCYAN}{nonterminal} -> {prod}{bcolors.ENDC}", end=" ")
            else:
                print(f"{bcolors.OKCYAN}{production}{bcolors.ENDC}", end=" ")
            print()
            if len(production) > 1 and production != "synch":
                print(f"{bcolors.FAIL}\nWARNING: The Grammar is Ambiguous!{bcolors.ENDC}")
                print(f"{bcolors.WARNING}The previous entry in the parsing table has more than one element.{bcolors.ENDC}")
        print("\n===============================================")


if __name__ == "__main__":
    # grammar = {
    #     "E": [["E", "+", "T"], ["T"]],
    #     "T": [["T", "*", "F"], ["F"]],
    #     "F": [["(", "E", ")"], ["id"]],
    # }

    # grammar = {
    #     "E": [["T", "E'"]],
    #     "E'": [["+", "T", "E'"], ["ε"]],
    #     "T": [["F", "T'"]],
    #     "T'": [["*", "F", "T'"], ["ε"]],
    #     "F": [["(", "E", ")"], ["id"]],
    # }

    # grammar = {
    #     "A": [["if", "expr", "then", "A"], ["if", "expr", "then", "A", "else", "A"], ["other"]]
    # }

    grammar = {
        "S": [["i", "E", "t", "S", "S'"], ["a"]],
        "S'": [["e", "S"], ["ε"]],
        "E": [["b"]],
    }

    parsing_table = create_parsing_table(grammar, start_symbol="S")
    pretty_print_parsing_table(parsing_table)
