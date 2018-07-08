# -*- coding: utf-8 -*-
from .frame import Frame


class Dict(object):
    def __init__(self, yaml):
        self.dict = list(map(lambda f: Frame(f), yaml['dict']))

    def getFrame(self, verb):
        for frame in self.dict:
            if verb == frame.verb:
                return frame
        return None

    def getSemanticFirstInstance(self, verb, sem):
        for fp in self.dict:
            if verb == fp.verb:
                for frame in fp.frame:
                    if frame.semantic == sem:
                        if frame.instance:
                            return frame.instance[0]
                        else:
                            return None
        return None

    def isFrame(self, verb):
        return any(verb == frame.verb for frame in self.dict)

    def __repr__(self):
        return "{{dict={}}}".format(self.dict)
