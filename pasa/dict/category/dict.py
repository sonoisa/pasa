# -*- coding: utf-8 -*-

from .category import Category
from pasa.utils import distinct
from pasa.result import Category as CategoryObj


class Dict(object):
    def __init__(self, yaml):
        self.dict = list(map(lambda c: Category(c), yaml['dict']))

    def get_cates(self, noun):
        category_names = distinct([category.category_name for category in self.dict if noun in category.noun])
        return [CategoryObj(name, 1.0) for name in category_names]

    def __repr__(self):
        return "{{dict={}}}".format(self.dict)
