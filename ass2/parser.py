import os
import ply.lex as lex
import sys

Matrix = []
stack  = []
array  = []
counter= 1
def createParseTable():
	global Matrix
	Matrix = [
		[],
		[0, 1, None, None, None, None, None, 1, 1, 1, 1, None],
		[0, 2, None, None, None, None, None, 2, 2, 2, 2, None],
		[0, None, 5, 3, 4, None, None, None, None, None, None, 5],
		[0, 6, None, None, None, None, None, 6, 6, 6, 6, None],
		[0, None, 9, 9, 9, 7 ,8, None, None, None, None, 9],
		[0, 10, None, None, None, None, None, 11, 12, 13, 14, None]
	]
	return Matrix

def one():
	global counter
	v = stack.pop()
	counter = counter + 1
	stack.append(counter)
	array.append("E")
	print v, "---->", counter
def two():
	global counter
	v = stack.pop()
	counter = counter + 1
	stack.append(counter)
	array.append("X")
	counter = counter + 1
	stack.append(counter)
	array.append("T")
	print v, "---->", counter, counter-1
def three():
	global counter
	v = stack.pop()
	counter = counter + 1
	array.append("X")
	stack.append(counter)
	counter = counter + 1
	array.append("T")
	stack.append(counter)
	counter = counter + 1
	array.append("ADD")
	stack.append(counter)
	print v, "---->", counter, counter-1, counter-2
def four():
	global counter
	v = stack.pop()
	counter = counter + 1
	array.append("X")
	stack.append(counter)
	counter = counter + 1
	array.append("T")
	stack.append(counter)
	counter = counter + 1
	array.append("MINUS")
	stack.append(counter)
	print v, "---->", counter, counter-1, counter-2
def five():
	v = stack.pop()
	print v, "----> epsilon"
def six():
	global counter
	v = stack.pop()
	counter = counter + 1
	array.append("Y")
	stack.append(counter)
	counter = counter + 1
	array.append("F")
	stack.append(counter)
	print v, "---->", counter, counter-1
def seven():
	global counter
	v = stack.pop()
	counter = counter + 1
	array.append("Y")
	stack.append(counter)
	counter = counter + 1
	array.append("F")
	stack.append(counter)
	counter = counter + 1
	array.append("MULT")
	stack.append(counter)
	print v, "---->", counter, counter-1, counter-2
def eight():
	global counter
	v = stack.pop()
	counter = counter + 1
	array.append("Y")
	stack.append(counter)
	counter = counter + 1
	array.append("F")
	stack.append(counter)
	counter = counter + 1
	array.append("DIV")
	stack.append(counter)
	print v, "---->", counter, counter-1, counter-2
def nine():
	v = stack.pop()
	print v, "----> epsilon"
def ten():
	global counter
	v = stack.pop()
	counter = counter + 1
	array.append(")")
	stack.append(counter)
	counter = counter + 1
	array.append("E")
	stack.append(counter)
	counter = counter + 1
	array.append("(")
	stack.append(counter)
	print v, "---->", counter, counter-1, counter-2
def eleven():
	global counter
	v = stack.pop()
	counter = counter + 1
	array.append("DEC_INT")
	stack.append(counter)
	print v, "---->", counter
def twelve():
	global counter
	v = stack.pop()
	counter = counter + 1
	array.append("EXP_REAL")
	stack.append(counter)
	print v, "---->", counter
def thirteen():
	global counter
	v = stack.pop()
	counter = counter + 1
	array.append("HEX_INT")
	stack.append(counter)
	print v, "---->", counter
def fourteen():
	global counter
	v = stack.pop()
	counter = counter + 1
	array.append("DOT_REAL")
	stack.append(counter)
	print v, "---->", counter

def parser(tok):
	p = stack.pop()
	stack.append(p)
	p = array[p]

	if tok == None:
		return -1
	while not tok.type==p:
	    if not tok: 
	    	break      # No more input
	    '''sys.stdout.write('('+tok.type+', "'+tok.value+'")\n')'''
	    if tok.type == "LPAREN" :
	    	if "S"==p :
	 
	    		options[1]()
	    	elif "E"==p :
	    		
	    		options[2]()
	    	elif "T"==p :
	    		
	    		options[6]()
	    	elif "F"==p :
	    		
	    		options[10]()
	    	elif "("==p :
	    		break
	    	else:
	    		print "errorLPAR"
	    		return -1
	    elif tok.type == "RPAREN" :
	    	if "X"==p :
	    		options[5]()
	    	elif "Y"==p :
	    		
	    		options[9]()
	    	elif ")"==p :
	    		break
	    	else:
	    		print "errorRPAR"
	    		return -1
	    elif tok.type == "ADD" :
	    	if "X"==p :
	    		options[3]()
	    	elif "Y"==p :
	    		options[9]()
	    	else:
	    		print "errorADD"
	    		return -1
	    elif tok.type == "MINUS" :
	    	if "X"==p :
	    		
	    		options[4]()
	    	elif "Y"==p :
	    		
	    		options[9]()
	    	else:
	    		print "errorMINUS"
	    		return -1
	    elif tok.type == "MULT" :
	    	if "Y"==p :
	    		
	    		options[7]()
	    	else:
	    		print "errorMULT"
	    		return -1
	    elif tok.type == "DIV" :
	    	if "Y"==p :
	    		
	    		options[8]()
	    	else:
	    		print "errorDIV"
	    		return -1
	    elif tok.type == "DEC_INT" :
	    	if "S"==p :
	    		options[1]()
	    	elif "E"==p :
	    		options[2]()
	    	elif "T"==p :
	    		options[6]()
	    	elif "F"==p:
	    		options[11]()
	    	else:
	    		print "errorDEC"
	    		return -1
	    elif tok.type == "EXP_REAL" :
	    	if "S"==p :
	    		options[1]()
	    	elif "E"==p :
	    		options[2]()
	    	elif "T"==p :
	    		options[6]()
	    	elif "F"==p :
	    		options[12]()
	    	else:
	    		print "errorEXP"
	    		return -1
	    elif tok.type == "HEX_INT" :
	    	if "S"==p :
	    		
	    		options[1]()
	    	elif "E"==p :
	    		
	    		options[2]()
	    	elif "T"==p :
	    		
	    		options[6]()
	    	elif "F"==p :
	    		
	    		options[13]()
	    	else:
	    		print "errorHEX"
	    		return -1
	    elif tok.type == "DOT_REAL" :
	    	if "S"==p :
	    		
	    		options[1]()
	    	elif "E"==p :
	    		
	    		options[2]()
	    	elif "T"==p :
	    		
	    		options[6]()
	    	elif "F"==p :
	    		
	    		options[14]()
	    	else:
	    		print "errorDOT"
	    		return -1
	    elif tok.type == "EQUALS" :
	    	if "X"==p :
	    		options[5]()
	    	elif "Y"==p :
	    		options[9]()
	    	elif "="==p:
	    		return -1
	    else:
	    	print "errorEQ"
	    	return -1

	    p = stack.pop()
	    stack.append(p)
	    p = array[p]

	stack.pop()
	return 1


options = {1 : one,
	2 : two,
	3 : three,
	4 : four,
	5 : five,
	6 : six,
	7 : seven,
	8 : eight,
	9 : nine,
	10 : ten,
	11 : eleven,
	12 : twelve,
	13 : thirteen,
	14 : fourteen
}

tokens = (
   'ADD',
   'MINUS',
   'MULT',
   'DIV',
   'HEX_INT',
   'EXP_REAL',
   'DOT_REAL',
   'DEC_INT', 
   'LPAREN',
   'RPAREN',
   'EQUALS'
)


t_ADD         = r'\+'
t_MINUS       = r'-'
t_MULT        = r'\*'
t_DIV         = r'/'
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_HEX_INT     = r'0[xX][0-9a-fA-F]+'
t_EXP_REAL    = r'((\d*\.\d+)|(\d+\.\d*)|\d+)(e|E)(\+|-)?\d+'
t_DOT_REAL    = r'(\d*\.\d+)|(\d+\.\d*)'
t_DEC_INT  	  = r'\d+'
t_EQUALS	  = r'\='
t_ignore  	  = ' \t'

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)



lexer = lex.lex()
data = raw_input()
lexer.input(data)
stack.append(0)
stack.append(1)
array.append("=")
array.append("S")
Matrix = createParseTable()

print "--------------------"
print "Rules"
print "--------------------"
while True:
	tok = lexer.token()
	if not tok: 
		break  
	parser(tok)

stack.pop()
j = 0
print "--------------------"
print "Notations"
print "--------------------"
for i in array:
	print j, i
	j+=1