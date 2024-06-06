from ParsingTable import create_parsing_table, print_parsing_table
from Tokenizer import get_tokens
from anytree import Node, RenderTree


def predictive_parsing(parsing_table: dict, start_symbol: str):
    stack = ['$', start_symbol]
    root = Node(start_symbol)
    current_node = root

    token_generator = get_tokens()
    current_token = next(token_generator)

    while stack:
        if current_token != "$":
            while current_token.name == "T_Whitespace".lower():
                current_token = next(token_generator)
                if current_token == "$":
                    break

        print("-----------")       
        print(f"Stack: {stack}")
        print(f"Current Token: {current_token}")

        top = stack[-1]
        if current_token == "$" and top == "$":
            break
        elif current_token == "$":
            current_token_name = "$"
            current_token_value = "$"
            current_token_line = "End of Tokens"
        else:
            current_token_name = current_token.name
            current_token_value = current_token.value
            current_token_line = current_token.line_num

  
        if top == current_token_name:
            print(f"Matched Token: {current_token_name}, Value: {current_token_value}")
            # current_node = current_node.parent
            stack.pop()
            current_token = next(token_generator)
        elif top.isupper():
            if top in parsing_table.keys() and current_token_name in parsing_table[top].keys():
                production = parsing_table[top][current_token_name]

                print(f"Action: {top} -> {production}")

                current_node = Node(current_token, parent=current_node)
                
                if production == "synch":
                    print(f"Syntax Error at line #{current_token_line}, Illegal {current_token_name}")
                    stack.pop()
                    continue
                elif production != ['ε']:
                    stack.pop()
                    for symbol in reversed(production):
                        stack.append(symbol)
                        Node(symbol, parent=current_node)
                    current_node = current_node.parent
                else:
                    stack.pop()
            else:
                print(f"Syntax Error at line #{current_token_line}, Extra token: {current_token_name}")
                print(f"M[A, a] is empty, Discarding Token...")
                current_token = next(token_generator)

        else:
            stack.pop()
            print(f"Syntax Error at line #{current_token_line}, Missing: {current_token_name}")
            print(f"X is not Terminal")

    return root


def print_parse_tree(root: Node):
    for pre, fill, node in RenderTree(root):
        print(f"{pre}{node.name}")


if __name__ == "__main__":
    grammar = {
        "E": [["T", "E'"]],
        "E'": [["t_aop_pl", "T", "E'"], ["ε"]],
        "T": [["F", "T'"]],
        "T'": [["t_aop_ml", "F", "T'"], ["ε"]],
        "F": [["t_lp", "E", "t_rp"], ["t_id"]],
    }

    parsing_table = create_parsing_table(grammar, start_symbol="E")
    # print_parsing_table(parsing_table)
    parse_tree_root = predictive_parsing(parsing_table, start_symbol="E")
    print_parse_tree(parse_tree_root)
