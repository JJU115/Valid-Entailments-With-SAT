import sys
import re
import os
import itertools
import time
from validity_checker import parse_sentence, tokenize, vcheck_1_2


def brutal(nodeA, tt, var_map):
    if nodeA.op > 0:
        # return tt[(nodeA.op - 1)]
        return tt[var_map[nodeA.op]]
    elif nodeA.op == -1:
        return not brutal(nodeA.lchild, tt, var_map)
    elif nodeA.op == -2:
        return (brutal(nodeA.lchild, tt, var_map) and brutal(nodeA.rchild, tt, var_map))
    elif nodeA.op == -3:
        return (brutal(nodeA.lchild, tt, var_map) or brutal(nodeA.rchild, tt, var_map))
    elif nodeA.op == -4:
        return (not brutal(nodeA.lchild, tt, var_map) or brutal(nodeA.rchild, tt, var_map))


def brute_force(boolean_formula):
    tokenized_formula = tokenize(boolean_formula)
    variables = [x for x in tokenized_formula if x > 0]
    doubled_vars = [2 * x for x in variables]
    num_var = len(variables)
    var_map = {x: variables.index(x) for x in variables} # handle noncontiguous variables

    # creates truth table list
    tt = list(itertools.product([False, True], repeat=num_var))

    AST_head = parse_sentence(tokenized_formula, doubled_vars, -1)

    for i in tt:
        if not brutal(AST_head, i, var_map):
            return "NOT VALID"
    return "VALID"


if __name__ == "__main__":
    boolean_formula = sys.stdin.readline().split()
    start = time.time()
    validity = brute_force(boolean_formula)
    end = time.time()
    start2 = time.time()
    validity2 = vcheck_1_2(boolean_formula, False)
    end2 = time.time()
    print("Brute Force returned: {} in {}s".format(validity, end - start))
    print("CNF method returned: {} in {}s".format(validity2, end2 - start2))



