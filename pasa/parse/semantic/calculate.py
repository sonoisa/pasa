# -*- coding: utf-8 -*-

from operator import itemgetter
from pasa.utils import *


# フレームより曖昧性を解消する計算を行うクラス
# @todo ここで求まる結果はタプルで無理やり格納して返している　＜ー新たな構造体などを用意してきれいにしたい
class Calculate(object):
    def __init__(self, frames):
        self.frames = frames

    # 述語のフレームを取得し，その内から最も類似度の高いフレームを取得
    def get_frame(self, verb, linkchunks):
        frames = self.frames.get_frame(verb)
        if frames is None:
            return None
        else:
            candidates = flatten(list(map(
                lambda frame: list(map(
                    lambda instance: self._calculate_snt_similar(frame.semantic, instance, linkchunks),
                    frame.instance)) if frame.instance else [(frame.semantic, -1.0, [])],
                frames.frame)))
            return max(candidates, key=itemgetter(1))

    # 事例の類似度を算出
    def _calculate_snt_similar(self, semantic, instance, linkchunks):
        comb = self._calculate_all_combinations(instance, linkchunks)
        insts = []
        while any(m[0] > 0 for m in comb):
            max_inst = max(comb, key=itemgetter(0))
            insts.append(max_inst)
            comb = list(filter(lambda arg: not ((arg[1].noun + arg[1].part) == (max_inst[1].noun + max_inst[1].part) or arg[2] == max_inst[2]), comb))

        similar = reduce(lambda s, i: s + i[0], insts, 0.0)
        return semantic, similar, insts

    # 入力文と事例の項のすべての組み合わせの項類似度を求める
    def _calculate_all_combinations(self, instance, linkchunks):
        combinations = flatten(list(map(
            lambda linkchunk: list(map(
                lambda icase: (self._calculate_arg_similar(icase, linkchunk), icase, linkchunk),
                instance.cases)),
            linkchunks)))
        return combinations

    # 項類似度を算出
    def _calculate_arg_similar(self, icase, chunk):
        nounsimilar = self._get_noun_similar(icase, chunk)
        partsimilar = self._get_part_similar(icase, chunk)
        surfsimilar = self._get_surf_similar(icase, chunk)
        similar = round(partsimilar * (surfsimilar + partsimilar + nounsimilar) * icase.weight, 6)
        return similar

    # 名詞のカテゴリーによる類似度
    @staticmethod
    def _get_noun_similar(icase, chunk):
        category = chunk.get_category(icase.category)
        if category is not None:
            return category.confidence
        else:
            return 0.0

    #　名詞の表層による類似度
    @staticmethod
    def _get_surf_similar(icase, chunk):
        surf = chunk.main
        if surf == "":
            return 0.0
        elif surf == icase.noun:
            return 1.0
        else:
            return 0.0

    # 名詞につく格による類似度
    @staticmethod
    def _get_part_similar(icase, chunk):
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
