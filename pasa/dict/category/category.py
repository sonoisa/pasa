# -*- coding: utf-8 -*-

from pasa.utils import getOrElse


# カテゴリー辞書のためのクラス
# 　カテゴリ辞書の構成
#  Categorys
#    - [Category]<-
#       - [noun]
#       -  category_name
class Category(object):
    def __init__(self, yaml):
        self.category_name = getOrElse(yaml, 'category_name', "")
        self.noun = getOrElse(yaml, 'noun', [])

    def __repr__(self):
        return "{{category_name={}, noun={}}}".format(self.category_name, self.noun)
