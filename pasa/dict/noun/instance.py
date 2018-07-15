# -*- coding: utf-8 -*-

from .agent import Agent
from .case import Case

from pasa.utils import get_or_else


class Instance(object):
    def __init__(self, yaml):
        self.cases = list(map(lambda c: Case(c), get_or_else(yaml, 'cases', [])))
        self.agent = list(map(lambda c: Agent(c), get_or_else(yaml, 'agent', [])))

    def __repr__(self):
        return "{{cases={}, agent={}}}".format(self.cases, self.agent)
