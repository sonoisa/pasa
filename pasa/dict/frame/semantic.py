# -*- coding: utf-8 -*-
from .instance import Instance

from pasa.utils import getOrElse


class Semantic(object):
    def __init__(self, yaml):
        self.semantic = getOrElse(yaml, 'semantic', "")
        yinstance = getOrElse(yaml, 'instance', [])
        self.instance = list(map(lambda i: Instance(i), yinstance if yinstance is not None else []))

    def __repr__(self):
        return "{{semantic={}, instance={}}}".format(self.semantic, self.instance)
