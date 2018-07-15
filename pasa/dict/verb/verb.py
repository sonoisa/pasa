# -*- coding: utf-8 -*-

from pasa.utils import get_or_else


# 動詞辞書のためのクラス
# 　動詞辞書の構成
#  Verbs
#    - [Verb] <-
#       -  entry
#       -  head
#       -  voice
class Verb(object):
    def __init__(self, yaml):
        self.entry = get_or_else(yaml, 'entry', "")
        self.head = get_or_else(yaml, 'head', "")
        self.voice = get_or_else(yaml, 'voice', "")

    def __repr__(self):
        return "{{entry={}, head={}, voice={}}}".format(self.entry, self.head, self.voice)
