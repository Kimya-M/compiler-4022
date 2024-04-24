token_map = {
    "bool": "T_Bool",
    "break": "T_Break",
    "char": "T_Char",
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

def get_token_until_delsp(token: str) -> str:
    index = 0
    for i in range(len(token)):
        if is_whitespace(token[i]) or is_delimiter(token[i]):
            index = i
            break

    return token[0:index]

def get_token_name(token: str):
    token_name = ""
    if token in token_map.keys():
        token_name = token_map[token]
    return token_name

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
    golabi = get_token_until_delsp(token)

    if golabi[0] =='_' or golabi[0].isalpha():
        for i in range(len(golabi)):
            if golabi[i] =='_' or golabi[i].isalnum():
                continue
            else:
                return False, None
        
        return True, golabi
   

def is_operator(token: str):
    """Checks if a character is one of the defined operators."""

    if token[0] == '=':
        if token[1] == '=':
            return True, get_token_name(token[0:2])
        return True, get_token_name(token[0])
    elif token[0] == '<':
        if token[1] == '=':
            return True, get_token_name(token[0:2])
        return True, get_token_name(token[0])
    elif token[0] == '>':
        if token[1] == '=':
            return True, get_token_name(token[0:2])
        return True, get_token_name(token[0])
    elif token[0] == '!':
        if token[1] == '=':
            return True, get_token_name(token[0:2])
        return True, get_token_name(token[0])
    elif token[0] == '+':
        return True, get_token_name(token[0])
    elif token[0] == '-':
        return True, get_token_name(token[0])
    elif token[0] == '*':
        return True, get_token_name(token[0])
    elif token[0] == '/':
        return True, get_token_name(token[0])
    elif token[0] == '%':
        return True, get_token_name(token[0])
    elif token[0:1] == "&&":
        return True, get_token_name(token[0:1])
    elif token[0:1] == "||":
        return True, get_token_name(token[0:1])


def is_delimiter(token: str):
    token_name = get_token_name(token)
    
    if token == '[' or token == ']' or token == '(' or token == ')' or token == '{' or token == '}' or token == ';' or token == ',':
        return True, token_name
    else:
        return False, None

  
def is_boolean_operator(token: str):
    pass
    

def is_litnum(token: str):
    pass


def is_litstring(token: str):
    pass

def is_keyword(token: str):
    golabi = get_token_until_delsp(token)
    
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
    for line in read_file_line("tests/test3.txt"):
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

                beg += len(is_identifier(line[beg:])[1])
            elif is_operator(line[beg:]):
                pass
            elif is_boolean_operator(line[beg:]):
                break
            elif is_litnum(line[beg:]):
                break
            elif is_litstring(line[beg:]):
                break
            beg += 1
    return tokens


if __name__ == "__main__":
    gen = get_tokens()
    for token in gen:
        print(token)
