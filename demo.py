#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)


from dnc.model import Model
from dnc.distributions import Uniform, Normal, Deterministic

theta = Uniform("theta", 0., 1.)
theta2 = Deterministic("theta2", "pow(theta, 2)")
x = Normal("x", theta2, 0.5)

model = Model("MyModel", [theta, theta2, x])
print(model.header)
print()
print(model.implementation)
