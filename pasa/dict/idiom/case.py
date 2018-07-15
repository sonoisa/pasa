# -*- coding: utf-8 -*-

from pasa.utils import get_or_else


class Case(object):
    def __init__(self, yaml):
        self.base = get_or_else(yaml, 'base', "")
        self.read = get_or_else(yaml, 'read', "")
        self.pos = get_or_else(yaml, 'pos', "")

    def __repr__(self):
        return "{{base={}, read={}, pos={}}}".format(self.base, self.read, self.pos)
