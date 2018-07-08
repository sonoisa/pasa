# -*- coding: utf-8 -*-

from pasa.utils import getOrElse


# 動詞辞書のためのクラス
# 　動詞辞書の構成
#  Verbs
#    - [Verb] <-
#       -  entry
#       -  head
#       -  voice
class Verb(object):
    def __init__(self, yaml):
        self.entry = getOrElse(yaml, 'entry', "")
        self.head = getOrElse(yaml, 'head', "")
        self.voice = getOrElse(yaml, 'voice', "")

    def __repr__(self):
        return "{{entry={}, head={}, voice={}}}".format(self.entry, self.head, self.voice)
