# -*- coding: utf-8 -*-
from .cchart import Cchart


class Dict(object):
    def __init__(self, yaml):
        self.dict = list(map(lambda c: Cchart(c), yaml['dict']))

    def get_cchart(self, ctype):
        for cchart in self.dict:
            if ctype == cchart.ctype:
                return cchart
        return None

    def __repr__(self):
        return "{{dict={}}}".format(self.dict)
