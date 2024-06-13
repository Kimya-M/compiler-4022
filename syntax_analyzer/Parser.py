from LeftRecursion import remove_left_recursion, print_grammar
from LeftFactoring import left_factor
from CheckLL1 import is_LL1
from Fcal import print_first_sets, print_follow_sets
from ParsingTable import create_parsing_table, print_parsing_table
from PredictiveParser import predictive_parser, print_parse_tree
from TerminalColors import bcolors
from Grammar import GRAMMAR, START_SYMBOL


# GRAMMAR = {
#         "E": [["E", "t_aop_pl", "T"], ["T"]],
#         "T": [["T", "t_aop_ml", "F"], ["F"]],
#         "F": [["t_lp", "E", "t_rp"], ["t_id"]],
# }

# START_SYMBOL = "E"


if __name__ == "__main__":
    start_symbol = START_SYMBOL

    no_left_recursion_grammar = remove_left_recursion(GRAMMAR)
    print_grammar(no_left_recursion_grammar)

    no_left_factor_grammar = left_factor(no_left_recursion_grammar)
    print_grammar(no_left_factor_grammar)

    is_LL1(no_left_factor_grammar, start_symbol)
    # if is_LL1(no_left_factor_grammar, start_symbol):
    #     print(f"{bcolors.OKGREEN}The grammar is LL(1).{bcolors.ENDC}")
    # else:
    #     print(f"{bcolors.WARNING}The grammar is not LL(1).{bcolors.ENDC}")

    print_first_sets(no_left_factor_grammar)
    print_follow_sets(no_left_factor_grammar, start_symbol)

    parsing_table = create_parsing_table(no_left_factor_grammar, start_symbol)
    print_parsing_table(parsing_table)

    tree_root = predictive_parser(parsing_table, start_symbol)

    print_parse_tree(tree_root)
