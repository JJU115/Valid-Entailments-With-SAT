#!/usr/bin/python

import re
import os
import subprocess
import math



tokens2 = []
var_counter = -1

class AST_node:
    'Nodes that form the Abstract Syntax Tree'

    def __init__(self, op, var, lchild, rchild):
        self.op = op
        self.var = var
        self.lchild = lchild
        self.rchild = rchild


    def set_op(self, new_op):
       self.op = new_op     


    def set_leftchild(self, child):
        self.lchild = child


    def set_rightchild(self, child):
        self.rchild = child



def parse_sentence(tokens):
    tokens2 = tokens
    sent = parse_disjunction(tokens)

    if not tokens2:
        return sent

    if tokens[0] == -6:
        return sent

    del tokens[0]
    global var_counter
    var_counter += 2
    head = AST_node(-4, var_counter, sent, parse_disjunction(tokens))
    return head



def parse_disjunction(tokens):
    disjunc = parse_conjunction(tokens)

    if tokens:
        while tokens and tokens[0] == -3:
            del tokens[0]
            global var_counter
            var_counter += 2
            next_orop = AST_node(-3, var_counter, disjunc, parse_conjunction(tokens))
            disjunc = next_orop

    return disjunc


def parse_conjunction(tokens):
    literal = parse_literal(tokens)

    if tokens:
        while tokens and tokens[0] == -2:
            del tokens[0]
            global var_counter
            var_counter += 2
            next_andop = AST_node(-2, var_counter, literal, parse_literal(tokens))
            literal = next_andop

    return literal


def parse_literal(tokens):

    if tokens[0] == -1:
        del tokens[0]
        temp = tokens[0]
        del tokens[0]
        global var_counter
        var_counter += 2
        return AST_node(-1, var_counter, parse_atom(tokens, temp), None)
    else:
        temp = tokens[0]
        del tokens[0]
        return parse_atom(tokens, temp)


def parse_atom(tokens, first):
    if first > 0:
        return AST_node(first, first*2, None, None)
    else:
        sent = parse_sentence(tokens)
        del tokens[0]
        return sent



def get_clauses(connective, A, LHS, RHS):
    """
    Converts formulae of the form "A = LHS connective RHS" to sets of
    clauses ensuring that the truth value of the formula is computed correctly
    """
    if connective == token_dict['~']:
        return ([[-LHS, -A],
                [LHS, A]])
    if connective == token_dict['&']:
        return([[-LHS, -RHS,  A],
                [-LHS,  RHS, -A],
                [ LHS, -RHS, -A],
                [ LHS,  RHS, -A]])
    elif connective == token_dict['v']:
        return([[-LHS, -RHS, A],
                [-LHS,  RHS, A],
                [ LHS, -RHS, A],
                [ LHS,  RHS, -A]])
    elif connective == token_dict['->']:
        return([[-LHS, -RHS, A],
                [-LHS,  RHS, -A],
                [ LHS, -RHS, A],
                [ LHS,  RHS, A]])
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


def split_formulas(input):
    forms = []
    comma1 = 0
    comma2 = 0

    for i in input:
        comma2 += 1

        if ',' in i:
            forms.append(input[comma1:comma2])
            comma1 = comma2

    forms.append(input[comma1:len(input)])

    return forms



#Token classes
token_dict = {'~':-1, '&':-2, 'v':-3,
              '->':-4, '(':-5, ')':-6}       


#Acquire command line input
boolean_formulas = split_formulas(input("Enter comma separated boolean expression(s) >>>").split())
print(boolean_formulas)
tokenized_formula = []
tokenized_formulas = []

#Tokenize the boolean formula 
variable = re.compile('A([1-9][0-9]*)')

#Tokenize all variables
for bf in boolean_formulas:
    for v in bf:
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

    tokenized_formulas.append(tokenized_formula.copy())
    tokenized_formula.clear()            


variables = []

print(tokenized_formulas)

high_var = 0

for i in tokenized_formulas:
    if max(i) > high_var:
        high_var = max(i)
    for v in i:
    	if v > 0 and not v in variables:
		    variables.append(v)

#Parse the tokenized formula and convert to CNF
cnfs = []
for f in tokenized_formulas:
    cnfs.append(parse_sentence(f))    

if len(cnfs) == 1:
    cnf = convert_to_cnf(cnfs[0])
elif len(cnfs) == 2:
    var_counter += 2
    cnf = convert_to_cnf(AST_node(-4, var_counter, cnfs[0], cnfs[1]))
else:
    var_counter += 2
    conj = AST_node(-2, var_counter, cnfs[0], cnfs[1])
    for p in range(2, len(cnfs)-2):
        var_counter += 2
        next_conj = AST_node(-2, var_counter, conj, cnfs[p])
        conj = next_conj
    var_counter += 2    
    cnf = convert_to_cnf(AST_node(-4, var_counter, conj, cnfs[len(cnfs)-1]))    


#Write to file and input to minisat
minisat_input = open("minisat_input.txt", "w")

minisat_input.write("p cnf " + str(high_var) + " " + str(len(cnf)) + "\n")

for clause in cnf:
    for var in clause:
        minisat_input.write(str(var) + " ")
    minisat_input.write("0\n")

minisat_input.close()

l = subprocess.call(["minisat", "minisat_input.txt", "minisat_output.txt"])

if l == 10:
    minisat_out = open("minisat_output.txt", "r")
    minisat_out.readline()
    assign = minisat_out.readline().split()

    for a in assign[:-1]:
	    num = int(math.fabs(float(a)))	
	    if num%2 == 0 and num/2 in variables:
		    if a[0] == '-':
			    truth = "F"
		    else:
			    truth = "T"	
		    print("A" + str(int(num/2)) + " = " + truth)
    minisat_out.close()			
else:
    print("Converted CNF is unsatisfiable, entailment holds")

