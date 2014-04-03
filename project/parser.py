import sys
import lexer
import ply.yacc as yacc

from lexer import tokens

tokens = lexer.tokens

def p_statements_1(t):
	'statements : statements statement SEMI_COLON'
	pass

def p_statements_2(t):
	'statements : statement SEMI_COLON'
	pass

def p_statement_1(t):
	'statement : declaration'
	pass

def p_statement_2(t):
	'statement : assignment_statement'
	pass	

def p_declaration_1(t):
	'declaration : type VARIABLE'
	pass

def p_declaration_2(t):
	'declaration : type VARIABLE EQUALS constant'
	pass

def p_declaration_3(t):
	'declaration : type VARIABLE EQUALS exp'

def p_type_1(t):
	'type : INT'
	pass

def p_type_2(t):
	'type : FLOAT'
	pass

def p_type_3(t):
	'type : CHAR'
	pass

def p_type_4(t):
	'type : DOUBLE'
	pass

def p_type_5(t):
	'type : VOID'
	pass

def p_type_6(t):
	'type : SHORT'
	pass

def p_type_6(t):
	'type : LONG'
	pass

def p_constant_1(t):
	'constant : HEX_INT'
	pass

def p_constant_2(t):
	'constant : DOT_REAL'
	pass

def p_constant_3(t):
	'constant : EXP_REAL'
	pass

def p_constant_4(t):
	'constant : DEC_INT'
	pass

def p_constant_5(t):
	'constant : CHARACTER'
	pass

def p_assignment_statement_1(t):
	'assignment_statement : VARIABLE EQUALS exp'
	pass

def p_exp_1(t):
	'exp : exp operator exp'
	pass

def p_exp_2(t):
	'exp : constant'
	pass

def p_exp_3(t):
	'exp : VARIABLE'
	pass

def p_operator_1(t):
	'operator : ADD'
	pass

def p_operator_2(t):
	'operator : MINUS'
	pass

def p_operator_3(t):
	'operator : MULT'
	pass

def p_operator_4(t):
	'operator : DIV'
	pass

def p_operator_5(t):
	'operator : MOD'
	pass	

def p_empty(t):
	'empty : '
	pass

def p_error(t):
    print "ERROR"


def parse():
	f = open(sys.argv[1])
	p = yacc.parse(f.read(), debug=1)
	print p

import profile
'''yacc.yacc(method='LALR', debug=0)'''
parser = yacc.yacc()
parse()