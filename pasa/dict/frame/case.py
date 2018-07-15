# -*- coding: utf-8 -*-

from pasa.utils import get_or_else


class Case(object):
    def __init__(self, yaml):
        self.part = get_or_else(yaml, 'part', "")
        self.causative_part = get_or_else(yaml, 'causative_part', "")
        self.passive_part = get_or_else(yaml, 'passive_part', "")
        self.noun = get_or_else(yaml, 'noun', "")
        self.category = get_or_else(yaml, 'category', "")
        self.semrole = get_or_else(yaml, 'semrole', "")
        self.arg = get_or_else(yaml, 'arg', "")
        self.weight = get_or_else(yaml, 'weight', 0.0)

    def __repr__(self):
        return "{{part={}, causative_part={}, passive_part={}, noun={}, category={}, semrole={}, arg={}, weight={}}}".format(self.part, self.causative_part, self.passive_part, self.noun, self.category, self.semrole, self.arg, self.weight)
