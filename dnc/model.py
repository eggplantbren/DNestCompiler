#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

__all__ = ["Model"]


import os
from jinja2 import Template


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
        self.nodes = nodes

    @property
    def header(self):
        return _header_template.render(name=self.name, nodes=self.nodes)

    @property
    def implementation(self):
        return _implementation_template.render(name=self.name,
                                               nodes=self.nodes)
