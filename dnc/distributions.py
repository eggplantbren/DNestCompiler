#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

__all__ = ["Distribution", "Uniform", "Normal"]


class Distribution(object):

    npars = 0

    def __init__(self, name, *args):
        self.name = name
        self.pars = args
        assert self.npars == len(args), "Wrong number of parameters."

    def __str__(self):
        return self.name

    def __repr__(self):
        cls = self.__class__.__name__
        args = "".join([", {0}".format(p) for p in self.pars])
        return "<{0}({1}{2})>".format(cls, self.name, args)

    @property
    def prior(self):
        return self._prior.format(name=self.name, pars=self.pars)

    @property
    def proposal(self):
        return self._proposal.format(name=self.name, pars=self.pars)


class Uniform(Distribution):

    npars = 2
    _prior = "{name} = {pars[0]} + ({pars[1]} - {pars[0]}) * randomU();"
    _proposal = """
    {name} += ({pars[1]} - {pars[0]}) * pow(10., 1.5-6.*randomU()) * randn();
    {name} = mod({name} - {pars[0]}, {pars[1]} - {pars[0]});
    """


class Normal(Distribution):

    npars = 2
    _prior = "{name} = {pars[0]} + {pars[1]} * randn();"
    _proposal = """
    double _dnc_{name} = ({name} - {pars[0]}) / {pars[1]};
    logH += 0.5 * pow(_dnc_{name}, 2);
    _dnc_{name} += {pars[1]} * pow(10., 1.5-6.*randomU()) * randn();
    logH -= 0.5 * pow(_dnc_{name}, 2);
    {name} = {pars[0]} + {pars[1]} * _dnc_{name};
    """


if __name__ == "__main__":
    theta = Uniform("theta", 0, 1)
    x = Normal("x", theta, 1.5)
