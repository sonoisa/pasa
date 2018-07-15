# -*- coding: utf-8 -*-
from pasa.utils import *


# Synonym クラス
# 名詞複合述語を見つけ、その類語と同じ語義、意味役割を付与する
#
# ほとんど Hiuchi のコピペ
# 見つけた慣用句に対して与える情報が違うだけ
class Synonym(object):
    def __init__(self, compound_predicate, filters):
        self.compound_predicates = compound_predicate
        self.filters = filters

    def parse(self, result):
        self._match_compound_predicate(result)
        return result

    # 形態素の木を作成
    def graphify(self, result):
        self._graphify_as_sequence(result)
        self._graphify_as_dependency(result)

    # 形態素の並び順によるグラフ化
    def _graphify_as_sequence(self, result):
        morphs = self._get_morphs(result)
        premorph = morphs[0]
        for morph in morphs[1:]:
            morph.tree.append(premorph)
            premorph = morph

    # 係り受け関係によるグラフ化
    @staticmethod
    def _graphify_as_dependency(result):
        for chunk in result.chunks[::-1]:
            for modchunk in chunk.modifiedchunks:
                tree = chunk.morphs[0].tree
                if not any(c is modchunk.morphs[-1] for c in tree):
                    tree.append(modchunk.morphs[-1])

    # 空白や接続詞などの関係ない形態素を除いたグラフ化
    # @todo 他にも除外する条件あり
    def _graphify_as_skipped(self, result):
        morphs = self._get_morphs(result)
        for morph in morphs:
            for depmorph in morph.tree:
                if depmorph.pos.find("接頭詞") >= 0:
                    distinct_append(morph.tree, depmorph.tree)

    @staticmethod
    def _get_morphs(result):
        morphs = flatten(list(map(lambda c: c.morphs, result.chunks)))
        return morphs

    # @todo すべての形態素を使用し連語の候補を取得した後，再びすべての形態素と候補でマッチングを行っている＜ーこれは無駄
    def _match_compound_predicate(self, result):
        morphs = self._get_morphs(result)
        candicates = self._get_candicate(morphs)

        for compound_predicate in candicates:
            compound_predicate_morph = self._matchs(morphs, compound_predicate.patterns)
            if compound_predicate_morph is not None:
                self._set_compound_predicate(compound_predicate, compound_predicate_morph)

    def _set_compound_predicate(self, compound_predicate, morphs):
        chunks = distinct(list(map(lambda m: m.chunk, morphs)))

        # 複合名詞述語のメイン部分の語義を上書き
        # メイン述語以外の部分の意味役割を上書き
        score = self._filtering() #複合名詞と語義のどちらを選ぶかのスコアを判定（未実装）
        if score > 0.8:
            for chunk in chunks:
                if chunk == chunks[-1]:
                    chunk.semantic = compound_predicate.semantic
                else:
                    chunk.idiom = compound_predicate.entry
                    chunk.phrase = compound_predicate.phrase
                    chunk.semrole = ["慣用句"]
                    chunk.idiom_morph = morphs
                    chunk.idiom_score = score

    @staticmethod
    def _filtering():
        score = 1.0
        return score

    def _get_candicate(self, morphs):
        cand = distinct(flatten(list(map(
            lambda morph: [idiom for idiom in self.compound_predicates.dict if self._is_match_pattern(morph, idiom.patterns[-1])],
            morphs))))
        return cand

    # 連語の同定
    def _matchs(self, morphs, patterns):
        if patterns:
            for morph in morphs:
                if self._is_match_pattern(morph, patterns[-1]):
                    idiom = self._matchs(morph.tree, patterns[0:-1])
                    if idiom is not None:
                        idiom.append(morph)
                        return idiom
            return None
        else:
            return []

    @staticmethod
    def _is_match_pattern(morph, pattern):
        for idcase in pattern.cases:
            bol = True
            if idcase.base:
                bol = bol and idcase.base == morph.base
            if idcase.read:
                bol = bol and idcase.read == morph.read
            if idcase.pos:
                bol = bol and idcase.pos == morph.pos
            if bol:
                return True
        return False
