import sys
import lexer
import ply.yacc as yacc

from lexer import tokens

tokens = lexer.tokens

precedence = (
 ('left','ADD','MINUS'),
 ('left','MULT','DIV','MOD'),
 ('left','L_OP','G_OP','LE_OP','GE_OP'),
 ('left','NOTEQUALS','EQUALS_OP'),
 ('left','OR_OP','AND_OP'),
 ('right','EQUALS','ADD_ASSIGN','MOD_ASSIGN','SUB_ASSIGN','MUL_ASSIGN','DIV_ASSIGN','LEFT_ASSIGN','RIGHT_ASSIGN','XOR_ASSIGN','OR_ASSIGN','AND_ASSIGN')
)

def p_statements_1(t):
	'statements : statements statement'
	pass

def p_statements_2(t):
	'statements : statement'
	pass

def p_statement_1(t):
	'statement : declaration'
	pass

def p_statement_2(t):
	'statement : exp SEMI_COLON'
	pass

def p_declaration_1(t):
	'declaration : type VARIABLE SEMI_COLON'
	pass

def p_declaration_2(t):
	'declaration : type VARIABLE EQUALS exp SEMI_COLON'

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

def p_type_7(t):
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

def p_constant_6(t):
	'constant : VARIABLE'
	pass

def p_exp_1(t):
	'exp : exp ADD exp'
	pass

def p_exp_2(t):
	'exp : exp MINUS exp'
	pass

def p_exp_3(t):
	'exp : exp MULT exp'
	pass

def p_exp_4(t):
	'exp : exp DIV exp'
	pass

def p_exp_5(t):
	'exp : exp MOD exp'
	pass

def p_exp_6(t):
	'exp : exp L_OP exp'
	pass

def p_exp_7(t):
	'exp : exp G_OP exp'
	pass

def p_exp_8(t):
	'exp : exp LE_OP exp'
	pass

def p_exp_9(t):
	'exp : exp GE_OP exp'
	pass

def p_exp_10(t):
	'exp : exp NOTEQUALS exp'
	pass

def p_exp_11(t):
	'exp : exp EQUALS_OP exp'
	pass

def p_exp_12(t):
	'exp : exp OR_OP exp'
	pass

def p_exp_13(t):
	'exp : exp AND_OP exp'
	pass

def p_exp_14(t):
	'exp : exp MUL_ASSIGN exp'
	pass

def p_exp_15(t):
	'exp : exp DIV_ASSIGN exp'
	pass

def p_exp_16(t):
	'exp : exp MOD_ASSIGN exp'
	pass

def p_exp_17(t):
	'exp : exp AND_ASSIGN exp'
	pass

def p_exp_18(t):
	'exp : exp SUB_ASSIGN exp'
	pass

def p_exp_19(t):
	'exp : exp LEFT_ASSIGN exp'
	pass

def p_exp_20(t):
	'exp : exp RIGHT_ASSIGN exp'
	pass

def p_exp_22(t):
	'exp : exp XOR_ASSIGN exp'
	pass

def p_exp_23(t):
	'exp : exp OR_ASSIGN exp'
	pass

def p_exp_24(t):
	'exp : exp EQUALS exp'
	pass

def p_exp_25(t):
	'exp : constant'
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

parser = yacc.yacc()
parse()
