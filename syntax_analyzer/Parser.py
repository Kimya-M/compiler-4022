from LeftRecursion import remove_left_recursion, print_grammar
from LeftFactoring import left_factor
from CheckLL1 import is_LL1
from Fcal import print_first_sets, print_follow_sets
from ParsingTable import create_parsing_table, print_parsing_table, pretty_print_parsing_table
from PredictiveParser import predictive_parser, print_parse_tree
from TerminalColors import bcolors
from Grammar import GRAMMAR, START_SYMBOL
from analyzer import reverse_children, semantic_analyzer


if __name__ == "__main__":
    start_symbol = START_SYMBOL

    print(f"{bcolors.OKBLUE}The Grammar after removing left recursion:{bcolors.ENDC}")
    no_left_recursion_grammar = remove_left_recursion(GRAMMAR)
    print_grammar(no_left_recursion_grammar)
    print(f"{bcolors.OKBLUE}-------------------\n-------------------{bcolors.ENDC}\n")

    print(f"{bcolors.OKBLUE}The Grammar after removing left recursion and left factoring:{bcolors.ENDC}")
    no_left_factor_grammar = left_factor(no_left_recursion_grammar)
    print_grammar(no_left_factor_grammar)
    print(f"{bcolors.OKBLUE}-------------------\n-------------------{bcolors.ENDC}\n")

    if is_LL1(no_left_factor_grammar, start_symbol):
        print(f"{bcolors.OKGREEN}The grammar is LL(1).{bcolors.ENDC}")
    else:
        print(f"{bcolors.FAIL}The grammar is not LL(1).{bcolors.ENDC}")
    print(f"{bcolors.OKBLUE}-------------------\n-------------------{bcolors.ENDC}\n")

    print(f"{bcolors.OKBLUE}First sets:{bcolors.ENDC}")
    print_first_sets(no_left_factor_grammar)
    print(f"{bcolors.OKBLUE}-------------------\n-------------------{bcolors.ENDC}\n")

    print(f"{bcolors.OKBLUE}Follow sets:{bcolors.ENDC}")
    print_follow_sets(no_left_factor_grammar, start_symbol)
    print(f"{bcolors.OKBLUE}-------------------\n-------------------{bcolors.ENDC}\n")

    parsing_table = create_parsing_table(no_left_factor_grammar, start_symbol)
    #print_parsing_table(parsing_table)
    # pretty_print_parsing_table(parsing_table)
    #print(f"{bcolors.OKBLUE}-------------------\n-------------------{bcolors.ENDC}\n")

    tree_root = predictive_parser(parsing_table, start_symbol)

    #print(f"{bcolors.OKBLUE}Parse Tree:{bcolors.ENDC}")
    print_parse_tree(tree_root)

    reverse_children(tree_root)
    
    print(semantic_analyzer(tree_root))
