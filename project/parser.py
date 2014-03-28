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

def enumerator_1(t):
	'enumerator : VARIABLE'
	pass

def enumerator_2(t):
	'enumerator : VARIABLE EQUALS constant_expression'
	pass

def constant_expression(t):
	'constant_expression : conditional_expression'
	pass

def conditional_expression_1(t):
	'conditional_expression : logical_or_expression'
	pass

def conditional_expression_2(t):
        'conditional_expression : logical_or_expression '?' expression'
        pass
