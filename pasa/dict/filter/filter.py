# -*- coding: utf-8 -*-
from .feature import Feature

from pasa.utils import get_or_else


class Filter(object):
    def __init__(self, yaml):
        self.entry = get_or_else(yaml, 'entry', "")
        self.negative = Feature(get_or_else(yaml, 'negative', {}))
        self.positive = Feature(get_or_else(yaml, 'positive', {}))

    def __repr__(self):
        return "{{entry={}, negative={}, positive={}}}".format(self.entry, self.negative, self.positive)
