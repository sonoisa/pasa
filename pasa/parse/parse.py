# -*- coding: utf-8 -*-

from .analyzer import Analyzer
from .analyzer import Basic
from .feature import Tagger
from .feature import Categorizer
from .idiom import Hiuchi
from .semantic import Sematter
from .compound_predicate import Synonym


class Parse(object):
    def __init__(self, dicts):
        self.analyzer = Analyzer()
        self.basic = Basic(dicts.frames)
        self.sematter = Sematter(dicts.frames, dicts.categorys, dicts.nouns)
        self.tagger = Tagger(dicts.ccharts)
        self.categorizer = Categorizer(dicts.categorys)
        self.idom = Hiuchi(dicts.idioms, dicts.filters)
        self.compound_predicate = Synonym(dicts.compound_predicates, dicts.filters)

    def parse(self, line):
        result = self._parse_chunk(line)
        result = self._parse_feature(result)
        result = self._parse_idiom(result)
        result = self._parse_semantic(result)
        result = self._parse_compound_predicate(result)
        return result

    def _parse_chunk(self, line):
        result = self.analyzer.parse(line)
        result = self.basic.parse(result)
        return result

    def _parse_feature(self, result):
        result = self.tagger.parse(result)
        result = self.categorizer.parse(result)
        return result

    def _parse_idiom(self, result):
        return self.idom.parse(result)

    def _parse_semantic(self, result):
        return self.sematter.parse(result)

    def _parse_compound_predicate(self, result):
        return self.compound_predicate.parse(result)
