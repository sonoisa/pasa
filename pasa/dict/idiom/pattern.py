# -*- coding: utf-8 -*-
from .case import Case

from pasa.utils import getOrElse


class Pattern(object):
    def __init__(self, yaml):
        self.entry = getOrElse(yaml, 'entry', "")
        self.cases = list(map(lambda c: Case(c), getOrElse(yaml, 'cases', [])))

    def __repr__(self):
        return "{{entry={}, cases={}}}".format(self.entry, self.cases)
