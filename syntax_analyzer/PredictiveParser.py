from Tokenizer import get_tokens
from anytree import Node, RenderTree


def predictive_parser(parsing_table: dict[str, dict], start_symbol: str) -> Node:
    stack = ['$', start_symbol]
    root = Node(start_symbol)
    parent_stack = [root]
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
        if stack != ["$"]:
            current_node = parent_stack.pop()

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
            stack.pop()
            current_token = next(token_generator)
            Node(current_token_value, parent=current_node)

            print(f"Matched Token: {current_token_name}, Value: {current_token_value}")
        elif top.isupper():
            if top in parsing_table.keys() and current_token_name in parsing_table[top].keys():
                production = parsing_table[top][current_token_name]

                print(f"Action: {top} -> {production}")

                if production == "synch":
                    print(f"Syntax Error at line #{current_token_line}, Illegal {current_token_name}")
                    stack.pop()
                elif production != ['ε']:
                    stack.pop()
                    for symbol in reversed(production):
                        stack.append(symbol)

                        child_node = Node(symbol.upper(), parent=current_node)
                        parent_stack.append(child_node)
                else:
                    child_node = Node("ε", parent=current_node)
                    stack.pop()
            else:
                print(f"Syntax Error at line #{current_token_line}, Extra token: {current_token_name}")
                print("M[A, a] is empty, Discarding Token...")
                current_token = next(token_generator)

        else:
            stack.pop()
            print(f"Syntax Error at line #{current_token_line}, Missing: {current_token_name}")
            print("X is not Terminal")

    return root


def print_parse_tree(root: Node):
    for pre, fill, node in RenderTree(root):
        print(f"{pre}{node.name}")


if __name__ == "__main__":
    from ParsingTable import create_parsing_table

    grammar = {
        "E": [["T", "E'"]],
        "E'": [["t_aop_pl", "T", "E'"], ["ε"]],
        "T": [["F", "T'"]],
        "T'": [["t_aop_ml", "F", "T'"], ["ε"]],
        "F": [["t_lp", "E", "t_rp"], ["t_id"]],
    }

    parsing_table = create_parsing_table(grammar, start_symbol="E")
    # print_parsing_table(parsing_table)
    parse_tree_root = predictive_parser(parsing_table, start_symbol="E")
    print_parse_tree(parse_tree_root)
