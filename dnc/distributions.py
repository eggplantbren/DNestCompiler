#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

__all__ = ["Node", "Uniform", "LogUniform", "Normal", "Derived"]


class Node(object):
    universe = []

    npars = 0
    _ctype = "double"
    _prior = ""
    _proposal = ""
    _logprob = ""
    _center_children = ""
    is_derived = False

    def __init__(self, name, *args):
        self.name = name
        self.pars = args
        assert self.npars == len(args), "Wrong number of parameters."
        self.observed = None
        self.children = []
        for arg in args:
            try:
                arg.children.append(self)
            except AttributeError:
                pass
        Node.universe.append(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        cls = self.__class__.__name__
        args = "".join(["{0}, ".format(p) for p in self.pars])
        args = args[:-2]
        return "<{1} ~ {0}({2})>".format(cls, self.name, args)

    @property
    def prior(self):
        s = ''
        s += self._prior.format(name=self.name, pars=self.pars)
        return s

    @property
    def proposal1(self):
        s = ''
        s += self.center_children
        s += self._proposal.format(name=self.name, pars=self.pars)
        s += self.decenter_children
	return s

    @property
    def proposal2(self):
        s = ''
        s += self.logp_children.replace('logL', 'logP1')
        s += self._proposal.format(name=self.name, pars=self.pars)
        s += self.logp_children.replace('logL', 'logP2')
	return s

    @property
    def logprob(self):
        return self._logprob.format(name=self.name, pars=self.pars)

    @property
    def center_children(self):
        s = ''
        for child in self.children:
            if child.observed is None:
		    s += child._center.format(name=child.name, pars=child.pars)
		    s += child.center_children
        return s

    @property
    def decenter_children(self):
        s = ''
        for child in self.children:
            if child.observed is None:
		    s += child._decenter.format(name=child.name, pars=child.pars)
		    s += child.decenter_children
        return s

    @property
    def logp_children(self):
        s = ''
        for child in self.children:
            if child.observed is None:
		    s += child.logprob.format(name=child.name, pars=child.pars)
        return s

class Uniform(Node):

    npars = 2
    _ctype = "double"
    _prior = "{name} = {pars[0]} + ({pars[1]} - {pars[0]})*randomU();"

    _proposal = """
    {name} += ({pars[1]} - {pars[0]})*pow(10., 1.5 - 6.*randomU())*randn();
    {name} = mod({name} - {pars[0]}, {pars[1]} - {pars[0]}) + {pars[0]};
    """

    _logprob = """
    if ({name} < {pars[0]} || {name} > {pars[1]})
        logL = -1e300;
    else
        logL += -log({pars[1]} - {pars[0]});
    """

    _center = """
    {name} = ({name} - {pars[0]})/({pars[1]} - {pars[0]});
    """

    _decenter = """
    {name} = {pars[0]} + ({pars[1]} - {pars[0]})*{name};
    """

class LogUniform(Node):

    npars = 2
    _ctype = "double"
    _prior = "{name} = exp(log({pars[0]}) + log({pars[1]}/{pars[0]})*randomU());"

    _proposal = """
    {name} = log({name});
    {name} += log({pars[1]}/{pars[0]})*pow(10., 1.5 - 6.*randomU())*randn();
    {name} = mod({name} - log({pars[0]}), log({pars[1]}/{pars[0]})) + log({pars[0]});
    {name} = exp({name});
    """

    _logprob = """
    if ({name} < log({pars[0]}) || {name} > log({pars[1]}))
        logL = -1e300;
    else
        logL += -log({name}) - log({pars[1]}/{pars[0]});
    """

    _center = """
    {name} = log({name})
    {name} = ({name} - log({pars[0]}))/(log({pars[1]}/{pars[0]}));
    """

    _decenter = """
    {name} = log({pars[0]}) + log({pars[1]}/{pars[0]})*{name};
    """


class Normal(Node):

    npars = 2
    _ctype = "double"
    _prior = "{name} = {pars[0]} + {pars[1]}*randn();"

    _proposal = """
    double _dnc_{name} = ({name} - {pars[0]})/{pars[1]};
    logH -= -0.5*pow(_dnc_{name}, 2);
    _dnc_{name} += {pars[1]}*pow(10., 1.5 - 6.*randomU())*randn();
    logH += -0.5* pow(_dnc_{name}, 2);
    {name} = {pars[0]} + {pars[1]}*_dnc_{name};
    """

    _logprob = """
    logL += -0.5*log(2*M_PI) - log({pars[1]}) - 0.5*pow(({name} - {pars[0]})/{pars[1]}, 2);
    """

    _center = """
    {name} = ({name} - {pars[0]})/{pars[1]};
    """

    _decenter = """
    {name} = {pars[0]} + {pars[1]}*{name};
    """

class Derived(Node):
    npars = 1
    _ctype = "double"
    _prior = "{name} = {pars[0]};"
    is_derived = True

    _center = ""
    _decenter = _prior

    def specify_parents(self, parents):
        for p in parents:
            p.children.append(self)


