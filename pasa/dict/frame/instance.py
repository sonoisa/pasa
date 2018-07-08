# -*- coding: utf-8 -*-
from .case import Case

from pasa.utils import getOrElse


class Instance(object):
    def __init__(self, yaml):
        self.cases = list(map(lambda c: Case(c), getOrElse(yaml, 'cases', [])))

    def __repr__(self):
        return "{{cases={}}}".format(self.cases)
