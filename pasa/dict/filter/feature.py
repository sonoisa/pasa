# -*- coding: utf-8 -*-

from pasa.utils import get_or_else


class Feature(object):
    def __init__(self, yaml):
        self.polarity = get_or_else(yaml, 'polarity', "")
        self.category = get_or_else(yaml, 'category', [])
        self.sentelem = get_or_else(yaml, 'sentelem', [])
        self.voice = get_or_else(yaml, 'voice', [])
        self.mood = get_or_else(yaml, 'mood', [])

    def __repr__(self):
        return "{{polarity={}, category={}, sentelem={}, voice={}, mood={}}}".format(self.polarity, self.category, self.sentelem, self.voice, self.mood)
