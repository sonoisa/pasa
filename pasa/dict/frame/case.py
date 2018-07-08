# -*- coding: utf-8 -*-

from pasa.utils import getOrElse


class Case(object):
    def __init__(self, yaml):
        self.part = getOrElse(yaml, 'part', "")
        self.causative_part = getOrElse(yaml, 'causative_part', "")
        self.passive_part = getOrElse(yaml, 'passive_part', "")
        self.noun = getOrElse(yaml, 'noun', "")
        self.category = getOrElse(yaml, 'category', "")
        self.semrole = getOrElse(yaml, 'semrole', "")
        self.arg = getOrElse(yaml, 'arg', "")
        self.weight = getOrElse(yaml, 'weight', 0.0)

    def __repr__(self):
        return "{{part={}, causative_part={}, passive_part={}, noun={}, category={}, semrole={}, arg={}, weight={}}}".format(self.part, self.causative_part, self.passive_part, self.noun, self.category, self.semrole, self.arg, self.weight)
