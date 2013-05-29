class Uniform:
	def __init__(self, name, a, b):
		self.name = name
		self.a = a
		self.b = b

	def __repr__(self):
		return '{name} ~ uniform({a}, {b});'.format(name=self.name,
						a=self.a, b=self.b)

	def __str__(self):
		return self.name

	def from_prior(self):
		s = ''
		s += '{name} = {a} + ({b} - {a})*randomU();\n'
		return s.format(name=self.name, a=self.a, b=self.b)		

	def log_likelihood(self):
		s = ''
		s += 'if({name} >= {a} && {name} <= {b})\n'
		s += '\tlogL += -log({b} - {a});\n'
		s += 'else\n'
		s += '\tlogL += -1E300;\n'
		return s.format(name=self.name, a=self.a, b=self.b)

	def proposal(self):
		s = ''
		s += '{name} += ({b} - {a})*pow(10., 1.5 - 6.*randomU())*randn();\n'
		s += '{name} = mod({name} - {a}, {b} - {a}) + {a};\n'
		return s.format(name=self.name, a=self.a, b=self.b)


class Normal:
	def __init__(self, name, mu, sigma):
		self.name = name
		self.mu = mu
		self.sigma = sigma

	def __repr__(self):
		return '{name} ~ normal({mu}, {sigma});'.format(name=self.name,
						mu=self.mu, sigma=self.sigma)

	def __str__(self):
		return self.name

	def from_prior(self):
		s = ''
		s += '{name} = {mu} + {sigma}*randn();\n'
		return s.format(name=self.name,	mu=self.mu, sigma=self.sigma)
	

	def log_likelihood(self):
		s = ''
		s += 'logL += -0.5*log(2.*M_PI) - log({sigma});\n'
		s += 'logL += -0.5*pow(({name} - {mu})/{sigma}, 2);\n'
		return s.format(name=self.name,	mu=self.mu, sigma=self.sigma)

	def proposal(self):
		s = ''
		s += 'logH -= -0.5*pow(({name} - {mu})/{sigma}, 2);\n'
		s += '{name} += {sigma}*pow(10., 1.5 - 6.*randomU())*randn();\n'
		s += 'logH += -0.5*pow(({name} - {mu})/{sigma}, 2);\n'
		return s.format(name=self.name,	mu=self.mu, sigma=self.sigma)


if __name__ == '__main__':
	theta = Uniform('theta', 0., 1.)
	x = Uniform('x', 0., theta)

	print("FROMPRIOR")
	print(theta.from_prior())

	print("PROPOSAL")
	print(theta.proposal())

	print("LOGLIKELIHOOD")
	print(theta.log_likelihood())

	print("\n\n\n")

	print("FROMPRIOR")
	print(x.from_prior())

	print("PROPOSAL")
	print(x.proposal())

	print("LOGLIKELIHOOD")
	print(x.log_likelihood())

