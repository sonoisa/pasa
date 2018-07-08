# -*- coding: utf-8 -*-

from .analyzer import Analyzer
from .analyzer import Basic
from .feature import Tagger
from .idiom import Hiuchi
from .semantic import Sematter
from .compound_predicate import Synonym

class Parse(object):
    def __init__(self, dicts):
        self.analyzer = Analyzer()
        self.basic = Basic(dicts.frames)
        self.sematter = Sematter(dicts.frames, dicts.categorys, dicts.nouns)
        self.tagger = Tagger(dicts.ccharts, dicts.categorys)
        self.idom = Hiuchi(dicts.idioms, dicts.filters)
        self.compoundPredicate = Synonym(dicts.compoundPredicates, dicts.filters)

    def parse(self, line):
        result = self.parseChunk(line)
        result = self.parseFeature(result)
        result = self.parseIdiom(result)
        result = self.parseSemantic(result)
        result = self.parseCompoundPredicate(result)
        return result

    def parseChunk(self, line):
        result = self.analyzer.parse(line)
        result = self.basic.parse(result)
        return result

    def parseFeature(self, result):
        return self.tagger.parse(result)

    def parseIdiom(self, result):
        return self.idom.parse(result)

    def parseSemantic(self, result):
        return self.sematter.parse(result)

    def parseCompoundPredicate(self, result):
        return self.compoundPredicate.parse(result)