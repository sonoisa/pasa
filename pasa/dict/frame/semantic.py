# -*- coding: utf-8 -*-
from .instance import Instance

from pasa.utils import get_or_else


class Semantic(object):
    def __init__(self, yaml):
        self.semantic = get_or_else(yaml, 'semantic', "")
        yinstance = get_or_else(yaml, 'instance', [])
        self.instance = list(map(lambda i: Instance(i), yinstance if yinstance is not None else []))

    def __repr__(self):
        return "{{semantic={}, instance={}}}".format(self.semantic, self.instance)
