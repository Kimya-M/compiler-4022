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
        
    
# Regular expressions are not used here, but could be added for more complex patterns
def is_identifier(token: str):
    """Checks if a character is a letter, digit, or underscore."""
    pass

def is_operator(token: str):
    """Checks if a character is one of the defined operators."""
    pass

def is_delimiter(token: str):
    if token in token_map.keys():
        token_name = token_map[token]
    
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
    if token[0] == 'b':
        if token[1:4] == "ool":
            if is_whitespace(token[4]) or is_delimiter(token[4])[0]:
                return True, "Bool"
            else:
                return False, None
        elif token[1: 5] == "reak":
            if is_whitespace(token[5]) or is_delimiter(token[5])[0]:
                return True, "Break"
            else:
                return False, None
    elif token[0] == 'c':
        if token[1:4] == "har":
            if is_whitespace(token[4]) or is_delimiter(token[4])[0]:
                return True, "Char"
            else:
                return False, None
        elif token[1:8] == "ontinue":
            if is_whitespace(token[8]) or is_delimiter(token[8])[0]:
                return True, "Continue"
            else:
                return False, None
    elif token[:4] == "else":
        if is_whitespace(token[4]) or is_delimiter(token[4])[0]:
            return True, "Else"
        else:
                return False, None
    elif token[0] == "f":
        if token[1:5] == "alse":
            if is_whitespace(token[5]) or is_delimiter(token[5])[0]:
                return True, "False"
            else:
                return False, None
        if token[1:3] == "or":
            if is_whitespace(token[3]) or is_delimiter(token[3])[0]:
                return True, "For"
            else:
                return False, None
    elif token[0] == 'i':
        if token[1:2] == "f":
            if is_whitespace(token[2]) or is_delimiter(token[2])[0]:
                return True, "If"
            else:
                return False, None
        if token[1:3] == "nt":
            if is_whitespace(token[3]) or is_delimiter(token[3])[0]:
                return True, "Int"
            else:
                return False, None
    elif token[:5] == "print":
        if is_whitespace(token[5]) or is_delimiter(token[5])[0]:
            return True, "Print"
        else:
            return False, None
    elif token[:6] == "return":
        if is_whitespace(token[6]) or is_delimiter(token[6])[0]:
            return True, "Return"
        else:
            return False, None
    elif token[:4] == "true":
        if is_whitespace(token[4]) or is_delimiter(token[4])[0]:
            return True, "True"
        else:
            return False, None
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
            elif is_identifier(line[beg:]):
                break
            elif is_operator(line[beg:]):
                break
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
