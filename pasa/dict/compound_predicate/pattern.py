# -*- coding: utf-8 -*-
from .case import Case

from pasa.utils import get_or_else


class Pattern(object):
    def __init__(self, yaml):
        self.entry = get_or_else(yaml, 'entry', "")
        self.cases = list(map(lambda c: Case(c), get_or_else(yaml, 'cases', [])))

    def __repr__(self):
        return "{{entry={}, cases={}}}".format(self.entry, self.cases)
