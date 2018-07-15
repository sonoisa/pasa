# -*- coding: utf-8 -*-
from . import category
from . import cchart
from . import filter
from . import frame
from . import idiom
from . import noun
from . import compound_predicate

import json


class LoadJson(object):
    def __init__(self, files):
        self.categorys = category.Dict(json.load(open(files.category, 'r')))
        self.ccharts = cchart.Dict(json.load(open(files.cchart, 'r')))
        self.idioms = idiom.Dict(json.load(open(files.idiom, 'r')))
        self.filters = filter.Dict(json.load(open(files.filter, 'r')))
        self.frames = frame.Dict(json.load(open(files.frame, 'r')))
        self.compoundPredicates = compound_predicate.Dict(json.load(open(files.compoundPredicate, 'r')))
        self.nouns = noun.Dict(json.load(open(files.noun, 'r')))
