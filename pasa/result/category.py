# -*- coding: utf-8 -*-
from pasa.utils import distinct


class Category(object):
    def __init__(self, name, confidence):
        self.name = name    # カテゴリ名
        self.confidence = confidence    # 確信度（0.0〜1.0）

    def __str__(self):
        return str({
            "name": self.name,
            "confidence": self.confidence
        })

    def __repr__(self):
        return str(self)

    @staticmethod
    def distinct_categories(categories):
        """同名のカテゴリについて、確信度が最大のもののみ残す。出現順を保つ。"""
        new_categories = []
        category_names = distinct([c.name for c in categories])
        for name in category_names:
            new_categories.append(max([c for c in categories if c.name == name], key=lambda c: c.confidence))
        return new_categories
