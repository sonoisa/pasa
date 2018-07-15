# -*- coding: utf-8 -*-
from .filter import Filter


class Dict(object):
    def __init__(self, yaml):
        self.dict = dict([(f.entry, f) for f in list(map(lambda f: Filter(f), yaml['dict']))])

    def get_filter(self, entry):
        return self.dict.get(entry, None)

    def __repr__(self):
        return "{{dict={}}}".format(self.dict)
