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

def p_statement_3(t):
	'statement : iterative_statement'
	pass

def p_declaration_1(t):
	'declaration : type enum_list SEMI_COLON'
	pass

def p_enum_list_1(t):
	'enum_list : VARIABLE COMMA enum_list'
	pass

def p_enum_list_2(t):
	'enum_list : VARIABLE EQUALS exp COMMA enum_list'
	pass

def p_enum_list_3(t):
	'enum_list : VARIABLE'
	pass

def p_enum_list_4(t):
	'enum_list : VARIABLE EQUALS exp'
	pass

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
	'exp : exp ADD_ASSIGN exp'
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

def p_exp_21(t):
	'exp : exp AND_ASSIGN exp'
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
	'exp : unary_expression'
	pass

def p_exp_26(t):
	'exp : constant'
	pass

def p_exp_27(t):
	'exp : VARIABLE'
	pass

def p_unary_expression_1(t):
	'unary_expression : VARIABLE unary_operator'
	pass

def p_unary_expression_2(t):
	'unary_expression : unary_operator VARIABLE'
	pass

def p_unary_operator_1(t):
	'unary_operator : INCREMENT'
	pass

def p_unary_operator_2(t):
	'unary_operator : DECREMENT'
	pass

def p_iterative_statement_1(t):
	'iterative_statement : FOR LPAREN iterative_exp SEMI_COLON iterative_exp SEMI_COLON iterative_exp RPAREN statement'
	pass

def p_iterative_statement_2(t):
	'iterative_statement : FOR LPAREN iterative_exp SEMI_COLON iterative_exp SEMI_COLON iterative_exp RPAREN LBRACE statements RBRACE'
	pass

def p_iterative_statement_3(t):
	'iterative_statement : FOR LPAREN iterative_exp SEMI_COLON iterative_exp SEMI_COLON iterative_exp RPAREN SEMI_COLON'
	pass

def p_iterative_statement_4(t):
	'iterative_statement : FOR LPAREN iterative_exp SEMI_COLON iterative_exp SEMI_COLON iterative_exp RPAREN LBRACE RBRACE'
	pass

def p_iterative_statement_5(t):
	'iterative_statement : WHILE LPAREN exp RPAREN statement'
	pass

def p_iterative_statement_6(t):
	'iterative_statement : WHILE LPAREN exp RPAREN SEMI_COLON'
	pass

def p_iterative_statement_7(t):
	'iterative_statement : WHILE LPAREN exp RPAREN LBRACE statements RBRACE'
	pass

def p_iterative_statement_8(t):
	'iterative_statement : WHILE LPAREN exp RPAREN LBRACE RBRACE'
	pass

def p_iterative_statement_9(t):
	'iterative_statement : DO statement WHILE LPAREN exp RPAREN SEMI_COLON'
	pass

def p_iterative_statement_10(t):
	'iterative_statement : DO LBRACE statements RBRACE WHILE LPAREN exp RPAREN SEMI_COLON'
	pass

def p_iterative_statement_11(t):
	'iterative_statement : DO SEMI_COLON WHILE LPAREN exp RPAREN SEMI_COLON'
	pass

def p_iterative_statement_12(t):
	'iterative_statement : DO LBRACE  RBRACE WHILE LPAREN exp RPAREN SEMI_COLON'
	pass

def p_iterative_exp_1(t):
	'iterative_exp : exp COMMA iterative_exp'
	pass

def p_iterative_exp_2(t):
	'iterative_exp : exp'
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
