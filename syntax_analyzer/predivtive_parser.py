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
        print("-----------")

        if current_token != "$":
            while current_token.name == "T_Whitespace".lower():
                current_token = next(token_generator)
                if current_token == "$":
                    break
        
        print(f"Stack: {stack}")
        print(f"Current Token: {current_token}")

        top = stack.pop()
        if current_token == "$" and top == "$":
            break
        elif current_token == "$" and top.isupper():
            if top in parsing_table.keys() and "$" in parsing_table[top].keys():
                production = parsing_table[top]["$"]

                print(f"Action: {top} -> {production}")

                current_node = Node(current_token, parent=current_node)
                if production != ['ε']:
                    for symbol in reversed(production):
                        stack.append(symbol)
                        current_node = Node(symbol, parent=current_node)
                    current_node = current_node.parent
            continue
        elif current_token == "$" and not top.isupper():
            raise SyntaxError(f"Unmatched grammar: {current_token.name}")

  
        if top == current_token.name:
            current_node = current_node.parent
            current_token = next(token_generator)
        elif top.isupper():
            if top in parsing_table.keys() and current_token.name in parsing_table[top].keys():
                production = parsing_table[top][current_token.name]

                print(f"Action: {top} -> {production}")

                current_node = Node(current_token, parent=current_node)
                if production != ['ε']:
                    for symbol in reversed(production):
                        stack.append(symbol)
                        current_node = Node(symbol, parent=current_node)
                    current_node = current_node.parent
            else:
                raise SyntaxError(f"Unexpected token: {current_token.name}")
        else:
            raise SyntaxError(f"X is not Terminal, token: {current_token.name}")

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
        "F": [["(", "E", ")"], ["t_id"]],
    }

    parsing_table = create_parsing_table(grammar, start_symbol="E")
    parse_tree_root = predictive_parsing(parsing_table, start_symbol="E")
    print_parse_tree(parse_tree_root)
