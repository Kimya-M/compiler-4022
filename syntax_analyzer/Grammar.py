START_SYMBOL = "PROGRAM"

GRAMMAR = {
    "PROGRAM": [["DECLIST"]],

    "DECLIST": [["DEC", "DECLIST'"]],
    "DECLIST'": [["DEC", "DECLIST'"], ["ε"]],

    "DEC": [["TYPE", "t_id", "DECLARATION"]],
    "DECLARATION": [["VARDEC"], ["FUNCDEC"]],

    "TYPE": [["t_int"], ["t_bool"], ["t_char"]],

    "VARDEC": [["VARDECLIST", "t_semicolon"]],
    "VARDECLIST": [["VARDECINIT", "VARDECLIST'"]],
    "VARDECLIST'": [["t_comma", "t_id", "VARDECINIT", "VARDECLIST'"], ["ε"]],

    "VARDECINIT": [["ARRAY", "VARDECINIT'"]],
    "VARDECINIT'": [["t_assign", "EXPRESSION"], ["ε"]],

    "ARRAY": [["t_lb", "ARRAYSIZE", "t_rb"], ["ε"]],
    "ARRAYSIZE": [["EXPRESSION"], ["ε"]],

    "FUNCDEC": [["t_lp", "PARAMETERS", "t_rp", "STATEMENT"]],
    "PARAMETERS": [["PARAMETERLIST"], ["ε"]],
    "PARAMETERLIST": [["TYPE", "t_id", "PARAMETERLIST'"]],
    "PARAMETERLIST'": [["t_comma", "TYPE", "t_id", "ARRAY", "PARAMETERLIST'"], ["ε"]],

    "STATEMENT": [["COMPOUNDSTMT", "STATEMENT"], ["SIMPLESTMT", "STATEMENT"], ["IFSTMT", "STATEMENT"], ["LOOPSTMT", "STATEMENT"], ["PRINTSTMT", "STATEMENT"], ["BREAKSTMT", "STATEMENT"], ["RETURNSTMT", "STATEMENT"], ["CONTINUESTMT", "STATEMENT"], ["VARDECSTMT", "STATEMENT"], ["ε"]],

    "COMPOUNDSTMT": [["t_lc", "statement", "t_rc"]],

    "IFSTMT": [["t_if", "EXPRESSION", "COMPOUNDSTMT", "ELSESTMT"]],
    "ELSESTMT": [["t_else", "COMPOUNDSTMT"], ["ε"]],

    "LOOPSTMT": [["t_for", "t_lp", "FORSTMT", "t_rp"]],
    "FORSTMT": [["LOOPVARDEC", "t_semicolon", "LOOPEXPR", "t_semicolon", "LOOPSTEP"]],

    "LOOPVARDEC": [["TYPE", "t_id", "t_assign", "t_decimal"], ["t_id", "t_assign", "t_decimal"], ["ε"]],
    "LOOPEXPR": [["EXPRESSION"], ["ε"]],
    "LOOPSTEP": [["EXPRESSION"], ["ε"]],

    "SIMPLESTMT": [["t_id", "ARRAY2", "t_assign", "EXPRESSION", "t_semicolon"]],
    "ARRAY2": [["t_lb", "ARRAYSIZE2", "t_rb"], ["ε"]],
    "ARRAYSIZE2": [["EXPRESSION"]],

    "VARDECSTMT": [["TYPE", "t_id", "VARDECLIST", "t_semicolon"]],

    "RETURNSTMT": [["t_return", "t_semicolon"], ["t_return", "EXPRESSION", "t_semicolon"]],

    "BREAKSTMT": [["t_break", "t_semicolon"]],

    "CONTINUESTMT": [["t_continue", "t_semicolon"]],

    "PRINTSTMT": [["t_print", "t_lp", "PRINTRULES", "t_rp", "t_semicolon"]],
    "PRINTRULES": [["EXPRESSION", "PRINTLIST"]],
    "PRINTLIST": [["t_comma", "EXPRESSION", "PRINTLIST"], ["ε"]],

    "EXPRESSION": [["OREXP"]],

    "OREXP": [["ANDEXP", "OR"]],
    "OR": [["t_lop_or", "ANDEXP", "OR"], ["ε"]],

    "ANDEXP": [["NOTEXP", "AND"]],
    "AND": [["t_lop_and", "NOTEXP", "AND"], ["ε"]],

    "NOTEXP": [["COMPEXP", "NOT"]],
    "NOT": [["t_lop_not", "COMPEXP", "NOT"], ["ε"]],

    "COMPEXP": [["EXPR", "COMP"]],
    "COMP": [["COMP_OP", "EXPR", "COMP"], ["ε"]],

    "COMP_OP": [["t_rop_l"], ["t_rop_g"], ["t_rop_le"], ["t_rop_ge"], ["t_rop_ne"], ["t_rop_e"]],

    "EXPR": [["TERM", "ARTH1"]],
    "ARTH1": [["t_aop_pl", "TERM", "ARTH1"], ["t_aop_mn", "TERM", "ARTH1"], ["ε"]],

    "TERM": [["FACTOR", "ARTH2"]],
    "ARTH2": [["t_aop_ml", "FACTOR", "ARTH2"], ["t_aop_dv", "FACTOR", "ARTH2"], ["t_aop_rm", "FACTOR", "ARTH2"], ["ε"]],

    "FACTOR": [["t_aop_pl", "ATOM"], ["t_aop_mn", "ATOM"], ["ATOM"]],

    "ATOM": [["t_id"], ["t_decimal"], ["t_hexadecimal"], ["t_string"], ["t_character"], ["t_true"], ["t_false"]]
}
