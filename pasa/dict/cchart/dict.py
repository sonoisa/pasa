# -*- coding: utf-8 -*-
from .cchart import Cchart


class Dict(object):
    def __init__(self, yaml):
        self.dict = dict([(c.ctype, c) for c in list(map(lambda c: Cchart(c), yaml['dict']))])

    def get_cchart(self, ctype):
        return self.dict.get(ctype, None)

    def __repr__(self):
        return "{{dict={}}}".format(self.dict)
