# -*- coding: utf-8 -*-

from pasa.utils import getOrElse


class Case(object):
    def __init__(self, yaml):
        self.noun = getOrElse(yaml, 'noun', "")
        self.part = getOrElse(yaml, 'part', "")
        self.category = getOrElse(yaml, 'category', "")
        self.semrole = getOrElse(yaml, 'semrole', "")
        self.arg = getOrElse(yaml, 'arg', "")

    def __repr__(self):
        return "{{noun={}, part={}, category={}, semrole={}, arg={}}}".format(self.noun, self.part, self.category, self.semrole, self.arg)
