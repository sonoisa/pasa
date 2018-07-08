# -*- coding: utf-8 -*-
from .semantic import Semantic

from pasa.utils import getOrElse


class Frame(object):
    def __init__(self, yaml):
        self.verb = getOrElse(yaml, 'verb', "")
        self.frame = list(map(lambda s: Semantic(s), getOrElse(yaml, 'frame', [])))

    def __repr__(self):
        return "{{verb={}, frame={}}}".format(self.verb, self.frame)
