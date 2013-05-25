class Node:
	def __init__(self, name, distribution, observed=None):
		"""
		Inputs are the name of the variable
		and its prior distribution which may
		depend on other variables. Also, the
		observed value, which defaults to `None`.
		"""
		self.name = name
		self.distribution = distribution
		self.observed = None

	def from_prior(self):
		return self.distribution.from_prior(self.name)

	def proposal(self):
		return self.distribution.proposal(self.name)

	def log_likelihood(self):
		return self.distribution.log_density(self.name).replace('logH',
							'logL')
	def __str__(self):
		return self.name

if __name__ == '__main__':
	from Distribution import Uniform

	n1 = Node(name='theta', distribution=Uniform(0., 1.))
	n2 = Node(name='x', distribution=Uniform(0., n1))

	print("FROMPRIOR")
	print(n2.from_prior())

	print("PROPOSAL")
	print(n2.proposal())


