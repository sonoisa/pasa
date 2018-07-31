# -*- coding: utf-8 -*-

# 語義，意味役割を付与するためのクラス
from .noun_structure import NounStructure
from .adjunct import Adjunct
from .calculate import Calculate
from pasa.result import Category


class Sematter(object):
    def __init__(self, frames, categorys, nouns):
        self.frames = frames
        self.categorys = categorys
        self.nouns = nouns
        self.calc = Calculate(frames)
        self.adjunct = Adjunct()
        self.nounstruct = NounStructure(nouns, frames)

    def parse(self, result):
        verbchunks = self._get_sem_chunks(result)
        for verbchunk in verbchunks:
            linkchunks = self._get_link_chunks(verbchunk)
            self._set_another_part(linkchunks)
            frame = self.calc.get_frame(verbchunk.main, linkchunks)
            if frame is not None:
                semantic, similar, insts = frame
                self._set_semantic(semantic, similar, verbchunk)
                self._set_sem_role(insts)
                self._set_arg(insts)
                self._set_special_semantic(verbchunk)
                self.adjunct.parse(verbchunk.modifiedchunks)

        nounchunks = self._get_noun_chunks(result)
        for nounchunk in nounchunks:
            self.nounstruct.parse(nounchunk)

        self._set_inversed_semantic(result)
        return result

    def _set_inversed_semantic(self, result):
        for chunk in result.chunks:
            self._get_mod_chunk(chunk)

    @staticmethod
    def _get_mod_chunk(chunk):
        if chunk.modifyingchunk is not None:
            chunk.modifiedchunks.append(chunk.modifyingchunk)

    @staticmethod
    def _set_special_semantic(chunk):
        semantics = chunk.semantic.split("-")
        semantics.extend(["", "", "", "", ""])
        if semantics[1] == "位置変化" and semantics[3] == "着点への移動":
            if not any("対象" in c.semrole for c in chunk.modifiedchunks):
                schunk = list(filter(lambda c: c.part == "が", chunk.modifiedchunks))
                if schunk:
                    schunk[0].semrole.append("対象")
        elif semantics[1] == "位置変化" and semantics[2] == "位置変化（物理）（人物間）" and semantics[3] == "他者からの所有物の移動":
            if not any("着点" in c.semrole for c in chunk.modifiedchunks):
                schunk = list(filter(lambda c: "動作主" in c.semrole or "経験者" in c.semrole, chunk.modifiedchunks))
                if schunk:
                    schunk[0].semrole.append("着点")

    # 助詞の言い換え候補があるものに対して，言い換えの助詞を付与
    @staticmethod
    def _set_another_part(chunks):
        for chunk in chunks:
            for morph in chunk.morphs:
                pos = morph.pos
                if pos.find("格助詞") >= 0 and chunk.part == "に":
                    chunk.another_parts = ["へ"]
                elif pos.find("格助詞") >= 0 and chunk.part == "へ":
                    chunk.another_parts = ["に"]
                elif pos.find("係助詞") >= 0:
                    chunk.another_parts = ["が", "を"]

    def _get_noun_chunks(self, result):
        chunks = list(filter(lambda chunk: self.nouns.is_frame(chunk.main), result.chunks))
        return chunks

    # 係り先である節を取得
    def _get_sem_chunks(self, result):
        chunks = list(filter(lambda c: c.ctype != "elem" and self.frames.is_frame(c.main), result.chunks))
        return chunks

    # 係り先の節を渡して，その係り元を取得
    @staticmethod
    def _get_link_chunks(verbchunk):
        if verbchunk.modifyingchunk is not None:
            linkchunks = [c for c in verbchunk.modifiedchunks]
            if verbchunk.modifyingchunk.ctype == "elem":
                can = set(map(lambda c: c.part, verbchunk.modifiedchunks))
                verbchunk.modifyingchunk.another_parts = [p for p in ["が", "を", "に"] if p not in can]
                linkchunks.append(verbchunk.modifyingchunk)
            return linkchunks
        else:
            return verbchunk.modifiedchunks

    # 曖昧性を解消したフレームのデータより語義を付与
    # @param semantic Calcurateクラスより取得したデータ
    # @param verbchunk 語義を付与する文節
    @staticmethod
    def _set_semantic(semantic, similar, verbchunk):
        verbchunk.semantic = semantic
        verbchunk.similar = similar

    # 曖昧性を解消したフレームのデータより意味役割を付与
    # @param semantic Calcurateクラスより取得したデータ
    @staticmethod
    def _set_sem_role(insts):
        for instset in insts:
            similar, icase, chunk = instset
            if icase.semrole:
                chunk.semrole.append(icase.semrole)
            chunk.similar = similar
            category = chunk.get_category(icase.category)
            if category is not None:
                chunk.category.insert(0, category)
                chunk.category = Category.distinct_categories(chunk.category)

    @staticmethod
    def _set_arg(insts):
        for instset in insts:
            similar, icase, chunk = instset
            if icase.arg:
                chunk.arg.append(icase.arg)
            chunk.similar = similar
            category = chunk.get_category(icase.category)
            if category is not None:
                chunk.category.insert(0, category)
                chunk.category = Category.distinct_categories(chunk.category)
