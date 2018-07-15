# -*- coding: utf-8 -*-
from .semantic import Semantic

from pasa.utils import get_or_else


class Frame(object):
    def __init__(self, yaml):
        self.verb = get_or_else(yaml, 'verb', "")
        self.frame = list(map(lambda s: Semantic(s), get_or_else(yaml, 'frame', [])))

    def __repr__(self):
        return "{{verb={}, frame={}}}".format(self.verb, self.frame)
