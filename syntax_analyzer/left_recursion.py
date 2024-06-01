
    
def remove_immidiate_left_recursion(nonterminal,productions):
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
    
    has_left_rec = []
    no_left_rec = []
    for production in productions:
        if production[0] == nonterminal:
            has_left_rec.append(production)
        else:
            no_left_rec.append(production)
    
    #print("has left recursion",has_left_rec)
    #print("no left recursion",no_left_rec)
    if has_left_rec:
        new_non_terminal = get_new_non_terminal(nonterminal)
        new_has_left_rec = []
        new_no_left_rec = []
        
        

        if no_left_rec:
            new_no_left_rec = [prod + [new_non_terminal] for prod in no_left_rec]
        
        if has_left_rec:
            new_has_left_rec = [prod[1:] + [new_non_terminal] for prod in has_left_rec]
        
        new_has_left_rec.append("ε")
        
        updated_productions = {
            nonterminal: new_no_left_rec,
            new_non_terminal: new_has_left_rec
        }
    else:
        updated_productions = {}
    
    return updated_productions
    
def remove_left_recursion(grammar):
    non_terminals = list(grammar.keys())
    grammar_copy = {k: v[:] for k, v in grammar.items()}
    for i in range(len(non_terminals)):
        A_i = non_terminals[i]
        for j in range(i):
            A_j = non_terminals[j]
            new_productions = []
            for production in grammar_copy[A_i]:
                if production[0] == A_j:
                    for Aj_production in grammar_copy[A_j]:
                        new_productions.append(Aj_production + production[len(A_j):])
                else:
                    new_productions.append(production)
                
                grammar_copy[A_i] = new_productions
        
        #print("now",A_i)
        immediate_left_recursion_removed = remove_immidiate_left_recursion(A_i, grammar_copy[A_i])
        #print("this:",immediate_left_recursion_removed)
        grammar_copy.update(immediate_left_recursion_removed)
        #print("new grammer", grammar_copy)
    
    return grammar_copy

def print_grammar(grammar):
    print("\nNew set of productions: ")
    for nt, productions in grammar.items():
        for prod in productions:
            print(f"{nt} -> {prod}")
    
grammar = {
    "E": [["E", "+", "T"],["T"]],
    "T": [["T", "*", "F"], ["F"]],
    "F": [["(", "E", ")"], ["id"]]
}

    
new_grammar = remove_left_recursion(grammar)
print_grammar(new_grammar)