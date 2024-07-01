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
    line = []
    
    for node in PreOrderIter(root):
        order.append(node.name[0])
        line.append(node.name[1])
        print(node.name[0])
    #add decelerations to symbol table
    for i in range(len(order)):
        if order[i] == "COMPOUNDSTMT":
            #print(symbol_table.table)
            symbol_table.enter_scope()
        if order[i] == "}":
            #print(symbol_table.table)
            symbol_table.exit_scope()
    
        if(order[i] == "T_ID"):
            if(order[i + 3] == "FUNCDEC"):
                if order[i + 1] in symbol_table.table.keys():
                    print(f"{order[i + 1]} already defined at line {line[i + 1]}!")
                    continue
                j = i + 4
                symbol_table.add(order[i + 1],"Function",order[i - 1], None)
                param = []
                while order[j] != ")":
                    j += 1
                    if order[j] == "T_ID": 
                        symbol_table.add(order[j + 1],"Variable",order[j - 1], None)
                        param.append((order[j + 1], order[j - 1]))        
                symbol_table.add(order[i + 1],"Function",order[i - 1], param)
                
            if(order[i - 2] == "VARDECSTMT"):
                if order[i + 1] in symbol_table.table.keys():
                    print(f"{order[i + 1]} already defined at line {line[i + 1]}!")
                    continue
                symbol_table.add(order[i + 1],"Variable",order[i - 1], None)
            if(order[i + 3] == "VARDEC"):
                if order[i + 1] in symbol_table.table.keys():
                    print(f"{order[i + 1]} already defined at line {line[i + 1]}!")
                    continue
                symbol_table.add(order[i + 1],"Variable",order[i - 1], None)
            if(order[i - 1] == "," and order[i + 2] == "VARDECINIT"):
                if order[i + 1] in symbol_table.table.keys():
                    print(f"{order[i + 1]} already defined at line {line[i + 1]}!")
                    continue
                j = i
                while(order[j]!= "VARDECSTMT"):
                    j -= 1    
                symbol_table.add(order[i + 1],"Variable",order[j + 1], None)
            else:
                if order[i + 1] not in symbol_table.table.keys():
                    print(f"{order[i + 1]} variable or function not defined at line {line[i + 1]}!")
                    
        if order[i] == "T_ASSIGN":
            j = i
            while (order[j] != "T_ID"):
                j -= 1
            if order[j + 1] in symbol_table.table.keys():
                type_expected = symbol_table.table[order[j + 1]][2]
                value = expression_evaluation(order[i:],symbol_table.table, line[i:])
                if value != type_expected:
                    print(f"types mismatch at line {line[i + 1]}")
            else:
                print(f"{order[j + 1]} not defined")
        if order[i] == "T_IF":
            value = expression_evaluation(order[i:],symbol_table.table, line[i:])
            if value != "T_BOOL":
                print(f"in if statements you can only use boolean as condition. line {line[i + 1]}")
        if order[i] == "ARRAY":
            dec = 0
            idt = 0
            if order[i + 1] == "T_LB":
                j = i
                while order[j] != "T_RB":
                    if order[j] == "T_DECIMAL":
                        if order[j - 2] == "-":
                            dec = 1
                    if order[j] == "T_ID":
                        idt += 1
                    j += 1
                value = expression_evaluation(order[i:], symbol_table.table, line[i:])
                if value != "T_INT":
                    print(f"array size value must be an integer. correct line {line[i + 1]}")
                
            if idt == 0 and dec == 1:
                print(f"array index/size can't be negetive. line {line[i + 1]}")
        if order[i] == "T_RETURN":
            value = expression_evaluation(order[i:], symbol_table.table, line[i:])
            j = i
            while order[j] != "FUNCDEC":
                j -= 1
            function_name = order[j - 2]
            if value != symbol_table.table[function_name][2]:
                print(f"function type isn't defined correctly. line {line[i + 1]}")
                
        if order[i] == "ISFUNCTION":
            pass
    return symbol_table.table           

def expression_evaluation(order: list, table: dict, line: list):
        j = 0
        actual_type = ""
        types = []
        aop_operators = []
        rop_operators = []
        lop_operators = []
        while order[j] != "T_SEMICOLON":
            if order[j] == "T_RP":
                if order[j + 1] == "COMPOUNDSTMT":
                    break
            j += 1
            if order[j] == "T_AOP_PL" or order[j] == "T_AOP_MN" or order[j] == "T_AOP_ML" or order[j] == "T_AOP_DV" or order[j] == "T_AOP_RM":
                aop_operators.append(order[j])
            elif order[j] == "T_ROP_L" or order[j] =="T_ROP_G" or order[j] == "T_ROP_LE" or order[j] == "T_ROP_GE" or order[j] == "T_ROP_NE" or order[j] == "T_ROP_E":
                rop_operators.append(order[j])
            elif order[j] == "T_LOP_AND" or order[j] == "T_LOP_OR" or order[j] == "T_LOP_NOT":
                lop_operators.append(order[j])
            elif order[j] == "T_ID":
                if order[j + 1] in table.keys():
                    types.append(table[order[j + 1]][2])
                else:
                    print(f"{order[j + 1]}not defined at line {line[j + 1]}")
                    return "wrong"
            elif order[j] == "T_DECIMAL":
                types.append("T_INT")
            elif order[j] == "T_CHAR":
                types.append("T_CHAR")
            elif order[j] == "T_TRUE" or order[j] == "T_FALSE":
                types.append("T_BOOL")

        if len(aop_operators) == 0  and len(rop_operators) == 0 and len(lop_operators) != 0:
            for typ in types:
                if typ != "T_BOOL":
                    return "wrong"
            actual_type = "T_BOOL"
        if len(aop_operators) != 0  and len(rop_operators) == 0 and len(lop_operators) == 0:
            for typ in types:
                if typ != "T_INT":
                    return "wrong"
            actual_type = "T_INT"
        if len(aop_operators) == 0  and len(rop_operators) != 0 and len(lop_operators) == 0:
            for typ in types:
                if typ != "T_BOOL":
                    return "wrong"
            actual_type = "T_BOOL"
        if len(aop_operators) == 0  and len(rop_operators) == 0 and len(lop_operators) == 0:
            actual_type = types[0]
            
        return actual_type


def reverse_children(root):
    if root.children:
        # Reverse the order of children
        root.children = tuple(reversed(root.children))
        # Recursively reverse the children of each child
        for child in root.children:
            reverse_children(child)


if __name__ == "__main__":
    pass
