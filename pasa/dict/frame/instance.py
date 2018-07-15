# -*- coding: utf-8 -*-
from .case import Case

from pasa.utils import get_or_else


class Instance(object):
    def __init__(self, yaml):
        self.cases = list(map(lambda c: Case(c), get_or_else(yaml, 'cases', [])))

    def __repr__(self):
        return "{{cases={}}}".format(self.cases)
