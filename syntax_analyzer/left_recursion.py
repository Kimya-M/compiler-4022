input_grammar = {
    "S": [["A", "a"], ["b"]],
    "A": [["A", "c"], ["S", "d"]]
}

def remove_immediate_left_recursion(lhs, rhs):
    meo1 = []
    meo2 = []
    for item in rhs:
        # print(item)
        # print(lhs)

        if item[0] == lhs:
            item.pop(0)
            item.append(lhs + "'")
            # print(item)
            meo1 = item
            meo1.append(["ε"])
            # print(meo1)
        else:
            item.append(lhs + "'")
            meo2 = item
            
    return {lhs: [meo2],
            lhs + "'": [meo1]}
        

def remove_left_recursion(grammar: dict):
    non_terminals = list(grammar.keys()) # grammars

    for i in range(len(non_terminals)):
        for j in range(i):
            for item in grammar[non_terminals[i]]:
                if item[0] == non_terminals[j]:
                    temp = grammar[non_terminals[j]]
                    temp.append(grammar[non_terminals[i]][1:])
                    grammar[non_terminals[i]] = temp
        # print(grammar)
        # del grammar[non_terminals[i]]
        # print(grammar)
        print(non_terminals[i])
        print(grammar[non_terminals[i]])
        print(remove_immediate_left_recursion(non_terminals[i], grammar[non_terminals[i]]))
        grammar = grammar | (remove_immediate_left_recursion(non_terminals[i], grammar[non_terminals[i]]))
    
    return grammar

print(remove_immediate_left_recursion("E", [["E", "+", "T"], ["T"]]))
#{"A": [["A", "+", "T"], ["T"]]}
print(remove_left_recursion(input_grammar))
