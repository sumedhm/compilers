import sys
import lexer
import ply.yacc as yacc

from lexer import tokens

tokens = lexer.tokens

precedence = (
 ('right','EQUALS','ADD_ASSIGN','MOD_ASSIGN','SUB_ASSIGN','MUL_ASSIGN','DIV_ASSIGN','LEFT_ASSIGN','RIGHT_ASSIGN','XOR_ASSIGN','OR_ASSIGN','AND_ASSIGN'),
 ('left','OR_OP','AND_OP'),
 ('left','NOTEQUALS','EQUALS_OP'),
 ('left','L_OP','G_OP','LE_OP','GE_OP'),
 ('left','ADD','MINUS'),
 ('left','MULT','DIV','MOD'),
 ('right', 'UELSE'),
 ('right', 'ELSE')
)

var_index = 3

class Table(object):
	def __init__(self, data):
		self.data = data
		self.parent = None
		self.child_tables = []
		self.variables = {}

	def add_table(self, obj):
		self.child_tables.append(obj)
		obj.parent = self

	def add_variable(self, obj, setType, setSize=0, func=0):
		if obj in self.variables:
			return False
		else:
			self.variables[obj] = {}
			self.variables[obj]['type'] = setType
			self.variables[obj]['size'] = setSize
			self.variables[obj]['offset'] = 'NA'
			i = 0
			if not func==1:
				global var_index
				var_index += 1
				i = var_index
			self.variables[obj]['index'] = i
			self.variables[obj]['mass'] = 0
			return True

class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []
        self.code = ""
        self.next = "next"
        self.place = ""
        self.count = 0
        self.type = 'i'
        self.var = 0
        self.array = 0
        self.lastIndex = 0

    def add_child(self, obj):
        self.children.append(obj)


mass = 3
errors = 0
labels = 0
offset = 0
type_size = {'int':4,'char':1,'float':4,'double':8,'function':0}
lineno = 1
global_scope = Table('Global_variables')
current_scope = global_scope
tableux = 1

i = 0
f = open('mach.dot','wb')
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

def print_table(obj):
	print "\nPrinting table", obj.data
	for j in obj.variables:
		print j, ':', obj.variables[j]
	print "Children of", obj.data, ":",
	flag = False
	for i in obj.child_tables:
		flag = True
		print i.data,
	if(not flag):
		print "No child\n"
	else:
		print " "
	for i in obj.child_tables:
		print_table(i)

def p_program_1(t):
	'program : statements'
	t[0] = t[1]
	print_all(t[0])
	global f
	f.write('\n\n}')
	f.close()
	t[0].code = t[1].code
	f = open(sys.argv[1]+'.j','wb')
	f.write(t[0].code)
	f.close()
	global global_scope
	print_table(global_scope)
	pass


def p_statements_1(t):
	'statements : statements statement'
	n = Node('statements1')
	n.add_child(t[1])
	n.add_child(t[2])
	t[0] = n
	t[0].code = t[1].code + t[2].code
	t[0].next = t[2].next
	pass

def p_statements_2(t):
	'statements : statement'
	t[0] = t[1]
	t[0].code = t[1].code
	t[0].next = t[1].next
	pass

def p_statement_1(t):
	'statement : declaration'
	t[0] = t[1]
	t[0].code = t[1].code
	t[0].next = t[1].next
	pass

def p_statement_2(t):
	'statement : exp SEMI_COLON'
	n = Node('statement2')
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	t[0] = n
	t[0].code = t[1].code
	t[0].next = t[1].next
	pass

def p_statement_3(t):
	'statement : iterative_statement'
	t[0] = t[1]
	t[0].code = t[1].code
	t[0].next = t[1].next
	pass

def p_statement_4(t):
	'statement : function'
	t[0] = t[1]
	t[0].code = t[1].code
	t[0].next = t[1].next
	pass

def p_statement_5(t):
	'statement : constant_statement'
	t[0] = t[1]
	t[0].code = t[1].code
	t[0].next = t[1].next
	pass

def p_statement_6(t):
	'statement : conditional_statement'
	t[0] = t[1]
	t[0].code = t[1].code
	t[0].next = t[1].next
	pass

def p_statement_7(t):
	'statement : COMMENT'
	t[0] = Node(t[1])
	t[0].code = ""
	pass

def p_constant_statement_1(t):
	'constant_statement : BREAK SEMI_COLON'
	n = Node('constant_statement1')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	t[0] = n
	t[0].code = 'break' + "\n"
	pass

def p_constant_statement_2(t):
	'constant_statement : CONTINUE SEMI_COLON'
	n = Node('constant_statement2')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	t[0] = n
	t[0].code = 'continue ' + ";\n"
	pass

def p_constant_statement_3(t):
	'constant_statement : RETURN SEMI_COLON'
	n = Node('constant_statement3')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	t[0] = n
	t[0].code = 'return ' + ";\n"
	pass

def p_constant_statement_4(t):
	'constant_statement : RETURN exp SEMI_COLON'
	n = Node('constant_statement4')
	n.add_child(Node(t[1]))
	n.add_child(t[2])
	n.add_child(Node(t[3]))
	t[0] = n
	t[0].code = t[2].code + "\n_x1 = " + t[2].place + ";\nreturn _x1;\n"
	t[0].next = t[2].next
	pass

def p_declaration_1(t):
	'declaration : type enum_list SEMI_COLON'
	n = Node('declaration1')
	n.add_child(t[1])
	n.add_child(t[2])
	n.add_child(Node(t[3]))
	global current_scope, offset
	for i in current_scope.variables:
		if(current_scope.variables[i]['type']=='NA'):
			current_scope.variables[i]['type'] = t[1].data
		if(current_scope.variables[i]['offset']=='NA'):
			current_scope.variables[i]['offset'] = offset
			if not current_scope.variables[i]['size']==-1:
				offset += type_size[t[1].data]
	t[0] = n
	t[0].code = t[2].code.replace('newarray', 'newarray '+ t[1].place.lower())
	t[0].code = t[0].code.replace('___type___', t[1].place.lower()[0])
	t[0].next = t[2].next
	pass

def p_enum_list_1(t):
	'enum_list : VARIABLE COMMA enum_list'
	n = Node('enum_list1')
	global current_scope, errors, mass
	new_var = current_scope.add_variable(t[1], 'NA')
	if(not new_var):
		errors += 1
		print "Error : line", t.lexer.lineno,": Variable", t[1], "declared multiple times in same scope."
	else:
		mass += 1
		current_scope.variables[t[1]]['mass'] = mass
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	t[0] = n
	t[0].code = t[3].code
	t[0].next = t[3].next
	pass

def p_enum_list_2(t):
	'enum_list : VARIABLE EQUALS exp COMMA enum_list'
	n = Node('enum_list2')
	global current_scope, errors, mass
	new_var = current_scope.add_variable(t[1], 'NA')
	if(not new_var):
		errors += 1
		print "Error : line", t.lexer.lineno,": Variable", t[1], "declared multiple times in same scope."
	else:
		mass += 1
		current_scope.variables[t[1]]['mass'] = mass
	x = Node(t[2])
	x.add_child(Node(t[1]))
	x.add_child(t[3])
	n.add_child(x)
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	t[0] = n
	t[0].code = t[3].code + "\n_x1 = " + t[3].place + ";\n" + t[1]+ " = _x1;\n" + t[5].code + "\n"
	t[0].next = t[3].next
	pass

def p_enum_list_3(t):
	'enum_list : VARIABLE'
	global current_scope, errors, mass
	new_var = current_scope.add_variable(t[1], 'NA')
	if(not new_var):
		errors += 1
		print "Error : line", t.lexer.lineno,": Variable", t[1], "declared multiple times in same scope."
	else:
		mass += 1
		current_scope.variables[t[1]]['mass'] = mass
	t[0] = Node(t[1])
	t[0].code = ""
	pass

def p_enum_list_4(t):
	'enum_list : VARIABLE EQUALS exp'
	global current_scope, errors, mass
	new_var = current_scope.add_variable(t[1], 'NA')
	if(not new_var):
		errors += 1
		print "Error : line", t.lexer.lineno,": Variable", t[1], "declared multiple times in same scope."
	else:
		mass += 1
		current_scope.variables[t[1]]['mass'] = mass
	n = Node(t[2])
	n.add_child(Node(t[1]))
	n.add_child(t[3])
	t[0] = n
	global labels
	labels += 1
	t[0].code = t[3].code + "\n" + str(labels) + ": " + t[3].type + "load " + t[3].place + "\n"
	t[0].code += str(labels+1) + ": " + t[3].type + "store " + str(current_scope.variables[t[1]]['mass']) + "\n"
	labels += 1
	t[0].next = t[3].next
 	pass

def p_enum_list_5(t):
	'enum_list : VARIABLE LBIG exp RBIG COMMA enum_list'
	n = Node('enum_list5')
	global current_scope, errors
	new_var = current_scope.add_variable(t[1], 'NA', t[3].data)
	if(not new_var):
		errors += 1
		print "Error : line", t.lexer.lineno,": Variable", t[1], "declared multiple times in same scope."
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(Node(t[5]))
	n.add_child(t[6])
	global labels
	labels += 1
	t[0].code = t[6].code + t[3].code + str(labels) + ": ___type___load " + t[3].place + "\n"
	t[0].code += str(labels+1) + ": newarray\n" + str(labels+2) + ": astore " + str(current_scope.variables[t[1]]['index']) + "\n"
	labels += 2
	t[0].next = t[6].next
	pass

def p_enum_list_6(t):
	'enum_list : VARIABLE LBIG exp RBIG EQUALS LBRACE num_list RBRACE COMMA enum_list'
	n = Node('enum_list6')
	global current_scope, errors
	new_var = current_scope.add_variable(t[1], 'NA', t[3].data)
	if(not new_var):
		errors += 1
		print "Error : line", t.lexer.lineno,": Variable", t[1], "declared multiple times in same scope."
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(Node(t[5]))
	n.add_child(Node(t[6]))
	n.add_child(t[7])
	n.add_child(Node(t[8]))
	n.add_child(Node(t[9]))
	n.add_child(t[10])
	t[0] = n
	t[0].code = t[7].code
	num_list = t[7].place.split(',')
	j = 0
	for i in num_list:
		t[0].code += t[1] + "[" + str(j) + "] = " +  i + ";\n"
		j += 1
	t[0].code += t[10].code
	t[0].next = t[10].next
	pass

def p_enum_list_7(t):
	'enum_list : VARIABLE LBIG exp RBIG'
	n = Node('enum_list7')
	global current_scope, errors
	new_var = current_scope.add_variable(t[1], 'NA', t[3].data)
	if(not new_var):
		errors += 1
		print "Error : line", t.lexer.lineno,": Variable", t[1], "declared multiple times in same scope."
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	t[0] = n
	global labels
	labels += 1
	t[0].code = t[3].code + str(labels) + ": ___type___load " + t[3].place + "\n"
	t[0].code += str(labels+1) + ": newarray\n" + str(labels+2) + ": astore " + str(current_scope.variables[t[1]]['index']) + "\n"
	labels += 2
	t[0].next = t[3].next 
	pass

def p_enum_list_8(t):
	'enum_list : VARIABLE LBIG exp RBIG EQUALS LBRACE num_list RBRACE'
	n = Node('enum_list8')
	global current_scope, errors
	new_var = current_scope.add_variable(t[1], 'NA', t[3].data)
	if(not new_var):
		errors += 1
		print "Error : line", t.lexer.lineno,": Variable", t[1], "declared multiple times in same scope."
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(Node(t[5]))
	n.add_child(Node(t[6]))
	n.add_child(t[7])
	n.add_child(Node(t[8]))
	t[0] = n
	t[0].code = t[7].code;
	global labels
	num_list = t[7].place.split(',')
	j = 0
	for i in num_list:
		t[0].code += "\n" + t[1] + "[" + str(j) + "] = " +  i + ";\n"
		j += 1
	t[0].next = t[7].next
	pass

def p_num_list_1(t):
	'num_list : exp COMMA num_list'
	n = Node('num_list1')
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	labels += 1
	new_var = mass
	t[0].code = t[3].code + t[1].code + "\n" + str(labels) + ": " + t[1].type + "load " + t[1].place + "\n"
	t[0].place = new_var + "," + t[3].place
	t[0].next = t[3].next
	pass

def p_num_list_2(t):
	'num_list : exp'
	t[0] = t[1]
	global mass, labels
	labels += 1
	new_var = mass
	t[0].code = t[1].code + "\n" + str(labels) + ": " + t[1].type + "load " + t[1].place + "\n"
	t[0].place = new_var
	t[0].next = t[1].next
	pass

def p_type_1(t):
	'type : INT'
	t[0] = Node(t[1])
	t[0].code = ""
	t[0].place = t[1]
	pass

def p_type_2(t):
	'type : FLOAT'
	t[0] = Node(t[1])
	t[0].code = ""
	t[0].place = t[1]
	pass

def p_type_3(t):
	'type : CHAR'
	t[0] = Node(t[1])
	t[0].code = ""
	t[0].place = t[1]
	pass

def p_type_4(t):
	'type : DOUBLE'
	t[0] = Node(t[1])
	t[0].code = ""
	t[0].place = t[1]
	pass

def p_type_5(t):
	'type : VOID'
	t[0] = Node(t[1])
	t[0].code = ""
	t[0].place = t[1]
	pass

def p_type_6(t):
	'type : SHORT'
	t[0] = Node(t[1])
	t[0].code = ""
	t[0].place = t[1]
	pass

def p_type_7(t):
	'type : LONG'
	t[0] = Node(t[1])
	t[0].code = ""
	t[0].place = t[1]
	pass

def p_constant_1(t):
	'constant : HEX_INT'
	t[0] = Node(t[1])
	t[0].code = ""
	t[0].place = t[1]
	pass

def p_constant_2(t):
	'constant : DOT_REAL'
	t[0] = Node(t[1])
	t[0].code = ""
	t[0].place = t[1]
	pass

def p_constant_3(t):
	'constant : EXP_REAL'
	t[0] = Node(t[1])
	t[0].code = ""
	t[0].place = t[1]
	pass

def p_constant_4(t):
	'constant : DEC_INT'
	t[0] = Node(t[1])
	t[0].code = ""
	t[0].place = t[1]
	pass

def p_constant_5(t):
	'constant : CHARACTER'
	t[0] = Node(t[1])
	t[0].code = ""
	t[0].place = t[1]
	pass

def p_exp_1(t):
	'exp : exp ADD exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	exp
	global mass, labels
	mass += 1
	new_var = str(mass)
	labels += 1
	t[0].code = t[1].code + "\n" + t[3].code + "\n" + str(labels) + ": " + t[0].type + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n" + str(labels+2) + ": " + t[0].type + "add\n" + str(labels+3) + ": " + t[0].type + "store " + new_var + "\n"
	labels += 3
	t[0].place = new_var
	t[0].next = t[3].next
	pass

def p_exp_2(t):
	'exp : exp MINUS exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	mass += 1
	new_var = str(mass)
	t[0].code = t[1].code + "\n" + t[3].code + "\n" + str(labels) + ": " + t[0].type + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n" + str(labels+2) + ": " + t[0].type + "sub\n" + str(labels+3) + ": " + t[0].type + "store " + new_var + "\n"
	labels += 3
	t[0].place = new_var
	t[0].next = t[3].next
	pass

def p_exp_3(t):
	'exp : exp MULT exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	mass += 1
	new_var = str(mass)
	t[0].code = t[1].code + "\n" + t[3].code + "\n" + str(labels) + ": " + t[0].type + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n" + str(labels+2) + ": " + t[0].type + "mul\n" + str(labels+3) + ": " + t[0].type + "store " + new_var + "\n"
	labels += 3
	t[0].place = new_var
	t[0].next = t[3].next
	pass

def p_exp_4(t):
	'exp : exp DIV exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	mass += 1
	new_var = str(mass)
	t[0].code = t[1].code + "\n" + t[3].code + "\n" + str(labels) + ": " + t[0].type + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n" + str(labels+2) + ": " + t[0].type + "div\n" + str(labels+3) + ": " + t[0].type + "store " + new_var + "\n"
	labels += 3
	t[0].place = new_var
	t[0].next = t[3].next
	pass

def p_exp_5(t):
	'exp : exp MOD exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	mass += 1
	new_var = str(mass)
	t[0].code = t[1].code + "\n" + t[3].code + "\n" + str(labels) + ": " + t[0].type + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n" + str(labels+2) + ": " + t[0].type + "rem\n" + str(labels+3) + ": " + t[0].type + "store " + new_var + "\n"
	labels += 3
	t[0].place = new_var
	t[0].next = t[3].next
	pass

def p_exp_6(t):
	'exp : exp L_OP exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	labels += 1
	mass += 1
	new_var = str(mass)
	t[0].code = "\n" + str(labels) + ": " + t[0].type + "const_0\n" + str(labels+1) + ": " + t[0].type + "store " + new_var + "\n" + t[1].code + t[3].code
	labels += 2
	t[0].code += "\n" + str(labels) + ": " + t[0].type + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place
	labels += 2
	t[0].code += "\n" + str(labels) + ": if_icmple " + str(labels+3)
	labels += 1
	t[0].code += "\n" + str(labels) + ": " + t[0].type + "const_1\n" + str(labels+1) + ": " + t[0].type + "store " + new_var + "\n" + str(labels+2) + ": \n"
	labels += 2
	t[0].place = new_var
	t[0].next = t[3].next
	pass

def p_exp_7(t):
	'exp : exp G_OP exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	labels += 1
	mass += 1
	new_var = str(mass)
	t[0].code = "\n" + str(labels) + ": " + t[0].type + "const_0\n" + str(labels+1) + ": " + t[0].type + "store " + new_var + "\n" + t[1].code + t[3].code
	labels += 2
	t[0].code += "\n" + str(labels) + ": " + t[0].type + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place
	labels += 2
	t[0].code += "\n" + str(labels) + ": if_icmpge " + str(labels+3)
	labels += 1
	t[0].code += "\n" + str(labels) + ": " + t[0].type + "const_1\n" + str(labels+1) + ": " + t[0].type + "store " + new_var + "\n" + str(labels+2) + ": \n"
	labels += 2
	t[0].place = new_var
	t[0].next = t[3].next
	pass

def p_exp_8(t):
	'exp : exp LE_OP exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	mass += 1
	new_var = str(mass)
	t[0].code = "\n" + str(labels) + ": " + t[0].type + "const_1\n" + str(labels+1) + ": " + t[0].type + "store " + new_var + "\n" + t[1].code + t[3].code
	labels += 2
	t[0].code += "\n" + str(labels) + ": " + t[0].type + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n"
	labels += 2
	t[0].code += "\n" + str(labels) + ": if_icmpge " + str(labels+3)
	t[0].code += "\n" + str(labels+1) + ": " + t[0].type + "const_0\n" + str(labels+2) + ": " + t[0].type + "store " + new_var + "\n" + str(labels+3) + ":\n"
	labels += 3
	t[0].place = new_var
	t[0].next = t[3].next
	pass

def p_exp_9(t):
	'exp : exp GE_OP exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	mass += 1
	new_var = str(mass)
	t[0].code = "\n" + str(labels) + ": " + t[0].type + "const_1\n" + str(labels+1) + ": " + t[0].type + "store " + new_var + "\n" + t[1].code + t[3].code
	labels += 2
	t[0].code += "\n" + str(labels) + ": " + t[0].type + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n"
	labels += 2
	t[0].code += "\n" + str(labels) + ": if_icmple " + str(labels+3)
	t[0].code += "\n" + str(labels+1) + ": " + t[0].type + "const_0\n" + str(labels+2) + ": " + t[0].type + "store " + new_var + "\n" + str(labels+3) + ":\n"
	labels += 3
	t[0].place = new_var
	t[0].next = t[3].next
	pass

def p_exp_10(t):
	'exp : exp NOTEQUALS exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	mass += 1
	labels += 1
	new_var = str(mass)
	t[0].code = "\n" + str(labels) + ": " + t[0].type + "const_1\n" + str(labels+1) + ": " + t[0].type + "store " + new_var + "\n"
	labels += 2
	t[0].code += t[1].code + t[3].code + str(labels) + ": " + t[0].type  + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n"
	labels += 2
	t[0].code += str(labels) + ": if_icmpne " + str(labels+3) + "\n"+ str(labels+1) + ": " + t[0].type + "const_0\n"
	t[0].code += str(labels+2) + ": " + t[0].type + "store " + new_var + "\n" + str(labels+3) + ":\n"
	labels += 3
	t[0].place = new_var
	t[0].next = t[3].next
	pass

def p_exp_11(t):
	'exp : exp EQUALS_OP exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	mass += 1
	labels += 1
	new_var = str(mass)
	t[0].code = "\n" + str(labels) + ": " + t[0].type + "const_0\n" + str(labels+1) + ": " + t[0].type + "store " + new_var + "\n"
	labels += 2
	t[0].code += t[1].code + t[3].code + str(labels) + ": " + t[0].type  + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n"
	labels += 2
	t[0].code += str(labels) + ": if_icmpne " + str(labels+3) + "\n"+ str(labels+1) + ": " + t[0].type + "const_1\n"
	t[0].code += str(labels+2) + ": " + t[0].type + "store " + new_var + "\n" + str(labels+3) + ":\n"
	labels += 3
	t[0].place = new_var
	t[0].next = t[3].next
	pass

def p_exp_12(t):
	'exp : exp OR_OP exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global labels, mass
	labels += 1
	mass += 1
	new_var = str(mass)
	t[0].code = t[1].code + t[3].code + str(labels) + ": " + t[0].type + "const_0\n" + str(labels+1) + ": " + t[0].type + "store " + new_var + "\n"
	labels += str(labels+2) + ": " + t[0].type + "load " + t[1].place + "\n"
	labels += 3
	t[0].code += str(labels) + ": ifgt " + str(labels+4) + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n"
	t[0].code += str(labels+2) + ": ifgt " + str(labels+4) + "\n" + str(labels+3) + ": goto " + str(labels+6) + ":\n"
	t[0].code += str(labels+4) + ": " + t[0].type + "const_1\n" + str(labels+5) + ": " + t[0].type + "store " + new_var + "\n"
	t[0].code += str(labels+6) + ":\n"
	labels += 6
	t[0].place = new_var
	t[0].next = t[3].next
	pass

def p_exp_13(t):
	'exp : exp AND_OP exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global labels, mass
	labels += 1
	mass += 1
	new_var = str(mass)
	t[0].code = t[1].code + t[3].code + str(labels) + ": " + t[0].type + "const_1\n" + str(labels+1) + ": " + t[0].type + "store " + new_var + "\n"
	labels += str(labels+2) + ": " + t[0].type + "load " + t[1].place + "\n"
	labels += 3
	t[0].code += str(labels) + ": ifeq " + str(labels+4) + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n"
	t[0].code += str(labels+2) + ": ifeq " + str(labels+4) + "\n" + str(labels+3) + ": goto " + str(labels+6) + ":\n"
	t[0].code += str(labels+4) + ": " + t[0].type + "const_0\n" + str(labels+5) + ": " + t[0].type + "store " + new_var + "\n"
	t[0].code += str(labels+6) + ":\n"
	labels += 6
	t[0].place = new_var
	t[0].next = t[3].next
	pass

def p_exp_14(t):
	'exp : exp MUL_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	labels += 1
	t[0].code = "\n" + str(labels) + ": " + t[0].type + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n"
	t[0].code += str(labels+2) + ": " + t[0].type + "mul\n" + str(labels+3) + ": " + t[0].type + "store " + t[1].place + "\n"
	labels += 3
	t[0].place = t[1].place
	t[0].next = t[3].next
	pass

def p_exp_15(t):
	'exp : exp DIV_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	labels += 1
	t[0].code = "\n" + str(labels) + ": " + t[0].type + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n"
	t[0].code += str(labels+2) + ": " + t[0].type + "div\n" + str(labels+3) + ": " + t[0].type + "store " + t[1].place + "\n"
	labels += 3
	t[0].place = t[1].place
	t[0].next = t[3].next
	pass

def p_exp_16(t):
	'exp : exp MOD_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	labels += 1
	t[0].code = "\n" + str(labels) + ": " + t[0].type + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n"
	t[0].code += str(labels+2) + ": " + t[0].type + "rem\n" + str(labels+3) + ": " + t[0].type + "store " + t[1].place + "\n"
	labels += 3
	t[0].place = t[1].place
	t[0].next = t[3].next
	pass

def p_exp_17(t):
	'exp : exp ADD_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	labels += 1
	t[0].code = "\n" + str(labels) + ": " + t[0].type + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n"
	t[0].code += str(labels+2) + ": " + t[0].type + "add\n" + str(labels+3) + ": " + t[0].type + "store " + t[1].place + "\n"
	labels += 3
	t[0].place = t[1].place
	t[0].next = t[3].next
	pass

def p_exp_18(t):
	'exp : exp SUB_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	labels += 1
	t[0].code = "\n" + str(labels) + ": " + t[0].type + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n"
	t[0].code += str(labels+2) + ": " + t[0].type + "sub\n" + str(labels+3) + ": " + t[0].type + "store " + t[1].place + "\n"
	labels += 3
	t[0].place = t[1].place
	t[0].next = t[3].next
	pass

def p_exp_19(t):
	'exp : exp LEFT_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	labels += 1
	t[0].code = "\n" + str(labels) + ": " + t[0].type + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n"
	t[0].code += str(labels+2) + ": " + t[0].type + "shl\n" + str(labels+3) + ": " + t[0].type + "store " + t[1].place + "\n"
	labels += 3
	t[0].place = t[1].place
	t[0].next = t[3].next
	pass

def p_exp_20(t):
	'exp : exp RIGHT_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	labels += 1
	t[0].code = "\n" + str(labels) + ": " + t[0].type + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n"
	t[0].code += str(labels+2) + ": " + t[0].type + "shr\n" + str(labels+3) + ": " + t[0].type + "store " + t[1].place + "\n"
	labels += 3
	t[0].place = t[1].place
	t[0].next = t[3].next
	pass

def p_exp_21(t):
	'exp : exp AND_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	labels += 1
	t[0].code = "\n" + str(labels) + ": " + t[0].type + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n"
	t[0].code += str(labels+2) + ": " + t[0].type + "and\n" + str(labels+3) + ": " + t[0].type + "store " + t[1].place + "\n"
	labels += 3
	t[0].place = t[1].place
	t[0].next = t[3].next
	pass

def p_exp_22(t):
	'exp : exp XOR_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	labels += 1
	t[0].code = "\n" + str(labels) + ": " + t[0].type + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n"
	t[0].code += str(labels+2) + ": " + t[0].type + "xor\n" + str(labels+3) + ": " + t[0].type + "store " + t[1].place + "\n"
	labels += 3
	t[0].place = t[1].place
	t[0].next = t[3].next
	pass

def p_exp_23(t):
	'exp : exp OR_ASSIGN exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global mass, labels
	labels += 1
	t[0].code = "\n" + str(labels) + ": " + t[0].type + "load " + t[1].place + "\n" + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n"
	t[0].code += str(labels+2) + ": " + t[0].type + "or\n" + str(labels+3) + ": " + t[0].type + "store " + t[1].place + "\n"
	labels += 3
	t[0].place = t[1].place
	t[0].next = t[3].next
	pass

def p_exp_24(t):
	'exp : exp EQUALS exp'
	n = Node(t[2])
	n.add_child(t[1])
	n.add_child(t[3])
	t[0] = n
	global labels, current_scope
	is_array = t[1].array
	if is_array >= 1:
		t[0].code = t[1].code + t[3].code + str(labels+1) + ": aload " + str(current_scope.variables[t[1].var]['index']) + "\n"
		t[0].code += str(labels+2) + ": " + t[0].type + "load " + t[1].lastIndex + "\n" + str(labels+3) + ": " + t[0].type + "load " + t[3].place + "\n"
		t[0].code += str(labels+4) + ": " + t[0].type + "astore\n"
	else :
		t[0].code = t[1].code + t[3].code + str(labels+1) + ": " + t[0].type + "load " + t[3].place + "\n"
		t[0].code += str(labels+2) + ": " + t[0].type + "store " + t[1].place + "\n"
		labels += 2
	t[0].place = t[1].place
	t[0].next = t[3].next
	pass

def p_exp_25(t):
	'exp : unary_expression'
	t[0] = t[1]
	t[0].code = t[1].code
	t[0].place = t[1].place
	t[0].next = t[1].next
	pass

def p_exp_26(t):
	'exp : LPAREN exp RPAREN'
	n = Node('exp26')
	n.add_child(Node(t[1]))
	n.add_child(t[2])
	n.add_child(Node(t[3]))
	t[0] = n
	t[0].code = t[2].code
	t[0].place = t[2].place
	t[0].next = t[2].next
	pass

def p_exp_27(t):
	'exp : constant'
	t[0] = t[1]
	global labels, mass
	mass += 1
	labels += 2
	t[0].code = "\n" + str(labels-1) + ": ldc " + t[1].place + "\n" + str(labels) + ": " + t[0].type + "store " + str(mass) + "\n"
	t[0].place = str(mass)
	t[0].next = t[1].next
	pass

def p_exp_28(t):
	'exp : VARIABLE'
	t[0] = Node(t[1])
	t[0].code = ""
	global current_scope
	t[0].place = str(current_scope.variables[t[1]]['mass'])
	pass

def p_exp_29(t):
	'exp : VARIABLE LBIG exp RBIG'
	n = Node('exp29')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	t[0] = n
	global mass, labels, current_scope
	mass += 1
	new_var = str(mass)
	labels += 1
	t[0].code = t[3].code + "\n" + str(labels) + ": aload " + str(current_scope.variables[t[1]]['index']) + "\n" + str(labels+1) + ": iload " + t[3].place + "\n"
	t[0].code += str(labels+2) + ": iaload\n" + str(labels+3) + ": " + t[0].type + "store " + new_var + "\n" 
	labels += 3
	t[0].lastIndex = t[3].place
	t[0].place = new_var
	t[0].var = t[1]
	t[0].array = 1
	pass

def p_exp_30(t):
	'exp : function_call'
	t[0] = t[1]
	t[0].code = t[1].code
	t[0].next = t[1].next
	t[0].place = t[1].place
	pass

def p_unary_expression_1(t):
	'unary_expression : VARIABLE unary_operator'
	n = Node('unary_expression1')
	n.add_child(Node(t[1]))
	n.add_child(t[2])
	t[0] = n
	global labels, mass, current_scope
	labels += 1
	mass += 1
	to_inc = ', 1\n'
	if t[2].place == 'dec':
		to_inc = ', -1\n'
	t[0].code = "\n" + str(labels) + ": iinc " + str(current_scope.variables[t[1]]['mass']) + t[2].code + "\n"
	t[0].code += str(labels+1) + ": " + t[0].type + "load " + str(current_scope.variables[t[1]]['mass']) + "\n"
	t[0].code += str(labels+2) + ": " + t[0].type + "store " + str(mass) + "\n" + str(labels+3) + ": iinc " + str(mass) + to_inc
	labels += 3
	t[0].place = str(mass)
	t[0].next = t[2].next
	pass

def p_unary_expression_2(t):
	'unary_expression : unary_operator VARIABLE'
	n = Node('unary_expression2')
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	t[0] = n
	global labels, mass, current_scope
	labels += 1
	t[0].code = "\n" + str(labels) + ": iinc " + str(current_scope.variables[t[1]]['mass']) + t[2].code + "\n"
	t[0].place = str(current_scope.variables[t[1]]['mass'])
	t[0].next = t[1].next
	pass

def p_unary_expression_3(t):
	'unary_expression : VARIABLE LBIG exp RBIG unary_operator'
	n = Node('unary_expression3')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	t[0] = n
	global labels, mass, current_scope
	labels += 1
	mass += 1
	to_inc = 'add'
	if(t[5].place=='dec'):
		to_inc = 'sub'
	t[0].code = t[3].code + str(labels) + ": aload" + str(current_scope.variables[t[1]]['index']) + "\n"
	t[0].code += str(labels+1) + ": " + t[3].type + "load " + t[3].place + "\n" + str(labels+2) + ": dup2\n" + str(labels+3) + ": " + t[0].type + "aload\n"
	t[0].code += str(labels+4) + ": dup\n"+ str(labels+5) + ": " + t[0].type + "store " + str(mass) + "\n"
	t[0].code += str(labels+6) + ": " + t[0].type + "const_1\n" + str(labels+7) + ": " + t[0].type + to_inc + "\n" + str(labels+8) + ": " + t[0].type + "astore\n"
	labels += 8
	t[0].lastIndex = t[3].place
	t[0].place = str(mass)
	t[0].var = t[1]
	t[0].array = 1
	t[0].next = t[3].next
	pass

def p_unary_expression_4(t):
	'unary_expression : unary_operator VARIABLE LBIG exp RBIG'
	n = Node('unary_expression4')
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(t[4])
	n.add_child(Node(t[5]))
	t[0] = n
	global labels, mass, current_scope
	labels += 1
	mass += 1
	to_inc = 'add'
	if(t[5].place=='dec'):
		to_inc = 'sub'
	t[0].code = t[3].code + str(labels) + ": aload" + str(current_scope.variables[t[1]]['index']) + "\n"
	t[0].code += str(labels+1) + ": " + t[3].type + "load " + t[3].place + "\n" + str(labels+2) + ": dup2\n" + str(labels+3) + ": " + t[0].type + "aload\n"
	t[0].code += str(labels+4) + ": " + t[0].type + "const_1\n" + str(labels+5) + ": " + t[0].type + to_inc + "\n" + str(labels+6) + ": dup\n" + str(labels+7) + ": " + t[0].type + "astore\n"
	t[0].code += str(labels+8) + ": " + t[0].type + "store " + str(mass) + "\n"
	labels += 8
	t[0].lastIndex = t[3].place
	t[0].place = str(mass)
	t[0].var = t[1]
	t[0].array = 1
	t[0].next = t[3].next
	pass

def p_unary_operator_1(t):
	'unary_operator : INCREMENT'
	t[0] = Node(t[1])
	t[0].code = ', 1\n'
	t[0].place = 'inc'
	pass

def p_unary_operator_2(t):
	'unary_operator : DECREMENT'
	t[0] = Node(t[1])
	global labels, mass
	labels += 1
	t[0].code = ', -1\n'
	t[0].place = 'dec'
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
	global labels
	labels += 1
	t[0].code = t[3].code + "\nlabel_" + str(labels) + ":\n"+ t[5].code + "_x = " + t[5].place + ";\n"  + "if _x > 0 goto label_" + str(labels+1) + ";\ngoto " + str(labels+2) + ";\n" 
	labels += 1 
	t[0].code += "\nlabel_" + str(labels) + ":\n"+ t[9].code + "\n" + t[7].code + "\ngoto label_" + str(labels-1) + ";\n" + "\nlabel_" + str(labels+1) + ":\n"
	labels += 1
	t[0].next = t[9].next
	pass

def p_iterative_statement_2(t):
	'iterative_statement : FOR LPAREN iterative_exp SEMI_COLON iterative_exp SEMI_COLON iterative_exp RPAREN lbrace statements rbrace'
	n = Node('iterative_statement2')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(Node(t[6]))
	n.add_child(t[7])
	n.add_child(Node(t[8]))
	n.add_child(t[9])
	n.add_child(t[10])
	n.add_child(t[11])
	t[0] = n
	global labels
	labels += 1
	t[0].code = t[3].code + "\nlabel_" + str(labels) + ":\n" + t[5].code + "_x = " + t[5].place + ";\nif _x > 0 goto label_" + str(labels+1) + ";\ngoto " + str(labels+2) + ";\n" 
	labels += 1
	t[0].code += "\nlabel_" + str(labels) + ":\n"+ t[10].code + "\n" + t[7].code + "\ngoto label_" + str(labels-1) + ";\n" + "\nlabel_" + str(labels+1) + ":\n"
	labels += 1
	t[0].next = t[10].next
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
	global labels
	labels += 1
	t[0].code = t[3].code + "\nlabel_" + str(labels) + ":\n"  + t[5].code + "_x = " + t[5].place + ";" + "\nif _x > 0 goto label_" + str(labels+1) + ";\ngoto " + str(labels+2) + ";\n" 
	labels += 1
	t[0].code += "\nlabel_" + str(labels) + ":\n" + t[7].code + "\ngoto label_" + str(labels-1) + ";\n" + "\nlabel_" + str(labels+1) + ":\n"
	labels += 1
	t[0].next = t[7].next
	pass

def p_iterative_statement_4(t):
	'iterative_statement : FOR LPAREN iterative_exp SEMI_COLON iterative_exp SEMI_COLON iterative_exp RPAREN lbrace rbrace'
	n = Node('iterative_statement4')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(Node(t[6]))
	n.add_child(t[7])
	n.add_child(Node(t[8]))
	n.add_child(t[9])
	n.add_child(t[10])
	t[0] = n
	global labels
	labels += 1
	t[0].code = t[3].code + "\nlabel_" + str(labels) + ":\n" + t[5].code + "_x = " + t[5].place + ";\nif _x > 0 goto label_" + str(labels+1) + ";\ngoto " + str(labels+2) + ";\n" 
	labels += 1
	t[0].code += "\nlabel_" + str(labels) + ":\n" + t[7].code + "\ngoto label_" + str(labels-1) + ";\n"+ "\nlabel_" + str(labels+1) + ":\n"
	labels += 1
	t[0].next = t[7].next
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
	global labels
	labels += 1
	t[0].code = "\nlabel_" + str(labels) + ":\n" + t[3].code + "_x = " + t[3].place + ";\n if _x > 0 goto label_" + str(labels+1) + ";\ngoto label_" + str(labels+2) + ";\n"
	labels += 1
	t[0].code += "\nlabel_" + str(labels) + ":\n" + t[5].code + "\ngoto label_" + str(labels-1) + ";\n" + "\nlabel_" + str(labels+1) + ":\n"
	labels += 1
	t[0].next = t[5].next
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
	global labels
	labels += 1
	t[0].code = "\nlabel_" + str(labels) +":" + t[3].code + "_x = " + t[3].place + ";\n" + "\nif _x > 0 goto label_" 
	t[0].code += str(labels) + ";\ngoto  label_" + str(labels+1) +";\nlabel_" + str(labels+1) + ":\n"
	labels += 1
	t[0].next = t[3].next
	pass

def p_iterative_statement_7(t):
	'iterative_statement : WHILE LPAREN exp RPAREN lbrace statements rbrace'
	n = Node('iterative_statement7')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(t[6])
	n.add_child(t[7])
	t[0] = n
	global labels
	labels += 1
	t[0].code = "\nlabel_" + str(labels) +":" + t[3].code + "_x = " + t[3].place + ";\nif _x > 0 goto label_" + str(labels+1) + ";\ngoto label_" + str(labels+2) + ";\n"
	labels += 1
	t[0].code += "\nlabel_" + str(labels) + ":\n" + t[6].code + "\ngoto label_" + str(labels-1) + ";\n" + "\nlabel_" + str(labels+1) + ":\n"
	labels += 1
	t[0].next = t[6].next
	pass

def p_iterative_statement_8(t):
	'iterative_statement : WHILE LPAREN exp RPAREN lbrace rbrace'
	n = Node('iterative_statement8')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(t[6])
	t[0] = n
	global labels
	labels += 1 
	t[0].code = "\nlabel_" + str(labels) + ":" + t[3].code + "_x = " + t[3].place + ";\n" + "\nif _x > 0 goto label_"
	t[0].code += str(labels) + ";\ngoto  label_" + str(labels+1) +";\nlabel_" + str(labels+1) + ":\n"
	labels += 1
	t[0].next = t[3].next
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
	global labels
	labels += 1 
	t[0].code = "\nlabel_" + str(labels) + ":\n" + t[2].code + t[5].code + "_x = " + t[5].place + ";\nif _x > 0 goto label_" 
	t[0].code += str(labels) + ";\ngoto  label_" + str(labels+1) +";\nlabel_" + str(labels+1) + ":\n"
	labels += 1
	t[0].next = t[5].next
	pass

def p_iterative_statement_10(t):
	'iterative_statement : DO lbrace statements rbrace WHILE LPAREN exp RPAREN SEMI_COLON'
	n = Node('iterative_statement10')
	n.add_child(Node(t[1]))
	n.add_child(t[2])
	n.add_child(t[3])
	n.add_child(t[4])
	n.add_child(Node(t[5]))
	n.add_child(Node(t[6]))
	n.add_child(t[7])
	n.add_child(Node(t[8]))
	n.add_child(Node(t[9]))
	t[0] = n
	global labels
	labels += 1
	t[0].code = "\nlabel_" + str(labels) + ":\n" + t[3].code + t[7].code + "_x = " + t[7].place +";\nif _x > 0 goto label_"
	t[0].code += str(labels) + ";\ngoto  label_" + str(labels+1) +";\nlabel_" + str(labels+1) + ":\n"
	labels += 1
	t[0].next = t[7].next
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
	global labels
	labels += 1
	t[0].code = "\nlabel_" + str(labels) + ":"+ t[5].code + "_x = " + t[5].place + ";\n" + "if _x > 0 goto label_"
	t[0].code += str(labels) + ";\ngoto  label_" + str(labels+1) +";\nlabel_" + str(labels+1) + ":\n"
	labels += 1
	t[0].next = t[5].next
	pass

def p_iterative_statement_12(t):
	'iterative_statement : DO lbrace rbrace WHILE LPAREN exp RPAREN SEMI_COLON'
	n = Node('iterative_statement12')
	n.add_child(Node(t[1]))
	n.add_child(t[2])
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(Node(t[5]))
	n.add_child(t[6])
	n.add_child(Node(t[7]))
	n.add_child(Node(t[8]))
	t[0] = n
	global labels
	labels += 1
	t[0].code = "\nlabel_" + str(labels) + ":"+ t[6].code + "_x = " + t[6].place + ";\n" + "if _x > 0 goto label_"
	t[0].code += str(labels) + ";\ngoto label_" + str(labels+1) +";\nlabel_" + str(labels+1) + ":\n"
	labels += 1
	t[0].next = t[6].next
	pass

def p_iterative_exp_1(t):
	'iterative_exp : exp COMMA iterative_exp'
	n = Node('iterative_exp1')
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	t[0] = n
	t[0].code = t[1].code + ";\n" + t[3].code + ";\n"
	t[0].next = t[3].next
	pass

def p_iterative_exp_2(t):
	'iterative_exp : exp'
	t[0] = t[1]
	t[0].code = t[1].code
	t[0].next = t[1].next
	t[0].place = t[1].place
	pass


def p_conditional_statement_1(t):
	'conditional_statement : IF LPAREN exp RPAREN statement %prec UELSE'
	n = Node('conditional_statement1')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	t[0] = n
	global labels
	labels += 1
	t[0].code = t[3].code + "_x = " + str(t[3].place) + ";\n"
	t[0].code += "\nif _x > 0 goto label_" + str(labels) + ";\ngoto label_" + str(labels+1) +";\n"
	t[0].code += "\nlabel_" + str(labels) + ":\n" + t[5].code + "\nlabel_" + str(labels+1) + ":\n"
	labels += 1
	t[0].next = 'label_' + str(labels)
	pass

def p_conditional_statement_2(t):
	'conditional_statement : IF LPAREN exp RPAREN lbrace statements rbrace %prec UELSE'
	n = Node('conditional_statement2') 
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(t[6])
	n.add_child(t[7])
	t[0] = n
	global labels
	labels += 1
	t[0].code = t[3].code + "_x = " + str(t[3].place) + ";\n"
	t[0].code += "\nif _x > 0 goto label_" + str(labels) + ";\ngoto label_" + str(labels+1) +";\n"
	t[0].code += "\nlabel_" + str(labels) + ":\n" + t[6].code + "\nlabel_"+ str(labels+1) + ":\n"
	labels += 1
	t[0].next = 'label_' + str(labels)
	pass

def p_conditional_statement_3(t):
	'conditional_statement : IF LPAREN exp RPAREN statement ELSE statement'
	n = Node('conditional_statement3')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(Node(t[6]))
	n.add_child(t[7])
	t[0] = n
	global labels
	labels += 1
	t[0].code = t[3].code + "_x = " + str(t[3].place) + ";\n"
	t[0].code += "if _x > 0 goto label_" + str(labels) + ";\n" + t[7].code + "\ngoto label_" + str(labels+1) +";\n"
	t[0].code += "\nlabel_" + str(labels) + ":\n" + t[5].code + "\nlabel_" + str(labels+1) + ":\n"
	labels += 1
	t[0].next = 'label_' + str(labels)
	pass

def p_conditional_statement_4(t):
	'conditional_statement : IF LPAREN exp RPAREN lbrace statements rbrace ELSE statement'
	n = Node('conditional_statement4')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(t[6])
	n.add_child(t[7])
	n.add_child(Node(t[8]))
	n.add_child(t[9])
	t[0] = n
	global labels
	labels += 1
	t[0].code = t[3].code + "_x = " + str(t[3].place) + ";\n"
	t[0].code += "if _x > 0 goto label_" + str(labels) + ";\n" + t[9].code + "goto label_" + str(labels+1) + ";\n"
	t[0].code += "\nlabel_" + str(labels) + ":\n" + t[6].code + "\n" + "label_" + str(labels+1) + ":\n"
	labels += 1
	t[0].next = 'label_' + str(labels)
	pass

def p_conditional_statement_5(t):
	'conditional_statement : IF LPAREN exp RPAREN statement ELSE lbrace statements rbrace'
	n = Node('conditional_statement5')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(Node(t[6]))
	n.add_child(t[7])
	n.add_child(t[8])
	n.add_child(t[9])
	t[0] = n
	global labels
	labels += 1
	t[0].code = t[3].code + "_x = " + str(t[3].place) + ";\n"
	t[0].code += "if _x > 0 goto label_" + str(labels) + ";\n" + t[8].code + "\ngoto label_" + str(labels+1) + ";\n"
	t[0].code += "\nlabel_" + str(labels) + ":\n" + t[5].code + "\nlabel_" + str(labels+1) + ":\n"
	labels += 1
	t[0].next = 'label_' + str(labels)
	pass

def p_conditional_statement_6(t):
	'conditional_statement : IF LPAREN exp RPAREN lbrace statements rbrace ELSE lbrace statements rbrace'
	n = Node('conditional_statement6')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(Node(t[5]))
	n.add_child(t[6])
	n.add_child(Node(t[7]))
	n.add_child(Node(t[8]))
	n.add_child(t[9])
	n.add_child(t[10])
	n.add_child(t[11])
	t[0] = n
	global labels
	labels += 1
	t[0].code = t[3].code + "_x = " + t[3].place + ";\n"
	t[0].code += "if _x > 0 goto label_" + str(labels) + ";\n" + t[10].code + "\ngoto label_" + str(labels+1) +";\n"
	t[0].code += "\nlabel_" + str(labels) + ":\n" + t[6].code + "\nlabel_" + str(labels+1) + ":\n"
	labels += 1
	t[0].next = 'label_' + str(labels)
	pass

def p_function_1(t):
	'function : normal_function'
	t[0] = t[1]
	t[0].code = t[1].code +"\n"
	t[0].next = t[1].next
	pass

def p_function_2(t):
	'function : main_function'
	t[0] = t[1]
	t[0].code = t[1].code + "\n"
	t[0].next = t[1].next
	pass

def p_main_function_1(t):
	'main_function : type MAIN LPAREN parameters RPAREN lbrace statements rbrace'
	n = Node('main_function1')
	global global_scope, current_scope, errors
	if not (global_scope == current_scope):
		errors += 1
		print "Error : line", t.lexer.lineno,": Function", t[2], "cannot be declared here."
	else:
		new_var = current_scope.add_variable(t[2], t[1] ,-1, 1)
		if(not new_var):
			errors += 1
			print "Error : line", t.lexer.lineno,": Function", t[2], "declared multiple times."
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(t[4])
	n.add_child(Node(t[5]))
	n.add_child(t[6])
	n.add_child(t[7])
	n.add_child(t[8])
	t[0] = n
	t[0].code = "\n main:\n" + t[4].code + "\n" + t[7].code + "\nreturn;\n\n"
	t[0].next = t[7].next
	pass

def p_main_function_2(t):
	'main_function : type MAIN LPAREN parameters RPAREN lbrace rbrace'
	n = Node('main_function2')
	global global_scope, current_scope, errors
	if not (global_scope == current_scope):
		errors += 1
		print "Error : line", t.lexer.lineno,": Function", t[2], "cannot be declared here."
	else:
		new_var = current_scope.add_variable(t[2], t[1].data,-1, 1)
		if(not new_var):
			errors += 1
			print "Error : line", t.lexer.lineno,": Function", t[2], "declared multiple times."
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(t[4])
	n.add_child(Node(t[5]))
	n.add_child(t[6])
	n.add_child(t[7])
	t[0] = n
	t[0].code = "\n main:\nreturn;\n\n"
	t[0].next = t[7].next
	pass

def p_main_function_3(t):
	'main_function : MAIN LPAREN parameters RPAREN lbrace statements rbrace'
	n = Node('main_function3')
	global global_scope, current_scope, errors
	if not (global_scope == current_scope):
		errors += 1
		print "Error : line", t.lexer.lineno,": Function", t[1], "cannot be declared here."
	else:
		new_var = current_scope.add_variable(t[1], 'void', -1, 1)
		if(not new_var):
			errors += 1
			print "Error : line", t.lexer.lineno,": Function", t[1], "declared multiple times."
	n.add_child(Node("VOID"))
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(t[6])
	n.add_child(t[7])
	t[0] = n
	t[0].code = "\n main:\n" + t[3].code + "\n" + t[6].code + "\nreturn;\n\n"
	t[0].next = t[6].next
	pass

def p_main_function_4(t):
	'main_function : MAIN LPAREN parameters RPAREN lbrace rbrace'
	n = Node('main_function4')
	global global_scope, current_scope, errors
	if not (global_scope == current_scope):
		errors += 1
		print "Error : line", t.lexer.lineno,": Function", t[1], "cannot be declared here."
	else:
		new_var = current_scope.add_variable(t[1], 'void',-1, 1)
		if(not new_var):
			errors += 1
			print "Error : line", t.lexer.lineno,": Function", t[1], "declared multiple times."
	n.add_child(Node("VOID"))
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(t[6])
	t[0] = n
	t[0].code = "\n main:\nreturn;\n\n"
	t[0].next = t[1].next
	pass

def p_main_function_5(t):
	'main_function : type MAIN LPAREN RPAREN lbrace statements rbrace'
	n = Node('main_function5')
	global global_scope, current_scope, errors
	if not (global_scope == current_scope):
		errors += 1
		print "Error : line", t.lexer.lineno,": Function", t[2], "cannot be declared here."
	else:
		new_var = current_scope.add_variable(t[2], t[1].data,-1, 1)
		if(not new_var):
			errors += 1
			print "Error : line", t.lexer.lineno,": Function", t[2], "declared multiple times."
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(t[6])
	n.add_child(t[7])
	t[0] = n
	t[0].code = "\n main:\n" + t[6].code + "\nreturn;\n\n"
	t[0].next = t[6].next
	pass

def p_main_function_6(t):
	'main_function : type MAIN LPAREN RPAREN lbrace rbrace'
	n = Node('main_function6')
	global global_scope, current_scope, errors
	if not (global_scope == current_scope):
		errors += 1
		print "Error : line", t.lexer.lineno,": Function", t[2], "cannot be declared here."
	else:
		new_var = current_scope.add_variable(t[2], t[1].data,-1, 1)
		if(not new_var):
			errors += 1
			print "Error : line", t.lexer.lineno,": Function", t[2], "declared multiple times."
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(t[6])
	t[0] = n
	t[0].code = "\n main:\nreturn;\n\n"
	t[0].next = t[6].next
	pass

def p_main_function_7(t):
	'main_function : MAIN LPAREN RPAREN lbrace statements rbrace'
	n = Node('main_function7')
	global global_scope, current_scope, errors
	if not (global_scope == current_scope):
		errors += 1
		print "Error : line", t.lexer.lineno,": Function", t[1], "cannot be declared here."
	else:
		new_var = current_scope.add_variable(t[1], 'void',-1, 1)
		if(not new_var):
			errors += 1
			print "Error : line", t.lexer.lineno,": Function", t[1], "declared multiple times."
	n.add_child(Node("VOID"))
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(t[4])
	n.add_child(t[5])
	n.add_child(t[6])
	t[0] = n
	t[0].code = "\n main:\n" + t[5].code + "\nreturn;\n\n"
	t[0].next = t[5].next
	pass

def p_main_function_8(t):
	'main_function : MAIN LPAREN RPAREN lbrace rbrace'
	n = Node('main_function8')
	global global_scope, current_scope, errors
	if not (global_scope == current_scope):
		errors += 1
		print "Error : line", t.lexer.lineno,": Function", t[1], "cannot be declared here."
	else:
		new_var = current_scope.add_variable(t[1], 'void',-1, 1)
		if(not new_var):
			errors += 1
			print "Error : line", t.lexer.lineno,": Function", t[1], "declared multiple times."
	n.add_child(Node("VOID"))
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(t[4])
	n.add_child(t[5])
	t[0] = n
	t[0].code = "\n main:\nreturn;\n\n"
	t[0].next = t[5].next
	pass


def p_normal_function_1(t):
	'normal_function : type VARIABLE LPAREN parameters RPAREN lbrace statements rbrace'
	n = Node('normal_function1')
	global global_scope, current_scope, errors
	if not (global_scope == current_scope):
		errors += 1
		print "Error : line", t.lexer.lineno,": Function", t[2], "cannot be declared here."
	else:
		new_var = current_scope.add_variable(t[2], t[1].data,-1, 1)
		if(not new_var):
			errors += 1
			print "Error : line", t.lexer.lineno,": Function", t[2], "declared multiple times."
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(t[4])
	n.add_child(Node(t[5]))
	n.add_child(t[6])
	n.add_child(t[7])
	n.add_child(t[8])
	t[0] = n
	t[0].code = "\n" + t[2] + "_begin:" + t[4].code + "\n" + t[4].code + "\n" + t[7].code + "\nreturn;\n\n"
	t[0].next = t[7].next
	pass

def p_normal_function_2(t):
	'normal_function : type VARIABLE LPAREN parameters RPAREN lbrace rbrace'
	n = Node('normal_function2')
	global global_scope, current_scope, errors
	if not (global_scope == current_scope):
		errors += 1
		print "Error : line", t.lexer.lineno,": Function", t[2], "cannot be declared here."
	else:
		new_var = current_scope.add_variable(t[2], t[1].data,-1, 1)
		if(not new_var):
			errors += 1
			print "Error : line", t.lexer.lineno,": Function", t[2], "declared multiple times."
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(t[4])
	n.add_child(Node(t[5]))
	n.add_child(t[6])
	n.add_child(t[7])
	t[0] = n
	t[0].code = "\n" + t[2] + "_begin:" + t[4].code + "\nreturn;\n\n"
	t[0].next = t[7].next
	pass

def p_normal_function_3(t):
	'normal_function : VARIABLE LPAREN parameters RPAREN lbrace statements rbrace'
	n = Node('normal_function3')
	global global_scope, current_scope, errors
	if not (global_scope == current_scope):
		errors += 1
		print "Error : line", t.lexer.lineno, ": Function", t[1], "cannot be declared here."
	else:
		new_var = current_scope.add_variable(t[1], 'void',-1, 1)
		if(not new_var):
			errors += 1
			print "Error : line", t.lexer.lineno, ": Function", t[1], "declared multiple times."
	n.add_child(Node("VOID"))
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(t[6])
	n.add_child(t[7])
	t[0] = n
	t[0].code = "\n" + t[1] + "_begin:" + t[3].code + "\n" + t[6].code + "\nreturn;\n\n"
	t[0].next = t[6].next
	pass

def p_normal_function_4(t):
	'normal_function : VARIABLE LPAREN parameters RPAREN lbrace rbrace'
	n = Node('normal_function4')
	global global_scope, current_scope, errors
	if not (global_scope == current_scope):
		errors += 1
		print "Error : line", t.lexer.lineno, ": Function", t[1], "cannot be declared here."
	else:
		new_var = current_scope.add_variable(t[1], 'void',-1, 1)
		if(not new_var):
			errors += 1
			print "Error : line", t.lexer.lineno, ": Function", t[1], "declared multiple times."
	n.add_child(Node("VOID"))
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(t[6])
	t[0] = n
	t[0].code = "\n" + t[1] + "_begin:" + t[3].code + "\nreturn;\n\n"
	t[0].next = t[6].next
	pass

def p_normal_function_5(t):
	'normal_function : type VARIABLE LPAREN RPAREN lbrace statements rbrace'
	n = Node('normal_function5')
	global global_scope, current_scope, errors
	if not (global_scope == current_scope):
		errors += 1
		print "Error : line", t.lexer.lineno, ": Function", t[2], "cannot be declared here."
	else:
		new_var = current_scope.add_variable(t[2], t[1].data,-1, 1)
		if(not new_var):
			errors += 1
			print "Error : line", t.lexer.lineno, ": Function", t[2], "declared multiple times."
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(t[6])
	n.add_child(t[7])
	t[0] = n
	t[0].code = "\n" + t[2] + "_begin:\n" + t[6].code + "\nreturn;\n\n"
	t[0].next = t[6].next
	pass

def p_normal_function_6(t):
	'normal_function : type VARIABLE LPAREN RPAREN lbrace rbrace'
	n = Node('normal_function6')
	global global_scope, current_scope, errors
	if not (global_scope == current_scope):
		errors += 1
		print "Error : line", t.lexer.lineno,": Function", t[2], "cannot be declared here."
	else:
		new_var = current_scope.add_variable(t[2], t[1].data,-1, 1)
		if(not new_var):
			errors += 1
			print "Error : line", t.lexer.lineno,": Function", t[2], "declared multiple times."
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(Node(t[4]))
	n.add_child(t[5])
	n.add_child(t[6])
	t[0] = n
	t[0].code = "\n" + t[2] + "_begin:\nreturn;\n\n"
	t[0].next = t[6].next
	pass

def p_normal_function_7(t):
	'normal_function : VARIABLE LPAREN RPAREN lbrace statements rbrace'
	n = Node('normal_function7')
	global global_scope, current_scope, errors
	if not (global_scope == current_scope):
		errors += 1
		print "Error : line", t.lexer.lineno,": Function", t[1], "cannot be declared here."
	else:
		new_var = current_scope.add_variable(t[1], 'void',-1, 1)
		if(not new_var):
			errors += 1
			print "Error : line", t.lexer.lineno,": Function", t[1], "declared multiple times."
	n.add_child(Node("VOID"))
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(t[4])
	n.add_child(t[5])
	n.add_child(t[6])
	t[0] = n
	t[0].code = "\n" + t[1] + "_begin:\n" + t[5].code + "\nreturn;\n\n"
	t[0].next = t[5].next
	pass

def p_normal_function_8(t):
	'normal_function : VARIABLE LPAREN RPAREN lbrace rbrace'
	n = Node('normal_function8')
	global global_scope, current_scope, errors
	if not (global_scope == current_scope):
		errors += 1
		print "Error : line", t.lexer.lineno,": Function", t[1], "cannot be declared here."
	else:
		new_var = current_scope.add_variable(t[1], 'void',-1, 1)
		if(not new_var):
			errors += 1
			print "Error : line", t.lexer.lineno,": Function", t[1], "declared multiple times."
	n.add_child(Node("VOID"))
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(t[4])
	n.add_child(t[5])
	t[0] = n
	t[0].code = "\n" + t[1] + "_begin:\nreturn;\n\n"
	t[0].next = t[5].next
	pass

def p_parameters_1(t):
	'parameters : type VARIABLE COMMA parameters'
	n = Node('parameters1')
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	n.add_child(t[4])
	t[0] = n
	t[0].code = "(" + t[1].place + " " + t[2] + "," + t[4].code + ")"
	pass

def p_parameters_2(t):
	'parameters : type VARIABLE'
	n = Node('parameters2')
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	t[0] = n
	t[0].code = t[1].place + " " + t[2]
	pass

def p_function_call_1(t):
	'function_call : VARIABLE LPAREN arguments RPAREN'
	n = Node('function_call1')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	n.add_child(Node(t[4]))
	t[0] = n
	global mass
	mass += 1
	new_var = "_t" + str(mass)
	t[0].code = t[3].code + "\n" + new_var + " = " + t[1] + "(" + t[3].place + ");" + "\ngoto " + t[1] + "_begin;\n"
	t[0].place = new_var
	pass

def p_function_call_2(t):
	'function_call : VARIABLE LPAREN RPAREN'
	n = Node('function_call2')
	n.add_child(Node(t[1]))
	n.add_child(Node(t[2]))
	n.add_child(Node(t[3]))
	t[0] = n
	global mass
	mass += 1
	new_var = "_t" + str(mass)
	t[0].code = "\n" + new_var + " = " + t[1] + "();" + "\ngoto "+ t[1] + "_begin;\n"
	t[0].place = new_var
	pass

def p_arguments_1(t):
	'arguments : arguments COMMA exp'
	n = Node('arguments1')
	n.add_child(t[1])
	n.add_child(Node(t[2]))
	n.add_child(t[3])
	t[0] = n
	t[0].code = t[1].code + t[3].code
	t[0].place = t[1].place + "," + t[3].place
	pass

def p_arguments_2(t):
	'arguments : exp'
	t[0] = t[1]
	t[0].code = t[1].code
	t[0].place = t[1].place
	t[0].next = t[1].next
	pass

def p_lbrace_1(t):
	'lbrace : LBRACE'
	t[0] = Node(t[1])
	t[0].code = ""
	global current_scope, tableux
	new_scope = Table(tableux)
	tableux += 1
	current_scope.add_table(new_scope)
	current_scope = new_scope
	pass

def p_rbrace_1(t):
	'rbrace : RBRACE'
	t[0] = Node(t[1])
	t[0].code = ""
	global current_scope
	current_scope = current_scope.parent
	pass

def p_empty(t):
	'empty : '
	t[0] = Node('empty')
	pass

def p_error(p):
    print "Error: Syntax error in line", str(p.lineno), ": Unexpected token :", str(p.value)
    yacc.errok()
    global errors
    errors += 1
    pass


def parse():
	print " "
	f = open(sys.argv[1])
	p = yacc.parse(f.read(), debug=0)
	global errors
	if(errors>0):
		print "Compilation failed.", errors, "errors found."

import profile

parser = yacc.yacc()
parse()
