# -*- coding: utf-8 -*-

from .instance import Instance

from pasa.utils import getOrElse


class Frame(object):
    def __init__(self, yaml):
        self.head = getOrElse(yaml, 'head', "")
        self.support = getOrElse(yaml, 'support', "")
        self.instance = list(map(lambda s: Instance(s), getOrElse(yaml, 'instance', [])))

    def __repr__(self):
        return "{{head={}, support={}, instance={}}}".format(self.head, self.support, self.instance)
