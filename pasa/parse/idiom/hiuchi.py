# -*- coding: utf-8 -*-

from pasa.utils import *


# 慣用句同定のためのクラス
# 以下の手順により同定
# - 形態素のグラフ化
# - 慣用句の同定
# - フィルタリング
class Hiuchi(object):
    def __init__(self, idioms, filters):
        self.idioms = idioms
        self.filters = filters

    def parse(self, result):
        self.graphify(result)
        self.matchIdiom(result)
        return result

    # 慣用句同定のために入力文グラフを作成
    def graphify(self, result):
        self.graphifyAsSequence(result)
        self.graphifyAsDependency(result)
        # self.graphifyAsSkipped(result)

    # 形態素の並び順によるグラフ化
    def graphifyAsSequence(self, result):
        morphs = self.getMorphs(result)
        if len(morphs) > 1:
            def process(prechunk, postchunk):
                postchunk.tree.append(prechunk)
                return postchunk
            reduce(process, morphs)

    # 係り受け関係によるグラフ化
    def graphifyAsDependency(self, result):
        for chunk in result.chunks:
            modifiedmorphs = list(map(lambda c: c.morphs[-1], chunk.modifiedchunks))
            distinct_append(chunk.morphs[0].tree, modifiedmorphs)

    # 空白や接続詞などの関係ない形態素を除いたグラフ化
    # @todo 他にも除外する条件あり
    def graphifyAsSkipped(self, result):
        morphs = self.getMorphs(result)
        for morph in morphs:
            for depmorph in morph.tree:
                if depmorph.pos.find("接頭詞") >= 0 or depmorph.pos.find("記号") >= 0 or depmorph.pos.find("接続助詞") >= 0:
                    distinct_append(morph.tree, depmorph.tree)

    # 慣用句表記辞書との比較し，慣用句情報の付与
    def matchIdiom(self, result):
        morphs = self.getMorphs(result)
        candicates = self.getCandicate(morphs)
        for idiom in candicates:
            for idiommorphs in self.matchMorphs(morphs, idiom.patterns):
                self.setIdiom(idiom, idiommorphs)

    # 慣用句表記辞書より候補となる慣用句の取得
    # (慣用句の最後の形態素と一致する形態素があれば候補とする)
    def getCandicate(self, morphs):
        candicate = []
        for morph in morphs:
            for idiom in self.idioms.dict:
                if self.isMatchPattern(morph, idiom.patterns[-1]):
                    candicate.append(idiom)
        return distinct(candicate)

    # 慣用句の候補と入力文グラフを比較し，慣用句と一致する形態素を取得
    def matchMorphs(self, morphs, patterns):
        idiommorphs = list(filter(
            lambda f: len(f) == len(patterns),
            foldRight(lambda pattern, precandidates: list(filter(
                lambda candidate:
                    self.isMatchPattern(candidate[0], pattern),
                flatten(list(map(
                    lambda precandidate:
                        list(map(lambda morph: [morph] + precandidate, precandidate[0].tree)),
                    precandidates))) if precandidates else list(map(lambda m: [m], morphs)))),
                [],
                patterns)))
        return idiommorphs

    # 同定された慣用句の特徴をまとめるクラス
    # この特徴は慣用句に関係する文節よりもってくる
    class MyIdiom(object):
        def __init__(self):
            self.entry = ""
            self.voice = []
            self.polarity = []
            self.mood = []
            self.category = []
            self.sentlem = ""
            self.score = 0.0

    def setIdiom(self, idiom, morphs):
        chunks = distinct(list(map(lambda m: m.chunk, morphs)))
        midiom = self.MyIdiom()
        midiom.entry = idiom.entry
        for chunk in chunks:
            midiom.voice.append(chunk.voice)
            midiom.mood.append(chunk.mood)
            midiom.polarity.append(chunk.polarity)

        modifer = []
        for chunk in chunks:
            for mchunk in chunk.modifiedchunks:
                if mchunk not in chunks:
                    modifer.append(mchunk)

        midiom.category = distinct(flatten([chunk.category for chunk in modifer if chunk.category]))

        self.filtering(midiom)
        for chunk in chunks:
            chunk.idiom = idiom.entry
            chunk.phrase = idiom.phrase
            chunk.idiom_morph = morphs
            chunk.idiom_score = midiom.score

    # フィルタリング辞書より曖昧性のスコアを計算
    def filtering(self, idiom):
        f = self.filters.getFilter(idiom.entry)
        if f is None:
            score = 0.5
        else:
            nega = 0.0 if self.disambiguator(f.negative, idiom) else 0.5
            posi = 1.0 if self.disambiguator(f.positive, idiom) else 0.5
            score = (nega + posi) / 2
        idiom.score = score

    # フィルタリング辞書のposi/nega要素の一致判定
    def disambiguator(self, feature, idiom):
        if feature.polarity:
            if feature.polarity == idiom.polarity:
                return True
        if feature.category:
            if any(c in idiom.category for c in feature.category):
                return True
        if feature.mood:
            if any(m in idiom.mood for m in feature.mood):
                return True
        if feature.voice:
            if any(v in idiom.voice for v in feature.voice):
                return True
        return False

    # resultよりすべての形態素を取得
    def getMorphs(self, result):
        morphs = flatten(list(map(lambda c: c.morphs, result.chunks)))
        return morphs

    # 慣用句表記辞書内の1形態素分の一致判定
    def isMatchPattern(self, morph, pattern):
        for idcase in pattern.cases:
            if (idcase.base == "" or idcase.base == morph.base) and (idcase.read == "" or idcase.read == morph.read) and (idcase.pos == "" or idcase.pos == morph.pos):
                return True
        return False
