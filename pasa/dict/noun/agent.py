# -*- coding: utf-8 -*-

from pasa.utils import getOrElse


class Agent(object):
    def __init__(self, yaml):
        self.agentive = getOrElse(yaml, 'agentive', "")
        self.semantic = getOrElse(yaml, 'semantic', "")
        self.arg0 = getOrElse(yaml, 'arg0', "")
        self.arg1 = getOrElse(yaml, 'arg1', "")
        self.arg2 = getOrElse(yaml, 'arg2', "")

    def __repr__(self):
        return "{{agentive={}, semantic={}, arg0={}, arg1={}, arg2={}}}".format(self.agentive, self.semantic, self.arg0, self.arg1, self.arg2)
