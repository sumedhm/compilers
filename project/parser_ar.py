import sys
import lexer
import ply.yacc as yacc

from lexer import tokens

tokens = lexer.tokens

def p_program_1(t):
	'program : statements'

def p_program_2(t):
	'program : program statements'
	pass

def p_statements_1(t):
	'statements : statements statement'
	pass

def p_statements_2(t):
	'statements : statement'
	pass

'''def p_statements_3(t):
	'statements : COMMENT'
	pass

def p_statements_4(t):
	'statements : statements COMMENT'
	pass

def p_statements_5(t):
	'statements : COMMENT statements'
	pass
'''
def p_statement_1(t):
	'statement : declaration'
	pass

def p_statement_2(t):
	'statement : assignment_statement SEMI_COLON'
	pass	

def p_statement_3(t):
	'statement : exp SEMI_COLON'
	pass

def p_statement_4(t):
	'statement : iterative_statement'
	pass

def p_statement_5(t):
	'statement : conditional_statement'
	pass

'''def p_exp_ender_1(t):
	'exp_ender : SEMI_COLON'
	pass

def p_exp_ender_2(t):
	'exp_ender : empty'
	pass'''

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

def p_assignment_statement_1(t):
	'assignment_statement : VARIABLE assignment_operator exp'
	pass

def p_assignment_statement_2(t):
	'assignment_statement : empty'
	pass

def p_assignment_operator_1(t):
	'assignment_operator : MUL_ASSIGN'
	pass

def p_assignment_operator_2(t):
	'assignment_operator : DIV_ASSIGN'
	pass

def p_assignment_operator_3(t):
	'assignment_operator : MOD_ASSIGN'
	pass

def p_assignment_operator_4(t):
	'assignment_operator : ADD_ASSIGN'
	pass

def p_assignment_operator_5(t):
	'assignment_operator : SUB_ASSIGN'
	pass

def p_assignment_operator_6(t):
	'assignment_operator : LEFT_ASSIGN'
	pass

def p_assignment_operator_7(t):
	'assignment_operator : RIGHT_ASSIGN'
	pass

def p_assignment_operator_8(t):
	'assignment_operator : AND_ASSIGN'
	pass

def p_assignment_operator_9(t):
	'assignment_operator : XOR_ASSIGN'
	pass

def p_assignment_operator_10(t):
	'assignment_operator : OR_ASSIGN'
	pass

def p_assignment_operator_11(t):
	'assignment_operator : EQUALS'
	pass

def p_exp_1(t):
	'exp : exp operator exp'
	pass

def p_exp_2(t):
	'exp : constant'
	pass

def p_exp_3(t):
	'exp : VARIABLE statement_qualifier'
	pass

def p_exp_4(t):
	'exp : unary_operator VARIABLE'
	pass

def p_exp_5(t):
	'exp : comparison_expression'
	pass

def p_exp_6(t):
	'exp : logical_expression'
	pass

def p_statement_qualifier_1(t):
	'statement_qualifier : unary_operator'
	pass

def p_statement_qualifier_2(t):
	'statement_qualifier : empty'
	pass

def p_unary_operator_1(t):
	'unary_operator : INCREMENT'
	pass

def p_unary_operator_2(t):
	'unary_operator : DECREMENT'
	pass

def p_iterative_statement_1(t):
	'iterative_statement : FOR LPAREN assignment_statement SEMI_COLON conditional_expression SEMI_COLON action RPAREN statement'
	pass

def p_iterative_statement_2(t):
	'iterative_statement : FOR LPAREN assignment_statement SEMI_COLON conditional_expression SEMI_COLON action RPAREN LBRACE statements RBRACE'
	pass

def p_iterative_statement_3(t):
	'iterative_statement : WHILE LPAREN conditional_expression RPAREN statement'
	pass

def p_iterative_statement_4(t):
	'iterative_statement : WHILE LPAREN conditional_expression RPAREN LBRACE statements RBRACE'
	pass

def p_iterative_statement_5(t):
	'iterative_statement : DO statement WHILE LPAREN conditional_expression RPAREN SEMI_COLON'
	pass

def p_iterative_statement_6(t):
	'iterative_statement : DO LBRACE statements RBRACE WHILE LPAREN conditional_expression RPAREN SEMI_COLON'
	pass

def p_action_1(t):
	'action : assignment_statement'
	pass

def p_action_2(t):
	'action : exp'
	pass

def p_conditional_statement_1(t):
	'conditional_statement : IF LPAREN conditional_expression RPAREN statement else_statement'
	pass

def p_conditional_statement_2(t):
	'conditional_statement : IF LPAREN conditional_expression RPAREN LBRACE statements RBRACE else_statement'
	pass

def p_else_statement_1(t):
	'else_statement : ELSE statement'
	pass

def p_else_statement_2(t):
	'else_statement : ELSE LBRACE statements RBRACE'
	pass

def p_else_statement_3(t):
	'else_statement : empty'
	pass

def p_conditional_expression_1(t):
	'conditional_expression : exp'
	pass

def p_conditional_expression_2(t):
	'conditional_expression : assignment_statement'
	pass

def p_comparison_expression_1(t):
	'comparison_expression : exp comparison_operator exp'
	pass

def p_logical_expression_1(t):
	'logical_expression : exp logical_operator exp'
	pass

def p_comparison_operator_1(t):
	'comparison_operator : L_OP'
	pass

def p_comparison_operator_2(t):
	'comparison_operator : G_OP'
	pass

def p_comparison_operator_3(t):
	'comparison_operator : LE_OP'
	pass

def p_comparison_operator_4(t):
	'comparison_operator : GE_OP'
	pass


def p_comparison_operator_5(t):
	'comparison_operator : NOTEQUALS'
	pass

def p_comparison_operator_6(t):
	'comparison_operator : EQUALS_OP'
	pass

def p_logical_operator_1(t):
	'logical_operator : OR_OP'
	pass

def p_logical_operator_2(t):
	'logical_operator : AND_OP'
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
