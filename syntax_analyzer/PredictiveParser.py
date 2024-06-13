from Tokenizer import get_tokens
from TerminalColors import bcolors
from anytree import Node, RenderTree, ContRoundStyle


def predictive_parser(parsing_table: dict[str, dict], start_symbol: str) -> Node:
    stack = ['$', start_symbol]
    root = Node(start_symbol)
    parent_stack = [root]
    token_generator = get_tokens()
    current_token = next(token_generator)
    pop_node_stack = True

    while stack:
        if current_token != "$":
            while current_token.name == "t_whitespace" or current_token.name == "t_comment":
                current_token = next(token_generator)
                if current_token == "$":
                    break

        print(f"{bcolors.BOLD}-----------{bcolors.ENDC}")
        print(f"Stack: {stack}")
        print(f"{bcolors.OKCYAN}Current Token: {current_token}{bcolors.ENDC}")

        # print(f"-----------")
        # print(f"Stack: {stack}")
        # print(f"Current Token: {current_token}")

        top = stack[-1]
        if stack != ["$"] and pop_node_stack:
            current_node = parent_stack.pop()
        else:
            pop_node_stack = True

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
            if current_token_value != None:
                Node(current_token_value, parent=current_node)

            # print(f"{bcolors.OKGREEN}Matched Token: {current_token_name.upper()}, Value: {current_token_value}{bcolors.ENDC}")
            print(f"Matched Token: {current_token_name.upper()}, Value: {current_token_value}")
        elif top[0].isupper():
            if top in parsing_table.keys() and current_token_name in parsing_table[top].keys():
                if parsing_table[top][current_token_name] != "synch":
                    production = parsing_table[top][current_token_name][0]
                else:
                    production = parsing_table[top][current_token_name]

                # print(f"{bcolors.WARNING}Action: {top} -> {production}{bcolors.ENDC}")
                print(f"Action: {top} -> {production}")

                if production == "synch":
                    print(f"{bcolors.OKGREEN}Synched{bcolors.ENDC}")
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
                print(f"{bcolors.FAIL}Syntax Error at line #{current_token_line}, Extra token: {current_token_name}{bcolors.ENDC}")
                print("M[A, a] is empty, Discarding Token...")
                print(f"M[{top}, {current_token_name}]")
                current_token = next(token_generator)
                pop_node_stack = False

        else:
            stack.pop()
            print(f"{bcolors.FAIL}Syntax Error at line #{current_token_line}, Extra: {current_token_name}{bcolors.ENDC}")

    return root


def print_parse_tree(root: Node):
    for pre, fill, node in RenderTree(root, style=ContRoundStyle):
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
