# -*- coding: utf-8 -*-

import re


class Basic(object):
    def __init__(self, frames):
        self.frames = frames

    def parse(self, result):
        last_chunk = result.chunks[-1]
        for chunk in result.chunks:
            chunk.surface = self._get_chunk_surface(chunk)
            chunk.modifyingchunk = self._get_modifying_chunk(result, chunk)
            chunk.modifiedchunks = self._get_modified_chunks(result, chunk)
            chunk.ctype = self._get_chunk_type(chunk, chunk is last_chunk)
            main, main_morphs = self._get_head(chunk)
            chunk.main = main
            chunk.main_morphs = main_morphs
            chunk.part = self._get_part(chunk)
            for morph in chunk.morphs:
                morph.chunk = chunk
        return result

    # 文節内の形態素の表層をつなげて，文節の表層を取得
    # @param chunk 文節
    # @return 文節の表層
    @staticmethod
    def _get_chunk_surface(chunk):
        surface = "".join([m.surface for m in chunk.morphs])
        return surface

    # 係っている文節を取得
    @staticmethod
    def _get_modifying_chunk(result, chunk):
        modifyingchunk = None if chunk.link == -1 else result.chunks[chunk.link]
        return modifyingchunk

    # 文節の係りを受けている文節を取得
    # @param chunk 文節
    # @return 係り元の文節集合
    @staticmethod
    def _get_modified_chunks(result, depchunk):
        linkchunks = [chunk for chunk in result.chunks if chunk.link == depchunk.id]
        return linkchunks

    # 文節のタイプを取得
    #  - verb:      動詞
    #  - adjective: 形容詞，形容動詞
    #  - copula:    コピュラ(AはBだ)
    #  - elem:      その他
    @staticmethod
    def _get_chunk_type(chunk, is_last):
        morphs = chunk.morphs
        if any(m.pos.find("動詞,自立") >= 0 for m in morphs) \
                or (is_last and morphs[-1].pos == "名詞,サ変接続"):  # サ変名詞の体言止めも動詞として扱う
            return "verb"
        elif any(re.search(r"形容詞|形容詞,自立|形容動詞語幹", m.pos) for m in morphs):
            return "adjective"
        elif any(re.search(r"特殊・ダ|特殊・デス|判定詞", m.cform) for m in morphs):
            return "copula"
        else:
            return "elem"

    # その文節の主辞となるような語の取得(意味役割付与に使用)
    def _get_head(self, chunk):
        ctype = chunk.ctype
        if ctype == "copula":
            main_morphs = [m for m in chunk.morphs if m.pos.find("名詞") >= 0]
            return "".join([(m.surface if m.base == "*" else m.base) for m in main_morphs]), main_morphs
        elif ctype == "verb":
            morphs = [m for m in chunk.morphs if m.base == "する"]
            if morphs:
                morph = morphs[0]
                sahen = [m for m in chunk.morphs if m.id < morph.id]
                if sahen:
                    predicate = "".join([s.surface for s in sahen[-2:]]) + "する"
                    if self.frames.is_frame(predicate):
                        return predicate, sahen[-2:] + [morph]
                    else:
                        return sahen[-1].surface + "する", sahen[-1:] + [morph]
                else:
                    return "する", [morph]
            elif any(m.pos.find("動詞,自立") >= 0 for m in chunk.morphs):
                morph = [m for m in chunk.morphs if m.pos == "動詞,自立"][0]
                morphs = [m for m in chunk.morphs if m.pos1 == "動詞" and m.id == morph.id + 1]
                if morphs:
                    predicate = morph.surface + morphs[0].base
                    main_morphs = [morph, morphs[0]]
                else:
                    premorphs = [m for m in chunk.morphs if m.id == morph.id - 1]
                    predicate = "".join([m.surface for m in premorphs]) + morph.base
                    main_morphs = [premorphs] + [morph]
                if self.frames.is_frame(predicate):
                    return predicate, main_morphs
                else:
                    return morph.base, [morph]
            elif chunk.morphs[-1].pos == "名詞,サ変接続":
                sahen = [m for m in chunk.morphs]
                predicate = "".join([s.surface for s in sahen[-2:]])
                if self.frames.is_frame(predicate):
                    return predicate, sahen[-2:]
                predicate += "する"
                if self.frames.is_frame(predicate):
                    return predicate, sahen[-2:]
                else:
                    return sahen[-1].surface, sahen[-1:]
            else:
                raise ValueError("illegal state")
        elif ctype == "adjective":
            morph = [m for m in chunk.morphs if re.search(r"形容詞|形容詞,自立|形容動詞語幹", m.pos)][0]
            if morph.pos.find("形容詞") >= 0:
                return morph.base, [morph]
            elif morph.pos.find("形容詞,自立") >= 0:
                return morph.base, [morph]
            else:
                premorphs = [m for m in chunk.morphs if m.id == morph.id - 1]
                return "".join([m.surface for m in premorphs]) + morph.base + "だ", premorphs + [morph]
        elif ctype == "elem":
            main_morphs = [m for m in chunk.morphs if re.search(r"名詞|副詞", m.pos)]
            return "".join([m.surface for m in main_morphs]), main_morphs

    # 文節内の名詞につく格助詞の取得
    # @param chunk 文節
    # @return 文節内の格助詞or係助詞
    @staticmethod
    def _get_part(chunk):
        morphs = [m for m in chunk.morphs if re.search(r"格助詞|係助詞|連体化|助動詞|副助詞|判定詞", m.pos)]
        if len(morphs) > 0:
            return morphs[-1].base
        else:
            return ""
