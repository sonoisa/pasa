# -*- coding: utf-8 -*-

from pasa.utils import getOrElse


class Case(object):
    def __init__(self, yaml):
        self.base = getOrElse(yaml, 'base', "")
        self.read = getOrElse(yaml, 'read', "")
        self.pos = getOrElse(yaml, 'pos', "")

    def __repr__(self):
        return "{{base={}, read={}, pos={}}}".format(self.base, self.read, self.pos)
