import ply.lex as lex
import sys
import os

reserved = {
	'int' : 'INT',
	'float' : 'FLOAT',
	'char' : 'CHAR',
	'double' : 'DOUBLE',
	'void' : 'VOID',
	'main' : 'MAIN',
	'if' : 'IF',
	'else' : 'ELSE',
	'while' : 'WHILE',
	'for' : 'FOR',
	'do' : 'DO',
	'short' : 'SHORT',
	'long' : 'LONG',
	'case' : 'CASE',
	'default' : 'DEFAULT',
	'switch' : 'SWITCH',
	'continue' : 'CONTINUE',
	'break' : 'BREAK',
	'return' : 'RETURN'
}

tokens = [
   'NEWLINE',
   'SINGLE_QUOTES',
   'DOUBLE_QUOTES',
   'COMMENT',
   'MOD',
   'ADD',
   'MINUS',
   'MULT',
   'DIV',
   'HEX_INT',
   'EXP_REAL',
   'DOT_REAL',
   'DEC_INT',
   'LBRACE',
   'RBRACE', 
   'LPAREN',
   'RPAREN',
   'EQUALS',
   'VARIABLE',
   'SEMI_COLON',
   'COMMA',
   'CONDOP',
   'COLON'
] + list(reserved.values())

t_SINGLE_QUOTES = r'\''
t_DOUBLE_QUOTES = r'\"'
t_NEWLINE = r'\\n'
t_COMMENT = r'(/\*(.|\n)*?\*/)|(//.*)'
t_INT 		  = r'int'
t_FLOAT		  = r'float'
t_CHAR 		  = r'char'
t_ADD         = r'\+'
t_MINUS       = r'-'
t_MULT        = r'\*'
t_DIV         = r'/'
t_MOD	      = r'%'
t_LBRACE      = r'\{'
t_RBRACE      = r'\}'
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_HEX_INT     = r'0[xX][0-9a-fA-F]+'
t_EXP_REAL    = r'((\d*\.\d+)|(\d+\.\d*)|\d+)(e|E)(\+|-)?\d+'
t_DOT_REAL    = r'(\d*\.\d+)|(\d+\.\d*)'
t_DEC_INT  	  = r'\d+'
t_EQUALS	  = r'\='
t_SEMI_COLON  = r'\;'
t_CONDOP      = r'\?'
t_COLON	      = r'\:'
t_COMMA	      = r'\,'
t_ignore  	  = ' \n\r\t'

def t_VARIABLE(t):
	r'[a-zA-Z][0-9a-zA-Z_]*'
	if t.value in reserved:
		t.type = reserved[t.value]
	return t

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)


lexer = lex.lex()
print sys.argv[0]
with open(sys.argv[1], 'r') as content_file:
    data = content_file.read()
lexer.input(data)

while True:
	tok = lexer.token()
	if not tok: break
	print tok.type + " - " + tok.value + "\n"
