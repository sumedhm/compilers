import sys
import lexer
import ply.yacc as yacc

from lexer import tokens

tokens = lexer.tokens

def p_declaration_1(t):
        'declaration : declaration_specifiers SEMI_COLON'
        pass

def p_declaration_2(t):
	'declaration : declaration_specifiers init_declarator_list SEMI_COLON'
	pass

def p_declaration_specifiers_1(t):
	'declaration_specifiers : type_specifier'
	pass

def p_declaration_specifiers_2(t):
        'declaration_specifiers : type_specifier declaration_specifiers'
	pass

def p_type_specifier_1(t):
	'type_specifier : VOID'
	pass

def p_type_specifier_2(t):
        'type_specifier : INT'
        pass

def p_type_specifier_3(t):
        'type_specifier : CHAR'
        pass

def p_type_specifier_4(t):
        'type_specifier : SHORT'
        pass

def p_type_specifier_5(t):
        'type_specifier : LONG'
        pass

def p_type_specifier_6(t):
        'type_specifier : FLOAT'
        pass

def p_type_specifier_7(t):
        'type_specifier : DOUBLE'
        pass  

def p_type_specifier_8(t):
        'type_specifier : enum_specifier'
        pass

def p_enum_specifier_1(t):
	'enum_specifier : type_specifier enum_list'
	pass

def p_enum_list_1(t):
	'enum_list : enumerator'
	pass

def p_enum_list_2(t):
        'enum_list : enum_list COMMA enumerator'
        pass

def p_enumerator_1(t):
	'enumerator : VARIABLE'
	pass

def p_enumerator_2(t):
	'enumerator : VARIABLE EQUALS constant_expression'
	pass

def p_constant_expression(t):
	'constant_expression : conditional_expression'
	pass

def p_conditional_expression_1(t):
	'conditional_expression : logical_or_expression'
	pass

def p_conditional_expression_2(t):
        'conditional_expression : logical_or_expression CONDOP expression COLON conditional_expression'
        pass


def p_logical_or_expression_1(t):
	'logical_or_epression : logical_and_expression '
	pass

def p_logical_or_expression_2(t):
	'logical_or_expression : logical_or_expression OR_OP logical_and_expression'
	pass

def p_logical_and_expression_1(t):
	'logical_and_expression : inclusive_or_expressioin'
pass

def p_logical_and_expression_2(t):
	'logical_and_expression : logical_and_expression AND_OP inclusive_or_expression'
	pass

def p_inclusive_or_expression_1(t):
	'inclusive_or_expression : exclusive_or_expression'
	pass

def p_inclusive_or_expression_2(t):
	'inclusive_or_expression : inclusive_or_expression OR exclusive_or_expression'
	pass

def p_exclusive_or_expression_1(t):
	'exclusive_or_expression : and_expression'
	pass

def p_exclusive_or_expression_2(t):
	'exclusive_or_expression : exclusive_or_expression AND and_expression'
	pass

def p_and_expression_1(t):
	'and_expression : equality_expression'
	pass

def p_and_expression_2(t):
	'and_expression : and_expression AND_OP equality_expression'
	pass

def p_equality_expression_1(t):
	'equality_expression : relational_expression'
	pass

def p_equality_expression_2(t):
	'equality_expression : equality_expression EQUALS relational_expression'
	pass

def p_equality_expression_3(t):
	'equality_expression : equality_expression NOTEQUALS relational_expression'
	pass
def p_relational_expression_1(t):
	'relational_expression : shift_expression'
	pass

def p_relational_expression_2(t):
	'relational_expression : relational_expression L_OP shift_expression'


def p_relational_expression_3(t):
	'relational_expression : relational_expression G_OP shift_expression'
	pass

def p_relational_expression_4(t):
	'relational_expression : relational_expression LE_OP shift_expression'
	pass

def p_relational_expression_5(t):
	'relational_expression : relational_expression GE_OP shift_expression'
	pass

def p_shift_operation_1(t):
	'shift_operation : additive_expression'
	pass

def p_shift_operation_2(t):
	'shift_operation : shift_expression LEFT_OP additive_expression'
	pass

def p_shift_expression_3(t):
	'shift_expression : shift_expression RIGHT_OP additive_expression'
	pass

def p_additive_expression_1(t):
	'additive_expression : multiplicative_expression'
	pass

def p_additive_expression_2(t):
	'additive_expression : additive_expression ADD multiplicative_expression'
	pass

def p_additive_expression_3(t):
	'additive_expression : additive_expression MINUS multiplicative_expression'
	pass

def p_multiplicative_expression_1(t):
	'multiplicative_expression : cast_expression'
	pass

def p_multiplicative_expression_2(t):
	'multiplicative_expressioin : multiplicative_expression MULT cast_expression'
	pass

def p_multiplicative_expression_3(t):
	'multiplicative_expressioin : multiplicative_expression DIV cast_expression'
	pass

def p_multiplicative_expression_4(t):
	'multiplicative_expressioin : multiplicative_expression MOD cast_expression'
	pass

def p_cast_expression_1(t):
	'cast_expression : unary_expression'
	pass

def p_cast_expression_2(t):
	'cast_expression : LPAREN type_name RPAREN cast_expression'
	pass

def p_unary_expression_1(t):
	'unary_expression : postfix_expression'
	pass

def p_unary_expression_2(t):
	'unary_expression : INCREMENT unary_expression'
	pass

def p_unary_expression_3(t):
	'unary_expression : DECREMENT unary_expression'
	pass

def p_unary_expression_4(t):
	'unary_expression : unary_operator  cast_expression'
	pass

def p_unary_expression_5(t):
	'unary_expression : SIZEOF unary_expression'
	pass

def p_unary_expression_6(t):
	'unary_expression : SIZEOF LPAREN type_name RPAREN'
	pass

def p_unary_operator_1(t):
	'unary_operator : AND_OP'
	pass

def p_unary_operator_2(t):
	'unary_operator : MULT'
	pass

def p_unary_operator_3(t):
	'unary_operator : ADD'
	pass
def p_unary_operator_4(t):
	'unary_operator : MINUS'
	pass

def p_unary_operator_5(t):
	'unary_operator : TILDA'
	pass

def p_unary_operator_6(t):
	'unary_operator : NOT'
	pass


def p_type_name_1(t):
	'type_name : specifier_qualifier_list'
	pass

def p_specifier_qualifier_list_1(t):
	'specifier_qualifier_list : type_specifier specifier_qualifier_list'
	pass

def p_specifier_qualifier_list_2(t):
	'specifier_qualifier_list : type_specifier'
	pass

def p_postfix_expression_1(t):
	'postfix_expression : primary_expression'
	pass

def p_postfix_expression_2(t):
	'postfix_expression : postfix_expression LBIG expression RBIG'
	pass

def p_postfix_expression_3(t):
	'postfix_expression : postfix_expression LPAREN RPAREN'
	pass

def p_postfix_expression_4(t):
	'postfix_expression : postfix_expression LPAREN argument_expression_list RPAREN'
	pass

def p_postfix_expression_5(t):
	'post_expression : postfix_expression DOT variable'
	pass

def p_postfix_expression_6(t):
	'post_expression : postfix_expression INCREMENT'
	pass

def p_postfix_expression_7(t):
	'post_expression : postfix_expression DECREMENT'
	pass

def p_argument_expression_list_1(t):
	'argument_expression_list : assignment_expression'
	pass

def p_argument_expression_list_2(t):
	'argument_expression_list : argument_expression_list COMMA assignment_expression'
pass

def p_expression_1(t):
	'expression : assignment_expression'
	pass

def p_expression_2(t):
	'expression : expression COMMA assignment_expression'
pass

def p_assignment_expression_1(t):
	'assignment_expression : contional_expression'
	pass

def p_assignement_expression_2(t):
	'assignment_expression : unary_expression assignment_operator assignment_expression'
	pass

def p_assignment_operator_1(t):
	'assignment_operator : EQUALS'
	pass

def p_assignment_operator_2(t):
	'assignment_operator : MUL_ASSIGN'
	pass

def p_assignment_operator_3(t):
	'assignment_operator : DIV_ASSIGN'
	pass

def p_assignment_operator_4(t):
	'assignment_operator : MOD_ASSIGN'
	pass

def p_assignment_operator_5(t):
	'assignment_operator : ADD_ASSIGN'
	pass

def p_assignment_operator_6(t):
	'assignment_operator : SUB_ASSIGN'
	pass

def p_assignment_operator_7(t):
	'assignment_operator : LEFT_ASSIGN'
	pass

def p_assignment_operator_8(t):
	'assignment_operator : RIGHT_ASSIGN'
	pass

def p_assignment_operator_9(t):
	'assignment_operator : AND_ASSIGN'
	pass

def p_assignment_operator_10(t):
	'assignment_operator : XOR_ASSIGN'
	pass

def p_assignment_operator_11(t):
	'assignment_operator : OR_ASSIGN'
	pass

import profile

yacc.yacc(method='LALR', debug=1)
