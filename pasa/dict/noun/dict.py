# -*- coding: utf-8 -*-
from .frame import Frame

from pasa.utils import getOrElse


class Dict(object):
    def __init__(self, yaml):
        self.dict = list(map(lambda f: Frame(f), yaml['dict']))

    def isFrame(self, noun):
        if noun:
            for frame in self.dict:
                if frame.head == noun or (frame.head + frame.support) == noun or frame.head == noun[0:-1] or (frame.head + frame.support) == noun[0:-1]:
                    return True
            return False
        else:
            return False

    def getFrame(self, noun):
        if noun:
            for frame in self.dict:
                if frame.head == noun or (frame.head + frame.support) == noun or frame.head == noun[0:-1] or (frame.head + frame.support) == noun[0:-1]:
                    return frame
            return None
        else:
            return None

    def __repr__(self):
        return "{{dict={}}}".format(self.dict)
