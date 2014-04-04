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

class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

i = 0
f = open('ast.dot','wb')
f.write('strict digraph graphname {\n\n0 [label="program"]\n')
def print_all(n):
	global i
	global f
	ni = i
	i = i+1
	for c in n.children:
		a = '{} {} {} {} \n'.format(i,'[label="',c.data,'"];')
		f.write(a)
		a = '{} {} {} {} \n'.format(ni,'->',i,';')
		f.write(a)
		print_all(c)

def p_program_1(t):
	'program : statements'
	t[0] = t[1]
	print t[0].data
	print_all(t[0])
	f.write('\n\n}')
	f.close()
	pass


def p_statements_1(t):
	'statements : statements statement'
	n = Node('statements1')
	n.add_child(t[1])
	n.add_child(t[2])
	t[0] = n
	pass

def p_statements_2(t):
	'statements : statement'
	t[0] = t[1]
	pass

def p_statement_1(t):
	'statement : declaration'
	t[0] = t[1]
	pass

def p_statement_2(t):
	'statement : exp SEMI_COLON'
	n = Node('statement2')
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	t[0] = n
	pass

def p_statement_3(t):
	'statement : iterative_statement'
	t[0] = t[1]
	pass

def p_statement_4(t):
	'statement : function'
	t[0] = t[1]
	pass

def p_statement_5(t):
	'statement : constant_statement'
	t[0] = t[1]
	pass

def p_constant_statement_1(t):
	'constant_statement : BREAK SEMI_COLON'
	n = Node('constant_statement1')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	t[0] = n
	pass

def p_constant_statement_2(t):
	'constant_statement : CONTINUE SEMI_COLON'
	n = Node('constant_statement2')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	t[0] = n
	pass

def p_constant_statement_3(t):
	'constant_statement : RETURN SEMI_COLON'
	n = Node('constant_statement3')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	t[0] = n
	pass

def p_constant_statement_4(t):
	'constant_statement : RETURN exp SEMI_COLON'
	n = Node('constant_statement4')
	n.add_child(Node(t[1]))
	n.add_child(t[2])
	n.add_child(Node(t[3]))
	t[0] = n
	pass

def p_declaration_1(t):
	'declaration : type enum_list SEMI_COLON'
	n = Node('declaration1')
	n.add_child(t[1])
	n.add_child(t[2])
	n.add_child(Node(t[3]))
	t[0] = n
	pass

def p_enum_list_1(t):
	'enum_list : VARIABLE COMMA enum_list'
	n = Node('enum_list1')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	t[0] = n
	pass

def p_enum_list_2(t):
	'enum_list : VARIABLE EQUALS exp COMMA enum_list'
	n = Node('enum_list2')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	t[0] = n
	pass

def p_enum_list_3(t):
	'enum_list : VARIABLE'
	t[0] = Node(t[1])
	pass

def p_enum_list_4(t):
	'enum_list : VARIABLE EQUALS exp'
	n = Node(t[2])
	n.add_child(Node(t[1]))
	n.add_child(t[3])
	t[0] = n
	pass

def p_type_1(t):
	'type : INT'
	t[0] = Node(t[1])
	pass

def p_type_2(t):
	'type : FLOAT'
	t[0] = Node(t[1])
	pass

def p_type_3(t):
	'type : CHAR'
	t[0] = Node(t[1])
	pass

def p_type_4(t):
	'type : DOUBLE'
	t[0] = Node(t[1])
	pass

def p_type_5(t):
	'type : VOID'
	t[0] = Node(t[1])
	pass

def p_type_6(t):
	'type : SHORT'
	t[0] = Node(t[1])
	pass

def p_type_7(t):
	'type : LONG'
	t[0] = Node(t[1])
	pass

def p_constant_1(t):
	'constant : HEX_INT'
	t[0] = Node(t[1])
	pass

def p_constant_2(t):
	'constant : DOT_REAL'
	t[0] = Node(t[1])
	pass

def p_constant_3(t):
	'constant : EXP_REAL'
	t[0] = Node(t[1])
	pass

def p_constant_4(t):
	'constant : DEC_INT'
	t[0] = Node(t[1])
	pass

def p_constant_5(t):
	'constant : CHARACTER'
	t[0] = Node(t[1])
	pass

def p_exp_1(t):
	'exp : exp ADD exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_2(t):
	'exp : exp MINUS exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_3(t):
	'exp : exp MULT exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_4(t):
	'exp : exp DIV exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_5(t):
	'exp : exp MOD exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_6(t):
	'exp : exp L_OP exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_7(t):
	'exp : exp G_OP exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_8(t):
	'exp : exp LE_OP exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_9(t):
	'exp : exp GE_OP exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_10(t):
	'exp : exp NOTEQUALS exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_11(t):
	'exp : exp EQUALS_OP exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_12(t):
	'exp : exp OR_OP exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_13(t):
	'exp : exp AND_OP exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_14(t):
	'exp : exp MUL_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_15(t):
	'exp : exp DIV_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_16(t):
	'exp : exp MOD_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_17(t):
	'exp : exp ADD_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_18(t):
	'exp : exp SUB_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_19(t):
	'exp : exp LEFT_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_20(t):
	'exp : exp RIGHT_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_21(t):
	'exp : exp AND_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_22(t):
	'exp : exp XOR_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_23(t):
	'exp : exp OR_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_24(t):
	'exp : exp EQUALS exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	pass

def p_exp_25(t):
	'exp : unary_expression'
	t[0] = t[1]
	pass

def p_exp_26(t):
	'exp : LPAREN exp RPAREN'
	n = Node('exp26')
	n.add_child(Node(t[1]))
	n.add_child(t[2])
	n.add_child(Node(t[3]))
	t[0] = n
	pass

def p_exp_27(t):
	'exp : constant'
	t[0] = t[1]
	pass

def p_exp_28(t):
	'exp : VARIABLE'
	t[0] = Node(t[1])
	pass

def p_exp_29(t):
	'exp : function_call'
	t[0] = t[1]
	pass

def p_unary_expression_1(t):
	'unary_expression : VARIABLE unary_operator'
	n = Node('unary_expression1')
	n.add_child(Node(t[1]))
	n.add_child(t[2])
	t[0] = n
	pass

def p_unary_expression_2(t):
	'unary_expression : unary_operator VARIABLE'
	n = Node('unary_expression2')
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	t[0] = n
	pass

def p_unary_operator_1(t):
	'unary_operator : INCREMENT'
	t[0] = Node(t[1])
	pass

def p_unary_operator_2(t):
	'unary_operator : DECREMENT'
	t[0] = Node(t[1])
	pass

def p_iterative_statement_1(t):
	'iterative_statement : FOR LPAREN iterative_exp SEMI_COLON iterative_exp SEMI_COLON iterative_exp RPAREN statement'
	n = Node('iterative_statement1')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(Node(t[6]))
	n.add_child(t[7])
	n.add_child(Node(t[8]))
	n.add_child(t[9])
	t[0] = n
	pass

def p_iterative_statement_2(t):
	'iterative_statement : FOR LPAREN iterative_exp SEMI_COLON iterative_exp SEMI_COLON iterative_exp RPAREN LBRACE statements RBRACE'
	n = Node('iterative_statement2')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(Node(t[6]))
	n.add_child(t[7])
	n.add_child(Node(t[8]))
	n.add_child(Node(t[9]))
	n.add_child(t[10])
	n.add_child(Node(t[11]))
	t[0] = n
	pass

def p_iterative_statement_3(t):
	'iterative_statement : FOR LPAREN iterative_exp SEMI_COLON iterative_exp SEMI_COLON iterative_exp RPAREN SEMI_COLON'
	n = Node('iterative_statement3')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(Node(t[6]))
	n.add_child(t[7])
	n.add_child(Node(t[8]))
	n.add_child(Node(t[9]))
	t[0] = n
	pass

def p_iterative_statement_4(t):
	'iterative_statement : FOR LPAREN iterative_exp SEMI_COLON iterative_exp SEMI_COLON iterative_exp RPAREN LBRACE RBRACE'
	n = Node('iterative_statement4')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(Node(t[6]))
	n.add_child(t[7])
	n.add_child(Node(t[8]))
	n.add_child(Node(t[9]))
	n.add_child(Node(t[10]))
	t[0] = n
	pass

def p_iterative_statement_5(t):
	'iterative_statement : WHILE LPAREN exp RPAREN statement'
	n = Node('iterative_statement5')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	t[0] = n
	pass

def p_iterative_statement_6(t):
	'iterative_statement : WHILE LPAREN exp RPAREN SEMI_COLON'
	n = Node('iterative_statement6')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(Node(t[5]))
	t[0] = n
	pass

def p_iterative_statement_7(t):
	'iterative_statement : WHILE LPAREN exp RPAREN LBRACE statements RBRACE'
	n = Node('iterative_statement7')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(Node(t[5]))
	n.add_child(t[6])
	n.add_child(Node(t[7]))
	t[0] = n
	pass

def p_iterative_statement_8(t):
	'iterative_statement : WHILE LPAREN exp RPAREN LBRACE RBRACE'
	n = Node('iterative_statement8')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(Node(t[5]))
	n.add_child(Node(t[6]))
	t[0] = n
	pass

def p_iterative_statement_9(t):
	'iterative_statement : DO statement WHILE LPAREN exp RPAREN SEMI_COLON'
	n = Node('iterative_statement9')
	n.add_child(Node(t[1]))
	n.add_child(t[2])
	n.add_child(Node(t[3]))
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(Node(t[6]))
	n.add_child(Node(t[7]))
	t[0] = n
	pass

def p_iterative_statement_10(t):
	'iterative_statement : DO LBRACE statements RBRACE WHILE LPAREN exp RPAREN SEMI_COLON'
	n = Node('iterative_statement10')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(Node(t[5]))
	n.add_child(Node(t[6]))
	n.add_child(t[7])
	n.add_child(Node(t[8]))
	n.add_child(Node(t[9]))
	t[0] = n
	pass

def p_iterative_statement_11(t):
	'iterative_statement : DO SEMI_COLON WHILE LPAREN exp RPAREN SEMI_COLON'
	n = Node('iterative_statement11')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(Node(t[6]))
	n.add_child(Node(t[7]))
	t[0] = n
	pass

def p_iterative_statement_12(t):
	'iterative_statement : DO LBRACE RBRACE WHILE LPAREN exp RPAREN SEMI_COLON'
	n = Node('iterative_statement12')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(Node(t[4]))
	n.add_child(Node(t[5]))
	n.add_child(t[6])
	n.add_child(Node(t[7]))
	n.add_child(Node(t[8]))
	t[0] = n
	pass

def p_iterative_exp_1(t):
	'iterative_exp : exp COMMA iterative_exp'
	n = Node('iterative_exp1')
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	t[0] = n
	pass

def p_iterative_exp_2(t):
	'iterative_exp : exp'
	t[0] = t[1]
	pass

def p_function_1(t):
	'function : normal_function'
	t[0] = t[1]
	pass

def p_function_2(t):
	'function : main_function'
	t[0] = t[1]
	pass

def p_main_function_1(t):
	'main_function : type MAIN LPAREN parameters RPAREN LBRACE statements RBRACE'
	n = Node('main_function1')
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(t[4])
	n.add_child(Node(t[5]))
	n.add_child(Node(t[6]))
	n.add_child(t[7])
	n.add_child(Node(t[8]))
	t[0] = n
	pass

def p_main_function_2(t):
	'main_function : type MAIN LPAREN parameters RPAREN LBRACE RBRACE'
	n = Node('main_function2')
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(t[4])
	n.add_child(Node(t[5]))
	n.add_child(Node(t[6]))
	n.add_child(Node(t[7]))
	t[0] = n
	pass

def p_normal_function_1(t):
	'normal_function : type VARIABLE LPAREN parameters RPAREN LBRACE statements RBRACE'
	n = Node('normal_function1')
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(t[4])
	n.add_child(Node(t[5]))
	n.add_child(Node(t[6]))
	n.add_child(t[7])
	n.add_child(Node(t[8]))
	t[0] = n
	pass

def p_normal_function_2(t):
	'normal_function : type VARIABLE LPAREN parameters RPAREN LBRACE RBRACE'
	n = Node('normal_function2')
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(t[4])
	n.add_child(Node(t[5]))
	n.add_child(Node(t[6]))
	n.add_child(Node(t[7]))
	t[0] = n
	pass

def p_parameters_1(t):
	'parameters : type VARIABLE COMMA parameters'
	n = Node('parameters1')
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(t[4])
	t[0] = n
	pass

def p_parameters_2(t):
	'parameters : type VARIABLE'
	n = Node('parameters2')
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	t[0] = n
	pass

def p_parameters_3(t):
	'parameters : empty'
	t[0] = t[1]
	pass

def p_function_call_1(t):
	'function_call : VARIABLE LPAREN arguments RPAREN'
	n = Node('function_call1')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	t[0] = n
	pass

def p_function_call_2(t):
	'function_call : VARIABLE LPAREN RPAREN'
	n = Node('function_call2')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	t[0] = n
	pass

def p_arguments_1(t):
	'arguments : arguments COMMA VARIABLE'
	n = Node('arguments1')
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	t[0] = n
	pass

def p_arguments_2(t):
	'arguments : arguments COMMA constant'
	n = Node('arguments2')
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	t[0] = n
	pass

def p_arguments_3(t):
	'arguments : VARIABLE'
	t[0] = Node(t[1])
	pass

def p_arguments_4(t):
	'arguments : constant'
	t[0] = t[1]
	pass

def p_empty(t):
	'empty : '
	t[0] = Node('empty')
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