# -*- coding: utf-8 -*-
from pasa.result import Category


class Categorizer(object):
    """文節にカテゴリ情報を付与するクラス"""
    def __init__(self, categories):
        self.categories = categories

    def parse(self, result):
        """文節にカテゴリ情報を付与する。"""
        for chunk in result.chunks:
            chunk.category = self._parse_category(chunk)
        return result

    # 文節中に名詞カテゴリが付与できるものがあればカテゴリの種類を返す
    # @param morphs 文節中の形態素の配列
    # @return カテゴリ
    def _parse_category(self, linkchunk):
        reason = Category.REASON_POS
        category = self.categories.get_cates(linkchunk.main)

        if any(morph.pos in ["名詞,非自立,副詞可能", "名詞,接尾,副詞可能", "名詞,副詞可能"] for morph in linkchunk.morphs):
            if any(morph.surface in ["時", "とき"] for morph in linkchunk.morphs):
                category = [Category("時間", 1.0, reason)] # categoryを上書きしているのは意図的である

        if any(morph.pos in ["名詞,接尾,助数詞", "名詞,数"] for morph in linkchunk.morphs):
            if any(morph.surface in ["年", "月", "日", "時", "分", "秒"] for morph in linkchunk.morphs):
                category.append(Category("時間", 1.0, reason))
            else:
                category.append(Category("数値", 1.0, reason))

        if linkchunk.main_morphs:
            last_morph = linkchunk.main_morphs[-1]
            pos = last_morph.pos
            if pos in ["名詞,固有名詞,人名", "名詞,接尾,人名"]:
                category.append(Category("人", 1.0, reason))
            elif pos in ["名詞,固有名詞,地域", "名詞,接尾,地域"]:
                category.append(Category("場所", 1.0, reason))
            elif pos == "名詞,固有名詞,組織":
                category.append(Category("組織", 1.0, reason))

        return Category.distinct_categories(category)
