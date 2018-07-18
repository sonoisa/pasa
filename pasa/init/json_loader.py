# -*- coding: utf-8 -*-

import pkgutil


class JsonLoader(object):
    def __init__(self):
        self.frame_loader = lambda: pkgutil.get_data("pasa", "json/new_argframes.json")
        self.cchart_loader = lambda: pkgutil.get_data("pasa", "json/ccharts.json")
        self.category_loader = lambda: pkgutil.get_data("pasa", "json/new_categorys.json")
        self.idiom_loader = lambda: pkgutil.get_data("pasa", "json/idioms.json")
        self.filter_loader = lambda: pkgutil.get_data("pasa", "json/filters.json")
        self.compound_predicate_loader = lambda: pkgutil.get_data("pasa", "json/compoundPredicates.json")
        self.noun_loader = lambda: pkgutil.get_data("pasa", "json/NounTest.json")
