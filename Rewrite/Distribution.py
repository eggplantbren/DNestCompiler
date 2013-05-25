class Uniform:
	def __init__(self, a, b):
		self.a = a
		self.b = b

	def __str__(self):
		return 'uniform(' + str(self.a) + ', ' + str(self.b) + ')'

	def from_prior(self, x):
		s = ''
		s += '{x} = {a} + ({b} - {a})*randomU();\n'
		return s.format(x=x, a=self.a, b=self.b)		

	def log_density(self, x):
		s = ''
		s += 'if({x} >= {a} && {x} <= {b})\n'
		s += '\tlogP += -log({b} - {a});\n'
		s += 'else\n'
		s += '\tlogP += -1E300;\n'
		return s.format(x=x, a=self.a, b=self.b)

	def proposal(self, x):
		s = ''
		s += '{x} += ({b} - {a})*pow(10., 1.5 - 6.*randomU())*randn();\n'
		s += '{x} = mod({x} - {a}, {b} - {a}) + {a};\n'
		return s.format(x=x, a=self.a, b=self.b)


