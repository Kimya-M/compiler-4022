token_map = {
    "bool": "T_Bool",
    "break": "T_Break",
    "char": "T_Char_keyword",
    "continue": "T_Continue",
    "else": "T_Else",
    "false": "T_False",
    "for": "T_For",
    "if": "T_If",
    "int": "T_Int",
    "print": "T_Print",
    "return": "T_Return",
    "true": "T_True",
    "+": "T_AOP_PL",  # Addition operator
    "-": "T_AOP_MN",  # Subtraction operator
    "*": "T_AOP_ML",  # Multiplication operator
    "/": "T_AOP_DV",  # Division operator
    "%": "T_AOP_RM",  # Modulo operator
    "<": "T_ROP_L",   # Less than operator
    "<=": "T_ROP_LE",  # Less than or equal operator
    ">": "T_ROP_GE",  # Greater than operator
    ">=": "T_ROP_E",  # Greater than or equal operator
    "!=": "T_ROP_NE",  # Not equal operator
    "==": "T_ROP_E",   # Equal operator
    "&&": "T_LOP_AND", # Logical AND operator
    "||": "T_LOP_OR",  # Logical OR operator
    "!": "T_LOP_NOT", # Logical NOT operator
    "=": "T_Assign",  # Assignment operator
    "(": "T_LP",      # Left parenthesis
    ")": "T_RP",      # Right parenthesis
    "{": "T_LC",      # Left curly brace
    "}": "T_RC",      # Right curly brace
    "[": "T_LB",      # Left square bracket
    "]": "T_RB",      # Right square bracket
    ";": "T_Semicolon", # Semicolon
    ",": "T_Comma",    # Comma
}

def get_token_until_delspop(token: str) -> str:
    #print(token)
    index = 0
    for i in range(len(token)):
        if is_whitespace(token[i]) or is_delimiter(token[i])[0] or is_a_operator(token[i]):
            #print(is_whitespace(token[i]),is_delimiter(token[i])[0],is_operator(token[i])[0])
            index = i
            #print(token[:index],"hey")
            break
    return token[0:index]


def is_a_operator(token:str):
    if token[0] == '=' or token[0] == '+' or token[0] == '-' or token[0] == '*' or token[0] == '/' or token[0] == '%' or token[0] == '!' or token[0] == '<' or token[0] == '>':
        return True
    return False 

def get_token_name(token: str):
    token_name = ""
    if token in token_map.keys():
        token_name = token_map[token]
    return token_name

def is_hex(s: str):
    if s.startswith("0X") or s.startswith("0x"):
        try:
            int(s[2:], 16)
            return True
        except ValueError:
            return False
    else:
        return False

#removinf spaces and comments
def is_comment(token: str):
    state = 0
    for char in token:
        if state == 0:
            if char == "/":
                state = 1
        elif state == 1:
            if char == "/":
                state = 2
        elif state == 2:
            return True
    return False
        
    
def is_identifier(token: str):
    """Checks if a token is a combination of letters, digits, or underscore."""
    golabi = get_token_until_delspop(token)
    #print(golabi, "here", len(golabi))
    if len(golabi) == 0:
        return False, None
    if golabi[0] == '_' or golabi[0].isalpha():
        for i in range(len(golabi)):
            if golabi[i] =='_' or golabi[i].isalnum():
                continue
            else:
                return False, None
        
        return True, golabi
    return False, None
   

def is_operator(token: str):
    """Checks if a character is one of the defined operators."""

    if token[0] == '=':
        if token[1] == '=':
            return True, "=="
        return True, "="
    elif token[0] == '<':
        if token[1] == '=':
            return True, "<="
        return True, "<"
    elif token[0] == '>':
        if token[1] == '=':
            return True, ">="
        return True, ">"
    elif token[0] == '!':
        if token[1] == '=':
            return True, "!="
        return True, "!"
    elif token[0] == '+':
        return True, "+"
    elif token[0] == '-':
        return True, "-"
    elif token[0] == '*':
        return True, "*"
    elif token[0] == '/':
        return True, "/"
    elif token[0] == '%':
        return True, "%"
    elif token[0:1] == "&&":
        return True, "&&"
    elif ord(token[0]) == 124 and ord(token[1]) == 124:
        return True, "||"
    return False, None


def is_delimiter(token: str):
    token_name = get_token_name(token)
    
    if token == '[' or token == ']' or token == '(' or token == ')' or token == '{' or token == '}' or token == ';' or token == ',':
        return True, token_name
    else:
        return False, None

def is_litnum(token: str):
    if token[0].isnumeric() or token[0] == '-':
        golabi = get_token_until_delspop(token)

        if is_hex(golabi):
            return True, "T_HexaDecimal", golabi
        elif golabi[0] == '-' and golabi[1:].isnumeric():
            return True, "T_Decimal", golabi
        elif golabi.isnumeric():
            return True, "T_Decimal", golabi
    else:
        return False, None, None

def is_litstring(token: str):
    if token[0] == "'":
        if token[1] == "\\" and token[3] == "'":
            if token[2] == "'":
                return True, "T_Char", token[:4]
            elif token[2] == "\\":
                return True, "T_Char", token[:4]
        elif token[2] == "'":
            return True, "T_Char", token[:3]

    elif token[0] == '"':
        index = 0
        for i in range(1, len(token)):
            if token[i] == '"':
                if token[i - 1] == '\\':
                    continue
                index = i
                break
        golabi = token[:index + 1]

        return True, "T_String", golabi


    else: 
        return False, None, None


def is_keyword(token: str):
    golabi = get_token_until_delspop(token)
    
    if golabi == "bool":
        return True, "Bool"
    elif golabi == "break":
        return True, "Break"
    elif golabi == "char":
        return True, "Char"
    elif golabi == "continue":
        return True, "Continue"
    elif golabi == "else":
        return True, "Else"
    elif golabi == "false":
        return True, "False"
    elif golabi == "for":
        return True, "For"
    elif golabi == "if":
        return True, "If"
    elif golabi == "int":
        return True, "Int"
    elif golabi == "print":
        return True, "Print"
    elif golabi == "return":
        return True, "Return"
    elif golabi == "true":
        return True, "True"
    else:
        return False, None

def is_whitespace(token: str):
        if ord(token) == 32 or ord(token) == 10 or ord(token) == 9:
            return True
        else:
            return False

def read_file_line(file_name: str):
    with open(file_name, "r") as file:
        for line in file:
            yield line


# This is just a placeholder for actual token objects (you can define a Token class later)
class Token:
    def __init__(self, name, line_num, value):
        self.name = name
        self.line_num = line_num
        self.value = value
    
    def __str__(self) -> str:
        return f"<{self.name}, {self.line_num}, {repr(self.value)}>"
    
    def __repr__(self) -> str:
        return str(self)

# This function can be used later to identify tokens from the input stream
def get_next_token(text):
    # Implement logic to identify the next token based on character sequences
    # and return a Token object with its type and value
    pass


def get_tokens():
    tokens = []
    count = 0
    for line in read_file_line("tests/test5.txt"):
        count += 1
        beg = 0
        while(beg < len(line)):
            if is_comment(line[beg:]):
                yield Token("T_Comment", count, line[beg + 2:])
                
                beg = len(line)
            elif is_whitespace(line[beg:beg + 1]):
                yield Token("T_Whitespace", count, line[beg:beg + 1])
                
            elif is_delimiter(line[beg:beg + 1])[0]:
                yield Token(is_delimiter(line[beg:beg + 1])[1], count, line[beg:beg + 1])
                
            elif is_keyword(line[beg:])[0]:
                yield Token("T_" + is_keyword(line[beg:])[1], count, None)
                
                beg += len(is_keyword(line[beg:])[1]) - 1
            elif is_identifier(line[beg:])[0]:
                yield Token("T_ID", count, is_identifier(line[beg:])[1])

                beg += len(is_identifier(line[beg:])[1]) - 1
            elif is_operator(line[beg:])[0]:
                operator = is_operator(line[beg:])[1]
                token_name = get_token_name(operator)
                
                yield Token(token_name, count, operator)

                beg += len(operator) - 1

            elif is_litnum(line[beg:])[0]:
                _ , token_name, number= is_litnum(line[beg:])
                yield Token(token_name, count, number)

                beg += len(number) - 1
            elif is_litstring(line[beg:])[0]:
                _ , token_name, word = is_litstring(line[beg:])
                yield Token(token_name, count, word)
                beg += len(word) - 1
            beg += 1
    return tokens


if __name__ == "__main__":
    gen = get_tokens()

    for token in gen:
        print(token)
