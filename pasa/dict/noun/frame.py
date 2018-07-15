# -*- coding: utf-8 -*-

from .instance import Instance

from pasa.utils import get_or_else


class Frame(object):
    def __init__(self, yaml):
        self.head = get_or_else(yaml, 'head', "")
        self.support = get_or_else(yaml, 'support', "")
        self.instance = list(map(lambda s: Instance(s), get_or_else(yaml, 'instance', [])))

    def __repr__(self):
        return "{{head={}, support={}, instance={}}}".format(self.head, self.support, self.instance)
