# -*- coding: utf-8 -*-

from operator import itemgetter
from pasa.utils import *


# フレームより曖昧性を解消する計算を行うクラス
# @todo ここで求まる結果はタプルで無理やり格納して返している　＜ー新たな構造体などを用意してきれいにしたい
class Calculate(object):
    def __init__(self, frames):
        self.frames = frames

    # 述語のフレームを取得し，その内から最も類似度の高いフレームを取得
    def getFrame(self, verb, linkchunks):
        # Option[(String, Float, Seq[(Float, Case, Chunk)])] = {
        frames = self.frames.getFrame(verb)
        if frames is None:
            return None
        else:
            xs = flatten(list(map(
                lambda frame: list(map(
                    lambda instance: self.calculateSntSimilar(frame.semantic, instance, linkchunks),
                    frame.instance)) if frame.instance else [(frame.semantic, -1.0, [])],
                frames.frame)))
            return max(xs, key=itemgetter(1))

    # 事例の類似度を算出
    def calculateSntSimilar(self, semantic, instance, linkchunks):
        comb = self.calculateAllCombinations(instance, linkchunks)
        insts = []
        while any(m[0] > 0 for m in comb):
            x = max(comb, key=itemgetter(0))
            insts.append(x)
            comb = list(filter(lambda arg: not ((arg[1].noun + arg[1].part) == (x[1].noun + x[1].part) or arg[2] == x[2]), comb))

        similar = reduce(lambda s, i: s + i[0], insts, 0.0)
        return semantic, similar, insts

    # 入力文と事例の項のすべての組み合わせの項類似度を求める
    def calculateAllCombinations(self, instance, linkchunks):
        combinations = flatten(list(map(
            lambda linkchunk: list(map(
                lambda icase: (self.calculateArgSimilar(icase, linkchunk), icase, linkchunk),
                instance.cases)),
            linkchunks)))
        return combinations

    # 項類似度を算出
    def calculateArgSimilar(self, icase, chunk):
        nounsimilar = self.getNounSimilar(icase, chunk)
        partsimilar = self.getPartSimilar(icase, chunk)
        surfsimilar = self.getSurfSimilar(icase, chunk)
        similar = round(partsimilar * (surfsimilar + partsimilar + nounsimilar) * icase.weight, 6)
        return similar

    # 名詞のカテゴリーによる類似度
    def getNounSimilar(self, icase, chunk):
        if icase.category in chunk.category:
            return 1.0
        else:
            return 0.0

    #　名詞の表層による類似度
    def getSurfSimilar(self, icase, chunk):
        surf = chunk.main
        if surf == "":
            return 0.0
        elif surf == icase.noun:
            return 1.0
        else:
            return 0.0

    # 名詞につく格による類似度
    def getPartSimilar(self, icase, chunk):
        part = icase.part
        if part:
            if chunk.part == part:
                return 1.0
            elif part == "は" and chunk.part == "が":
                return 1.1 # シソーラスの格が"は"のとき"が"
            elif part == "は" and chunk.part == "を":
                return 1.1 # シソーラスの格が"は"のとき"を"
            elif part in chunk.another_parts:
                return 1.0
            elif chunk.modifyingchunk:
                voice = chunk.modifyingchunk.voice
                if voice == "CAUSATIVE" and chunk.part == icase.causative_part:
                    return 1.0
                elif voice == "PASSIVE" and chunk.part == icase.passive_part:
                    return 1.0
                else:
                    return 0.0
            else:
                return 0.0
        else:
            return 0.0
