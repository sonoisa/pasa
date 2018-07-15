# -*- coding: utf-8 -*-
from .filter import Filter


class Dict(object):
    def __init__(self, yaml):
        self.dict = list(map(lambda f: Filter(f), yaml['dict']))

    def get_filter(self, entry):
        for f in self.dict:
            if entry == f.entry:
                return f
        return None

    def __repr__(self):
        return "{{dict={}}}".format(self.dict)
