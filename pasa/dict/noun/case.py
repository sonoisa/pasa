# -*- coding: utf-8 -*-

from pasa.utils import get_or_else


class Case(object):
    def __init__(self, yaml):
        self.noun = get_or_else(yaml, 'noun', "")
        self.part = get_or_else(yaml, 'part', "")
        self.category = get_or_else(yaml, 'category', "")
        self.semrole = get_or_else(yaml, 'semrole', "")
        self.arg = get_or_else(yaml, 'arg', "")

    def __repr__(self):
        return "{{noun={}, part={}, category={}, semrole={}, arg={}}}".format(self.noun, self.part, self.category, self.semrole, self.arg)
