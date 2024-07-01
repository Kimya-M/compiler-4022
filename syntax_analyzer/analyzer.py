from PredictiveParser import predictive_parser
from anytree import Node, PreOrderIter

class SymbolTable:
    def __init__(self):
        self.table = {}
        self.scope_level = 0

    def enter_scope(self):
        self.scope_level += 1

    def exit_scope(self):
        # Remove all entries that have the current scope level
        self.table = {k: v for k, v in self.table.items() if v[3] < self.scope_level}
        self.scope_level -= 1

    def add(self, name, category, type, attributes=None):
        entry = [name, category, type, self.scope_level, attributes]
        self.table[name] = entry

    def lookup(self, name):
        return self.table.get(name, None)


def semantic_analyzer(root: Node):
    symbol_table = SymbolTable()
    # Using PostOrderIter for post-order DFS
    order = []
    
    for node in PreOrderIter(root):
        order.append(node.name)
        line.append(node.line)
        print(node.name)
    #add decelerations to symbol table
    for i in range(len(order)):
        if order[i] == "COMPOUNDSTMT":
            print(symbol_table.table)
            symbol_table.enter_scope()
        if order[i] == "}":
            print(symbol_table.table)
            symbol_table.exit_scope()
    
        if(order[i] == "T_ID"):
            if order[i + 1] in symbol_table.table.keys():
                print(f"{order[i + 1]} already defined!")

            else:
                if(order[i + 3] == "FUNCDEC"):
                    symbol_table.add(order[i + 1],"Function",order[i - 1], None)
                if(order[i - 2] == "VARDECSTMT"):
                    symbol_table.add(order[i + 1],"Variable",order[i - 1], None)
                if(order[i + 3] == "VARDEC"):
                    symbol_table.add(order[i + 1],"Variable",order[i - 1], None)
                if(order[i - 1] == "," and order[i + 2] == "VARDECINIT"):
                    j = i
                    while(order[j]!= "VARDECSTMT"):
                        j -= 1    
                    symbol_table.add(order[i + 1],"Variable",order[j + 1], None)
                else:
                    if order[i + 1] not in symbol_table.table.keys():
                        print(f"{order[i + 1]} variable or function not defined!")
    return symbol_table.table

                



def reverse_children(root):
    if root.children:
        # Reverse the order of children
        root.children = tuple(reversed(root.children))
        # Recursively reverse the children of each child
        for child in root.children:
            reverse_children(child)

if __name__ == "__main__":
    pass