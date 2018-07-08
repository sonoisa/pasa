# -*- coding: utf-8 -*-
from .pattern import Pattern

from pasa.utils import getOrElse


class CompoundPredicate(object):
    def __init__(self, yaml):
        self.entry = getOrElse(yaml, 'entry', "")
        self.phrase = getOrElse(yaml, 'phrase', [])
        self.patterns = list(map(lambda p: Pattern(p), getOrElse(yaml, 'patterns', [])))
        self.semantic = getOrElse(yaml, 'semantic', "")

    def __repr__(self):
        return "{{entry={}, phrase={}, patterns={}, semantic={}}}".format(self.entry, self.phrase, self.patterns, self.semantic)
