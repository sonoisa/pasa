# -*- coding: utf-8 -*-
from .verb import Verb
from pasa.utils import getOrElse


# 動詞辞書のためのクラス
# 　動詞辞書の構成
#  Verbs <-
#    - [Verb]
#       -  entry
#       -  head
#       -  voice
class Verbs(object):
    def __init__(self, yaml):
        self.verb = list(map(lambda v: Verb(v), getOrElse(yaml, 'verb', [])))

    def isVerb(self, verbs):
        for ver in self.verb:
            if verbs and verbs == ver.entry:
                return True
        return False

    def __repr__(self):
        return "{{verb={}}}".format(self.verb)
