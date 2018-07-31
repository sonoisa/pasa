# -*- coding: utf-8 -*-

from .category import CategoryDict
from pasa.utils import distinct
from pasa.result import Category


class Dict(object):
    def __init__(self, yaml):
        self.dict = list(map(lambda c: CategoryDict(c), yaml['dict']))

    def get_cates(self, noun):
        category_names = distinct([category.category_name for category in self.dict if noun in category.noun])
        return [Category(name, 1.0, Category.REASON_DICT) for name in category_names]

    def __repr__(self):
        return "{{dict={}}}".format(self.dict)
