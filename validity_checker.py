'''
CSC 322 - Spring 2019 - Project 1
Finding logical entailments using SAT

Date of creation: Jan 26, 2019
Date of last modification: Feb 7, 2019

Last modified by: Rylan Boothman

'''


import sys
import re
import os
import subprocess
import math
import tempfile
import shutil


#Token classes
token_dict = {'~':-1, '&':-2, 'v':-3,
              '->':-4, '(':-5, ')':-6}

class AST_node:
    'Nodes that form the Abstract Syntax Tree'

    def __init__(self, op, var, lchild, rchild):
        self.op = op
        self.var = var
        self.lchild = lchild
        self.rchild = rchild

    def set_leftchild(self, child):
        self.lchild = child

    def set_rightchild(self, child):
        self.rchild = child


def get_next_var(variables, subf_counter):
    """
    Keeps track of variable numbers given to subformulae, ensuring that they
    are all odd and not in variables
    """
    if subf_counter % 2 == 0:
        msg = "subf_counter must be odd, was {}".format(subf_counter)
        raise ValueError(msg)
    subf_counter += 2
    while subf_counter in variables:
        subf_counter += 2
    variables.append(subf_counter)
    return variables, subf_counter


def parse_sentence(tokens, variables, subf_counter):
    tokens2 = tokens
    sent = parse_disjunction(tokens, variables, subf_counter)

    if not tokens2:
        return sent

    if tokens[0] == -6:
        return sent

    del tokens[0]
    vars, var = get_next_var(variables, subf_counter)
    head = AST_node(-4, var, sent, parse_disjunction(tokens, vars, var))
    return head


def parse_disjunction(tokens, variables, subf_counter):
    disjunc = parse_conjunction(tokens, variables, subf_counter)

    if tokens:
        while tokens and tokens[0] == -3:
            del tokens[0]
            vars, var = get_next_var(variables, subf_counter)
            next_orop = AST_node(-3, var, disjunc, parse_conjunction(tokens, vars, var))
            disjunc = next_orop

    return disjunc


def parse_conjunction(tokens, variables, subf_counter):
    literal = parse_literal(tokens, variables, subf_counter)

    if tokens:
        while tokens and tokens[0] == -2:
            del tokens[0]
            vars, var = get_next_var(variables, subf_counter)
            next_andop = AST_node(-2, var, literal, parse_literal(tokens, vars, var))
            literal = next_andop

    return literal


def parse_literal(tokens, variables, subf_counter):
    vars, var = get_next_var(variables, subf_counter)
    if tokens[0] == -1:
        del tokens[0]
        temp = tokens[0]
        del tokens[0]
        return AST_node(-1, var, parse_atom(tokens, temp, vars, var), None)
    else:
        temp = tokens[0]
        del tokens[0]
        return parse_atom(tokens, temp, variables, var)


def parse_atom(tokens, first, variables, subf_counter):
    if first > 0:
        return AST_node(first, first * 2, None, None)
    else:
        vars, var = get_next_var(variables, subf_counter)
        sent = parse_sentence(tokens, vars, var)
        del tokens[0]
        return sent


def get_clauses(connective, A, LHS, RHS):
    """
    Converts formulae of the form "A = LHS connective RHS" to sets of
    clauses ensuring that the truth value of the formula is computed correctly
    """
    if connective == token_dict['~']:
        return ([[-LHS, -A],
                 [ LHS,  A]])
    if connective == token_dict['&']:
        return([[-LHS, -RHS,  A],
                [-LHS,  RHS, -A],
                [ LHS, -RHS, -A],
                [ LHS,  RHS, -A]])
    elif connective == token_dict['v']:
        return([[-LHS, -RHS,  A],
                [-LHS,  RHS,  A],
                [ LHS, -RHS,  A],
                [ LHS,  RHS, -A]])
    elif connective == token_dict['->']:
        return([[-LHS, -RHS,  A],
                [-LHS,  RHS, -A],
                [ LHS, -RHS,  A],
                [ LHS,  RHS,  A]])
    else:
        raise ValueError(connective + " is not a valid connective")


def convert_to_cnf(ast, output=None):
    """
    Given the root of an AST return its formula in CNF
    """
    if output is None: output = [[-ast.var]]
    if (ast.lchild or ast.rchild):
        convert_to_cnf(ast.lchild, output)
        if (ast.op != -1):
            clauses = get_clauses(ast.op, ast.var, ast.lchild.var, ast.rchild.var)
            output.extend(clauses)
            convert_to_cnf(ast.rchild, output)
        else:
            clauses = get_clauses(ast.op, ast.var, ast.lchild.var, None)
            output.extend(clauses)
    return output


def convert_to_DIMACS(cnf):
    """
    Given a list of lists of a boolean formula in CNF, convert to a string in
    DIMACS format ready to be given to minisat
    """
    max_value = 0
    for f in cnf:
        curr_max = max([abs(x) for x in f])
        if curr_max > max_value:
            max_value = curr_max
        f.append(0)
    cnf = [["p", "cnf", max_value, len(cnf)]] + cnf
    return "\n".join([" ".join([str(x) for x in y]) for y in cnf])


def minisat(dimacs, return_assignment, variables):
    """
    Write dimacs string to temporary file, pass that file to minisat, record
    minisat output in another temporary file, return VALID if minisat returns
    UNSAT, return NOT VALID if minisat returns SAT, if return_assignment set to
    True also return the variable assignment given by minisat when the formula
    is SAT
    """
    temp_dir = tempfile.mkdtemp()
    input_file = temp_dir + '/input.txt'
    output_file = temp_dir + '/output.txt'
    with open(input_file, 'w') as f:
        f.write(dimacs)
    subprocess.call(["minisat", input_file, output_file],
                    stdout=subprocess.PIPE)
    with open(output_file, 'r') as f:
        sat = f.readline().strip()
        if sat == "UNSAT":
            output = "VALID"
        elif sat == "SAT":
            if not return_assignment:
                output = "NOT VALID"
            else:
                assignment = f.readline().strip()
                assignment = [int(x) for x in assignment.split(" ")
                              if int(x) % 2 == 0 and abs(int(x)) > 0]
                assignment = [x for x in assignment if abs(x/2) in variables]
                assignment = ["A" + str(abs(x)//2) + " = F" if x < 0 else
                              "A" + str(abs(x)//2) + " = T" for x in assignment]
                output = "NOT VALID: {}".format(", ".join(assignment))
        else:
            output = "Error minisat did not return SAT or UNSAT"
    shutil.rmtree(temp_dir)
    return output


def tokenize(boolean_formula):
    tokenized_formula = []
    #Tokenize the boolean formula 
    variable = re.compile('A([1-9][0-9]*)')

    #Tokenize all variables
    for v in boolean_formula:
        match = variable.search(v)
        if match:
            for p in re.findall('~|[(]', v):
                tokenized_formula.append(token_dict[p])

            tokenized_formula.append(int(match.group(1)))

            for p in re.findall('[)]', v):
                tokenized_formula.append(token_dict[p])
        else:
            if v in token_dict:
                tokenized_formula.append(token_dict[v])
            else:
                print("Boolean formula misformed, quitting...")
                os._exit(-1)
    return tokenized_formula


def tokenize_many(boolean_formulas):
    tokenized_formulas = []
    for bf in boolean_formulas:
        tokenized_formulas.append(tokenize(bf))
    return tokenized_formulas


def vcheck_1_2(boolean_formula, return_assignment=False):
    tokenized_formula = tokenize(boolean_formula)

    #Parse the tokenized formula and convert to CNF
    variables = [x for x in tokenized_formula if x > 0]
    doubled_vars = [2 * x for x in variables]
    AST_head = parse_sentence(tokenized_formula, doubled_vars, -1)
    cnf = convert_to_cnf(AST_head)
    dimacs = convert_to_DIMACS(cnf)
    return minisat(dimacs, return_assignment, variables)


def vcheck_3(boolean_formulas):
    tokenized_formulas = tokenize_many(boolean_formulas)

    variables = list(set(x for y in tokenized_formulas for x in y if x > 0))
    doubled_vars = [2 * x for x in variables]

    #Parse the tokenized formula and convert to CNF
    cnfs = []
    for f in tokenized_formulas:
        var = get_next_var(doubled_vars, -1)
        cnfs.append(parse_sentence(f, doubled_vars, var))

    if len(cnfs) == 1:
        cnf = convert_to_cnf(cnfs[0])
    elif len(cnfs) == 2:
        var = get_next_var(doubled_vars, var)
        cnf = convert_to_cnf(AST_node(-4, var, cnfs[0], cnfs[1]))
    else:
        var = get_next_var(doubled_vars, var)
        conj = AST_node(-2, var, cnfs[0], cnfs[1])
        for p in range(2, len(cnfs)-2):
            var = get_next_var(doubled_vars, var)
            next_conj = AST_node(-2, var, conj, cnfs[p])
            conj = next_conj
        var = get_next_var(doubled_vars, var)
        cnf = convert_to_cnf(AST_node(-4, var, conj, cnfs[len(cnfs)-1]))

    dimacs = convert_to_DIMACS(cnf)
    return minisat(dimacs, True, variables)

if __name__ == '__main__':
    task_num = int(sys.argv[1])
    if task_num == 1:
        boolean_formula = sys.stdin.readline().split()
        output = vcheck_1_2(boolean_formula, False)
    elif task_num == 2:
        boolean_formula = sys.stdin.readline().split()
        output = vcheck_1_2(boolean_formula, True)
    elif task_num == 3:
        boolean_formulas = [x.split() for x in sys.stdin.readline().split(",")]
        output = vcheck_3(boolean_formulas)
    else:
        output = "Error invalid task number"
    print(output)

