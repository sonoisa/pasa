# -*- coding: utf-8 -*-
from . import category
from . import cchart
from . import filter
from . import frame
from . import idiom
from . import verb
from . import noun
from . import compoundPredicate

import yaml


class LoadYaml(object):
    def __init__(self, files):
        self.categorys = category.Dict(yaml.load(open(files.category, 'r')))
        self.verbs = verb.Verbs(yaml.load(open(files.verb, 'r')))
        self.ccharts = cchart.Dict(yaml.load(open(files.cchart, 'r')))
        self.idioms = idiom.Dict(yaml.load(open(files.idiom, 'r')))
        self.filters = filter.Dict(yaml.load(open(files.filter, 'r')))
        self.frames = frame.Dict(yaml.load(open(files.frame, 'r')))
        self.compoundPredicates = compoundPredicate.Dict(yaml.load(open(files.compoundPredicate, 'r')))
        self.nouns = noun.Dict(yaml.load(open(files.noun, 'r')))
