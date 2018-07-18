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
    def __init__(self, json_loader):
        self.categorys = category.Dict(json.loads(json_loader.category_loader()))
        self.ccharts = cchart.Dict(json.loads(json_loader.cchart_loader()))
        self.idioms = idiom.Dict(json.loads(json_loader.idiom_loader()))
        self.filters = filter.Dict(json.loads(json_loader.filter_loader()))
        self.frames = frame.Dict(json.loads(json_loader.frame_loader()))
        self.compound_predicates = compound_predicate.Dict(json.loads(json_loader.compound_predicate_loader()))
        self.nouns = noun.Dict(json.loads(json_loader.noun_loader()))
