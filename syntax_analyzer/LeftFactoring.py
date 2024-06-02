def left_factor(grammar):
    counter = 1
    def get_new_non_terminal(base): #making the name of the new terminal :D 
        nonlocal counter
        if counter == 1:
            new_non_terminal = base + str(counter)
        else:
            base = base[:-1]
            new_non_terminal = base + str(counter)
        counter += 1
        return new_non_terminal

    def factor_once(grammar): 
        new_grammar = {}
        changes_made = False

        for non_terminal, productions in grammar.items():
            grouped = {}
            # Group productions by their first symbol
            for prod in productions:
                first = prod[0]
                if first not in grouped:
                    grouped[first] = []
                grouped[first].append(prod) #all the productions that have the same first letters will be grouped in this list
            
            new_grammar[non_terminal] = []

            for first, group in grouped.items():
                if len(group) > 1:
                    # Need to factor these productions
                    changes_made = True
                    new_non_terminal = get_new_non_terminal(non_terminal)
                    new_grammar[non_terminal].append([first, new_non_terminal]) # changing the rule for the productions that have in common prefix
                    new_grammar[new_non_terminal] = [] #adding the new non-terminal and it's rules 

                    for prod in group:
                        suffix = prod[1:] if len(prod) > 1 else ["ε"] # new non terminal rules calculations 
                        new_grammar[new_non_terminal].append(suffix)
                else:
                    new_grammar[non_terminal].append(group[0]) #adding the rules that don't have anything in common 

        return new_grammar, changes_made

    current_grammar = grammar
    while True:
        current_grammar, changes_made = factor_once(current_grammar)
        if not changes_made:
            break

    return current_grammar

# Example grammar
grammar = {
    "S": ["iEtS", "iEtSeS", "a"],
    "E": ["b"]
}


factored_grammar = left_factor(grammar)
print(factored_grammar)
