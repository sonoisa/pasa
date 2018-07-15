# -*- coding: utf-8 -*-

from pasa.utils import get_or_else


class Agent(object):
    def __init__(self, yaml):
        self.agentive = get_or_else(yaml, 'agentive', "")
        self.semantic = get_or_else(yaml, 'semantic', "")
        self.arg0 = get_or_else(yaml, 'arg0', "")
        self.arg1 = get_or_else(yaml, 'arg1', "")
        self.arg2 = get_or_else(yaml, 'arg2', "")

    def __repr__(self):
        return "{{agentive={}, semantic={}, arg0={}, arg1={}, arg2={}}}".format(self.agentive, self.semantic, self.arg0, self.arg1, self.arg2)
