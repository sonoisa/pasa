# -*- coding: utf-8 -*-

from pasa.utils import get_or_else


# カテゴリー辞書のためのクラス
# 　カテゴリ辞書の構成
#  Categorys
#    - [Category]<-
#       - [noun]
#       -  category_name
class CategoryDict(object):
    def __init__(self, yaml):
        self.category_name = get_or_else(yaml, 'category_name', "")
        self.noun = get_or_else(yaml, 'noun', [])

    def __repr__(self):
        return "{{category_name={}, noun={}}}".format(self.category_name, self.noun)
