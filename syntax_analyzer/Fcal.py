def compute_first(grammar):
    first = {non_terminal: set() for non_terminal in grammar}

    for nonterminal in grammar:
        for production in grammar[nonterminal]:
            for symbol in production:
                if not symbol[0].isupper():
                    first[symbol] = {symbol}

    def first_of(symbol):
        if not symbol[0].isupper():
            return first[symbol]
        if not first[symbol]:
            for production in grammar[symbol]:
                for sym in production:
                    first[symbol] |= first_of(sym) - {'ε'}
                    if 'ε' not in first_of(sym):
                        break

                else:
                    first[symbol] |= {'ε'}
        return first[symbol]

    for non_terminal in grammar:
        first_of(non_terminal)

    return first


def compute_follow(grammar, start_symbol):
    follow = {non_terminal: set() for non_terminal in grammar}
    follow[start_symbol] = {'$'}

    first = compute_first(grammar)

    changed = True
    while changed:
        changed = False
        for non_terminal, productions in grammar.items():
            for production in productions:
                # print("the production:", production)
                for symbol in range(len(production)):
                    if not production[symbol][0].isupper():
                        # print(production[symbol], "this isn't a non terminal")
                        continue
                    before_change = len(follow[production[symbol]])
                    # print(production[symbol],"this is a nonterminal.")
                    if symbol == len(production) - 1:
                        follow[production[symbol]] |= follow[non_terminal]
                        # print("0",production[symbol], production, follow[production[symbol]])
                    else:
                        if 'ε' in first[production[symbol + 1]]:
                            if not production[symbol + 1][0].isupper():
                                follow[production[symbol]] |= production[symbol + 1]
                                # print("1",production[symbol], production, follow[production[symbol]])
                            else:
                                follow[production[symbol]] |= follow[production[symbol + 1]]
                                follow[production[symbol]] |= first[production[symbol + 1]] - {'ε'}
                                # print("2",production[symbol], production, follow[production[symbol]])
                        else:
                            follow[production[symbol]] |= first[production[symbol + 1]]
                            # print("3",production[symbol], production, follow[production[symbol]])

                    if before_change != len(follow[production[symbol]]):
                        changed = True

    return follow


def print_first_sets(grammar: dict):
    first_sets = compute_first(grammar)
    better_first_set = {}

    for non_terminal, productions in first_sets.items():
        if non_terminal[0].isupper():
            print(f"First set {non_terminal} : {productions}")
            better_first_set[non_terminal] = productions


def print_follow_sets(grammar: dict, start_symbol: str):
    follow_sets = compute_follow(grammar, start_symbol)
    # print("Follow sets:", follow_sets)
    for non_terminal, productions in follow_sets.items():
        print(f"Follow set {non_terminal} : {productions}")


if __name__ == "__main__":
    # Example grammar to test
    # grammar = {
    #     "S": ["iEtS", "iEtSeS", "a"],
    #     "E": ["b"]
    # }

    grammar = {
        "S": [["a", "A", "b"], ["b", "B", "a"]],
        "A": [["c", "S"], ["ε"]],
        "B": [["d", "S"], ["ε"]]
    }

    grammar = {
        "S": [["0", "S", "1"], ["0", "1"]],
    }

    grammar = {
        "S": [["+", "S", "S"], ["*", "S", "S"], ["a"]],
    }

    grammar = {
        "S": [["S", "(", "S", ")", "S"], ["a"]],
    }

    start_symbol = "S"

    print_first_sets(grammar)
    print_follow_sets(grammar, start_symbol)
