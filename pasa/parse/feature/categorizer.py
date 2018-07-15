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
        category = self.categories.get_cates(linkchunk.main)

        if any(morph.pos in ["名詞,接尾,助数詞", "名詞,数"] for morph in linkchunk.morphs):
            if any(morph.surface in ["年", "月", "日", "時", "分", "秒"] for morph in linkchunk.morphs):
                category.append(Category("時間", 1.0))
            else:
                category.append(Category("数値", 1.0))

        for morph in linkchunk.morphs:
            pos = morph.pos
            if pos in ["名詞,固有名詞,人名", "名詞,接尾,人名"]:
                category.append(Category("人", 1.0))
            elif pos in ["名詞,固有名詞,地域", "名詞,接尾,地域"]:
                category.append(Category("場所", 1.0))
            elif pos == "名詞,固有名詞,組織":
                category.append(Category("組織", 1.0))

        # for morph in linkchunk.morphs:
        #     pos = morph.pos
        #     if pos in ["名詞,接尾,助数詞", "名詞,数"]:
        #         if morph.surface:
        #             category.append(Category("時間", 1.0))
        #         else:
        #             category.append(Category("数値", 1.0))
        #     elif pos in ["名詞,固有名詞,人名", "名詞,接尾,人名"]:
        #         category.append(Category("人", 1.0))
        #     elif pos in ["名詞,固有名詞,地域", "名詞,接尾,地域"]:
        #         category.append(Category("場所", 1.0))
        #     elif pos == "名詞,固有名詞,組織":
        #         category.append(Category("組織", 1.0))

        return Category.distinct_categories(category)
