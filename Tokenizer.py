# Define token types (replace with your actual keywords if needed)"
KEYWORDS = {"bool", "break", "char", "continue", "else", "false", "for", "if", "int", "print", "return", "true"}

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
    """Checks if a character is one of the defined delimiters."""
    pass
  
def is_boolean_operator(token: str):
    pass
    

def is_litnum(token: str):
    pass


def is_litstring(token: str):
    pass

def is_keyword(token: str):
    pass

def is_whitespace(token: str):
    pass

def read_file_line(file_name: str):
    with open(file_name, "r") as file:
        for line in file:
            yield line.strip()


# This is just a placeholder for actual token objects (you can define a Token class later)
class Token:
    def __init__(self, name, line_num, value):
        self.name = name
        self.line_num = line_num
        self.value = value
    
    def __str__(self) -> str:
        return f"<{self.name}, {self.line_num}, \"{self.value}\">"
    
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
    for line in read_file_line("tokens.txt"):
        count += 1
        for beg in range(0, len(line)):
            for end in range(1, len(line) + 1):
                if is_comment(line[beg:end]):
                    comment_flag = True
                    token = Token("T_Comment", count, line[beg + 2:])
                    tokens.append(token)
                    break
                elif is_identifier(line[beg:end]):
                    break
                elif is_keyword(line[beg:end]):
                    break
                elif is_operator(line[beg:end]):
                    break
                elif is_boolean_operator(line[beg:end]):
                    break
                elif is_litnum(line[beg:end]):
                    break
                elif is_litstring(line[beg:end]):
                    break
                elif is_delimiter(line[beg:end]):
                    break
                elif is_whitespace(line[beg:end]):
                    break
            if comment_flag:
                break
    return tokens
                

if __name__ == "__main__":
    print(get_tokens())