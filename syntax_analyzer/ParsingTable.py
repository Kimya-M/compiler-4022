from Fcal import compute_first, compute_follow


def create_parsing_table(grammar: dict, start_symbol="S"):
    # Initialize the parsing table
    parsing_table = {nonterminal: {} for nonterminal in grammar}

    # Populate the parsing table
    for nonterminal, productions in grammar.items():
        for production in productions:
            first_set = compute_first_set(production, compute_first(grammar))
            all_follow_set = compute_follow(grammar, start_symbol)

            for first_terminal in first_set:
                if first_terminal != 'ε':
                    parsing_table[nonterminal][first_terminal] = production
                else:
                    for terminal in all_follow_set[nonterminal]:
                        parsing_table[nonterminal][terminal] = production
                        if '$' in all_follow_set[nonterminal]:
                            parsing_table[nonterminal]['$'] = production

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
    print("Parsing Table:")
    for nonterminal, rules in parsing_table.items():
        for terminal, production in rules.items():
            print(f"M[{nonterminal}, {terminal}] = {production}")


if __name__ == "__main__":
    # grammar = {
    #     "E": [["E", "+", "T"], ["T"]],
    #     "E": [["T", "*", "F"], ["F"]],
    #     "F": [["(", "E", ")"], ["id"]],
    # }
    
    grammar = {
        "E": [["T", "E'"]],
        "E'": [["+", "T", "E'"], ["ε"]],
        "T": [["F", "T'"]],
        "T'": [["*", "F", "T'"], ["ε"]],
        "F": [["(", "E", ")"], ["id"]],
    }
    
    parsing_table = create_parsing_table(grammar, start_symbol="E")
    print_parsing_table(parsing_table)
