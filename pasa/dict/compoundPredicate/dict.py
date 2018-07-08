# -*- coding: utf-8 -*-
from .compound_predicate import CompoundPredicate


class Dict(object):
    def __init__(self, yaml):
        self.dict = list(map(lambda i: CompoundPredicate(i), yaml['dict']))

    def __repr__(self):
        return "{{dict={}}}".format(self.dict)
