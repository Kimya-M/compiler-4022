START_SYMBOL = "Program"

GRAMMAR = {
    "Program": [["Declist"]],

    "Declist": [["Dec", "Declist'"]],
    "Declist'": [["Dec", "Declist'"], ["ε"]],

    "Dec": [["Type", "t_id", "Declaration"]],
    "Declaration": [["Vardec"], ["Funcdec"]],

    "Type": [["t_int"], ["t_bool"], ["t_char"]],

    "Vardec": [["Vardeclist", "t_semicolon"]],
    "Vardeclist": [["VardecInit", "Vardeclist'"]],
    "Vardeclist'": [["t_comma", "t_id", "VardecInit", "Vardeclist'"], ["ε"]],

    "VardecInit": [["Array", "VardecInit'"]],
    "VardecInit'": [["t_assign", "Expression"], ["ε"]],

    "Array": [["t_lb", "Arraysize", "t_rb"], ["ε"]],
    "Arraysize": [["Expression"], ["ε"]],

    "Funcdec": [["t_lp", "Parameters", "t_rp", "Statement"]],
    "Parameters": [["ParameterList"], ["ε"]],
    "ParameterList": [["Type", "t_id", "ParameterList'"]],
    "ParameterList'": [["t_comma", "Type", "t_id", "Array", "ParameterList'"], ["ε"]],

    "Statement": [["CompoundStmt"], ["SimpleStmt"], ["IfStmt"],
                  ["LoopStmt"], ["PrintStmt"], ["BreakStmt"],
                  ["ReturnStmt"], ["ContinueStmt"], ["VardecStmt"]
                ],


    "CompoundStmt": [["t_lc", "StatementList", "t_rc"]],
    "StatementList" :[["Statement","StatementList"],["ε"]],

    "IfStmt": [["t_if", "Expression", "CompoundStmt", "ElseStmt"]],
    "ElseStmt": [["t_else", "CompoundStmt"], ["ε"]],

    "LoopStmt": [["t_for", "t_lp", "ForStmt", "t_rp"]],
    "ForStmt": [["LoopVardec", "t_semicolon", "LoopExpr", "t_semicolon", "LoopStep"]],

    "LoopVardec": [["Type", "t_id", "t_assign", "Expression"], ["t_id", "t_assign", "Expression"], ["ε"]],
    "LoopExpr": [["Expression"], ["ε"]],
    "LoopStep": [["SimpleStmt2"], ["ε"]],

    "SimpleStmt": [["t_id", "Array2", "t_assign", "Expression", "t_semicolon"]],
    "SimpleStmt2": [["t_id", "Array2", "t_assign", "Expression"]],
    "Array2": [["t_lb", "Arraysize2", "t_rb"], ["ε"]],
    "Arraysize2": [["Expression"]],

    "VardecStmt": [["Type", "t_id", "Vardeclist", "t_semicolon"]],

    "ReturnStmt": [["t_return", "t_semicolon"], ["t_return", "Expression", "t_semicolon"]],

    "BreakStmt": [["t_break", "t_semicolon"]],

    "ContinueStmt": [["t_continue", "t_semicolon"]],

    "PrintStmt": [["t_print", "t_lp", "PrintRules", "t_rp", "t_semicolon"]],
    "PrintRules": [["Expression", "PrintList"]],
    "PrintList": [["t_comma", "Expression", "PrintList"], ["ε"]],

    "Expression": [["OrExp"]],

    "OrExp": [["AndExp", "Or"]],
    "Or": [["t_lop_or", "AndExp", "Or"], ["ε"]],

    "AndExp": [["NotExp", "And"]],
    "And": [["t_lop_and", "NotExp", "And"], ["ε"]],

    "NotExp": [["t_lop_not","NotExp"],["CompExp"]],

    "CompExp": [["Expr", "Comp"]],
    "Comp": [["Comp_OP", "Expr", "Comp"], ["ε"]],

    "Comp_OP": [["t_rop_l"], ["t_rop_g"], ["t_rop_le"], ["t_rop_ge"], ["t_rop_ne"], ["t_rop_e"]],

    "Expr": [["Term", "Arth1"]],
    "Arth1": [["t_aop_pl", "Term", "Arth1"], ["t_aop_mn", "Term", "Arth1"], ["ε"]],

    "Term": [["Factor", "Arth2"]],
    "Arth2": [["t_aop_ml", "Factor", "Arth2"], ["t_aop_dv", "Factor", "Arth2"], ["t_aop_rm", "Factor", "Arth2"], ["ε"]],

    "Factor": [["t_aop_pl", "Atom"], ["t_aop_mn", "Atom"], ["Atom"]],

    "Atom": [["t_id", "IsFunction"], ["t_decimal"], ["t_hexadecimal"],
             ["t_string"], ["t_char"], ["t_true"], ["t_false"],
             ["t_lp", "Expression", "t_rp"]],
    
    "IsFunction": [["ε"], ["t_lp", "Parameters2", "t_rp"]],

    "Parameters2" : [["ParameterList2"], ["ε"]],

    "ParameterList2": [["t_id", "ParameterList2'"]],

    "ParameterList2'": [["t_comma", "t_id", "Array", "ParameterList2'"], ["ε"]]
}
