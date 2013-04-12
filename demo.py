#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)


from dnc.model import Model
from dnc.distributions import Node, Uniform, LogUniform, Normal, Derived

mu = Uniform("mu", -10., 10.)
sigma = LogUniform("sigma", 1E-3, 1.)
muSq = Derived("muSq", "pow(mu, 2)")
muSq.specify_parents([mu]) # MANUAL ENTRY REQUIRED HERE

x = Normal("x", mu, sigma)
x.observed = 3.141

model = Model("MyModel", Node.universe)
model.save("demo_results")

