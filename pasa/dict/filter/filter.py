# -*- coding: utf-8 -*-
from .feature import Feature

from pasa.utils import getOrElse


class Filter(object):
    def __init__(self, yaml):
        self.entry = getOrElse(yaml, 'entry', "")
        self.negative = Feature(getOrElse(yaml, 'negative', {}))
        self.positive = Feature(getOrElse(yaml, 'positive', {}))

    def __repr__(self):
        return "{{entry={}, negative={}, positive={}}}".format(self.entry, self.negative, self.positive)
