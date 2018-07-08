# -*- coding: utf-8 -*-
from .idiom import Idiom


class Dict(object):
    def __init__(self, yaml):
        self.dict = list(map(lambda i: Idiom(i), yaml['dict']))

    def __repr__(self):
        return "{{dict={}}}".format(self.dict)
