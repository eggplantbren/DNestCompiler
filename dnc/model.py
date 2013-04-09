#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

__all__ = ["Model"]


import os
from jinja2 import Template
from .distributions import Derived

_template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "templates")
_header_template = Template(open(os.path.join(_template_dir,
                                              "header.h")).read())
_implementation_template = Template(open(os.path.join(_template_dir,
                                                      "implementation.cpp"))
                                    .read())

class Model(object):

    def __init__(self, name, nodes):
        self.name = name
        self.derived = [node for node in nodes if isinstance(node, Derived)]
	self.params =  [node for node in nodes if not isinstance(node, Derived) and node.observed is None]
        self.data = [node for node in nodes if not isinstance(node, Derived) and node.observed is not None]
	self.npar = len(self.params)

    @property
    def header(self):
        return _header_template.render(name=self.name, params=self.params,
                                          derived=self.derived, data=self.data, npar=self.npar)

    @property
    def implementation(self):
        return _implementation_template.render(name=self.name, params=self.params,
                                          derived=self.derived, data=self.data, npar=self.npar)

    def save(self, basepath=".", clobber=True):
        try:
            os.makedirs(basepath)
        except os.error:
            if clobber:
                print("Overwriting existing model.")
            else:
                raise

        fn = os.path.join(basepath, "{0}.h".format(self.name))
        print("Writing header to: {0}".format(fn))
        with open(fn, "w") as f:
            f.write(self.header)

        fn = os.path.join(basepath, "{0}.cpp".format(self.name))
        print("Writing implementation to: {0}".format(fn))
        with open(fn, "w") as f:
            f.write(self.implementation)
