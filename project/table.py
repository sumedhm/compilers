import sys

class Table(object):
	def __init__(self, data):
		self.data = data
		self.parent = None
		self.child_tables = []
		self.variables = {}

	def add_table(self, obj):
		self.child_tables.append(obj)
		obj.parent = self

	def add_variable(self, obj, setType):
		if obj in self.variables:
			return False
		else:
			self.variables[obj] = {}
			self.variables[obj]['type'] = setType
			self.variables[obj]['size'] = 0
			return True

def print_table(obj):
	print "\nPrinting table", obj.data
	print "Children: ",
	for i in obj.child_tables:
		print i.data,
	print " "
	for j in obj.variables:
		print j, ':', obj.variables[j]
	for i in obj.child_tables:
		print_table(i)

i = 0
global_scope = Table('global')
i = i+1
global_scope.add_variable('a', 'int')
global_scope.add_variable('b', 'int')
current_scope = global_scope
new_scope = Table(i)
i += 1
current_scope.add_table(new_scope)
current_scope = new_scope
current_scope.add_variable('ab', 'char')
current_scope.add_variable('a', 'char')
new_scope = Table(i)
i += 1
current_scope.add_table(new_scope)
current_scope = new_scope
x = current_scope.add_variable('ab', 'char')
if(not x):
	print "Adding variable failed1"
x = current_scope.add_variable('ab', 'char')
if(not x):
	print "Adding variable failed2"
table = global_scope
print_table(table)