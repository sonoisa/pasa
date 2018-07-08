# -*- coding: utf-8 -*-

from pasa.utils import getOrElse


class Feature(object):
    def __init__(self, yaml):
        self.polarity = getOrElse(yaml, 'polarity', "")
        self.category = getOrElse(yaml, 'category', [])
        self.sentelem = getOrElse(yaml, 'sentelem', [])
        self.voice = getOrElse(yaml, 'voice', [])
        self.mood = getOrElse(yaml, 'mood', [])

    def __repr__(self):
        return "{{polarity={}, category={}, sentelem={}, voice={}, mood={}}}".format(self.polarity, self.category, self.sentelem, self.voice, self.mood)
