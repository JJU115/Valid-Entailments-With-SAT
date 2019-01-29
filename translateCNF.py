'''
CSC 322 - Spring 2019 - Project 1
Finding logical entailments using SAT

Date of creation: Jan 26, 2019
Date of last modification: Jan 29, 2019

Last modified by: Justin Underhay

Notes:

    - Entering boolean formula on command line causes them to be interpreted as bash commands 
      unless enclosed in double quotes: -">" and "&" - Only a problem for implication and AND operators
'''

import sys
import re
import os



tokens2 = []

class AST_node:
    'Nodes that form the Abstract Syntax Tree'

    def __init__(self, op, lchild, rchild):
        self.op = op
        self.lchild = lchild
        self.rchild = rchild


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
    head = AST_node(-4, sent, parse_disjunction(tokens))
    return head    



def parse_disjunction(tokens):
    disjunc = parse_conjunction(tokens)

    if tokens:
        while tokens and tokens[0] == -3:
            del tokens[0]
            next_orop = AST_node(-3, disjunc, parse_conjunction(tokens))
            disjunc = next_orop

    return disjunc    


def parse_conjunction(tokens):
    literal = parse_literal(tokens)

    if tokens:
        while tokens and tokens[0] == -2:
            del tokens[0]
            next_andop = AST_node(-2, literal, parse_literal(tokens))
            literal = next_andop

    return literal


def parse_literal(tokens):
    
    if tokens[0] == -1:
        del tokens[0]
        temp = tokens[0]
        del tokens[0]
        return AST_node(-1, parse_atom(tokens, temp), None)
    else:
        temp = tokens[0]
        del tokens[0]
        return parse_atom(tokens, temp)
    

def parse_atom(tokens, first):
    if first > 0:
        return AST_node(first, None, None)
    else:
        sent = parse_sentence(tokens)
        del tokens[0]
        return sent



#Token classes
token_dict = {'~':-1, '&':-2, 'v':-3,
              '->':-4, '(':-5, ')':-6}


#Acquire command line input
boolean_formula = sys.argv[1:]
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

#Parse the tokenized formula
AST_head = parse_sentence(tokenized_formula)    
print(AST_head.op)     
