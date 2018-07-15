# -*- coding: utf-8 -*-
from .pattern import Pattern

from pasa.utils import get_or_else


class CompoundPredicate(object):
    def __init__(self, yaml):
        self.entry = get_or_else(yaml, 'entry', "")
        self.phrase = get_or_else(yaml, 'phrase', [])
        self.patterns = list(map(lambda p: Pattern(p), get_or_else(yaml, 'patterns', [])))
        self.semantic = get_or_else(yaml, 'semantic', "")

    def __repr__(self):
        return "{{entry={}, phrase={}, patterns={}, semantic={}}}".format(self.entry, self.phrase, self.patterns, self.semantic)
