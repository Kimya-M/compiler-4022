from ParsingTable import compute_first_set, compute_first, compute_follow


def is_LL1(grammar: dict, start_symbol: str):
    try:
        all_follow_set = compute_follow(grammar, start_symbol)
    except RecursionError as e:
        print(e)
        return False

    for nonterminal, productions in grammar.items():
        for i in range(len(productions)):
            for j in range(i + 1, len(productions)):
                alpha = productions[i]
                beta = productions[j]

                first_alpha = compute_first_set(alpha, compute_first(grammar))
                first_beta = compute_first_set(beta, compute_first(grammar))

                # Check if First(alpha) and First(beta) are not disjoint
                if first_alpha.intersection(first_beta):
                    print("First(alpha) and First(beta) are not disjoint")
                    print(f"alpha: {nonterminal} -> {alpha}, beta: {nonterminal} -> {beta}")
                    print(f"first(alpha): {first_alpha}, first(beta): {first_beta}")
                    # return False

                # Check if epsilon is in First(beta) and First(alpha) intersect Follow(A) is not empty
                if 'ε' in first_beta:
                    if first_alpha.intersection(all_follow_set[nonterminal]):
                        print("First(alpha) intersect Follow(A) is not empty")
                        print(f"alpha: {nonterminal} -> {alpha}, beta: {nonterminal} -> {beta}")
                        print(f"first(alpha): {first_alpha}, follow(A): {all_follow_set[nonterminal]}")
                        # return False

                # Check if epsilon is in First(alpha) and First(beta) intersect Follow(A) is not empty
                if 'ε' in first_alpha:
                    if first_beta.intersection(all_follow_set[nonterminal]):
                        print("First(beta) intersect Follow(A) is not empty")
                        print(f"beta: {nonterminal} -> {beta}")
                        print(f"follow(A): {all_follow_set[nonterminal]}, first(beta): {first_beta}")
                        # return False

    return True


if __name__ == "__main__":
    grammar = {
        "E": [["T", "E'"]],
        "E'": [["+", "T", "E'"], ["ε"]],
        "T": [["F", "T'"]],
        "T'": [["*", "F", "T'"], ["ε"]],
        "F": [["(", "E", ")"], ["id"]],
    }

    # grammar = {
    #     "E": [["E", "+", "T"], ["T"]],
    #     "T": [["T", "*", "F"], ["F"]],
    #     "F": [["(", "E", ")"], ["id"]],
    # }

    # grammar = { # ll1
    # "E": [["T", "E'"]],
    # "E'": [["or", "T", "E'"], ["ε"]],
    # "T": [["F", "T'"]],
    # "T'": [["and", "F", "T'"], ["ε"]],
    # "F": [["not", "F"], ["(", "E", ")"], ["id"]],
    # }

    if is_LL1(grammar, start_symbol="E"):
        print("The grammar is LL(1).")
    else:
        print("The grammar is not LL(1).")
