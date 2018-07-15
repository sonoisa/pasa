# -*- coding: utf-8 -*-
from .frame import Frame


class Dict(object):
    def __init__(self, yaml):
        self.dict = dict([(f.verb, f) for f in list(map(lambda f: Frame(f), yaml['dict']))])

    def get_frame(self, verb):
        return self.dict.get(verb, None)

    def is_frame(self, verb):
        return self.dict.get(verb, None) is not None

    def __repr__(self):
        return "{{dict={}}}".format(self.dict)
