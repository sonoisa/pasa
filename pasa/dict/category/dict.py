# -*- coding: utf-8 -*-

from .category import Category
from pasa.utils import distinct


class Dict(object):
    def __init__(self, yaml):
        self.dict = list(map(lambda c: Category(c), yaml['dict']))

    def getCates(self, noun):
        category_names = distinct([category.category_name for category in self.dict if noun in category.noun])
        return distinct(category_names)

    def __repr__(self):
        return "{{dict={}}}".format(self.dict)
