# -*- coding: utf-8 -*-


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
            chunk.main = self._get_head(chunk)
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
        if any(m.pos.find("動詞,自立") >= 0 for m in morphs) or (is_last and morphs[-1].pos == "名詞,サ変接続"): # サ変名詞の体言止めも動詞として扱う
            return "verb"
        elif any(m.pos.find("形容詞") >= 0 or m.pos.find("形容詞,自立") >= 0 or m.pos.find("形容動詞語幹") >= 0 for m in morphs):
            return "adjective"
        elif any(m.cform.find("特殊・ダ") >= 0 or m.cform.find("特殊・デス") >= 0 or m.cform.find("判定詞") >= 0 for m in morphs):
            return "copula"
        else:
            return "elem"

    # その文節の主辞となるような語の取得(意味役割付与に使用)
    def _get_head(self, chunk):
        ctype = chunk.ctype
        if ctype == "copula":
            return "".join([(m.surface if m.base == "*" else m.base) for m in chunk.morphs if m.pos.find("名詞") >= 0])
        elif ctype == "verb":
            morphs = [m for m in chunk.morphs if m.base == "する"]
            if morphs:
                morph = morphs[0]
                sahen = [m.surface for m in chunk.morphs if m.id < morph.id]
                if sahen:
                    predicate = "".join(sahen[-2:]) + "する"
                    if self.frames.is_frame(predicate):
                        return predicate
                    else:
                        return sahen[-1] + "する"
                else:
                    return "する"
            elif any(m.pos.find("動詞,自立") >= 0 for m in chunk.morphs):
                morph = [m for m in chunk.morphs if m.pos == "動詞,自立"][0]
                morphs = [m for m in chunk.morphs if m.pos1 == "動詞" and m.id == morph.id + 1]
                if morphs:
                    predicate = morph.surface + morphs[0].base
                else:
                    predicate = "".join([m.surface for m in chunk.morphs if m.id == morph.id - 1]) + morph.base
                if self.frames.is_frame(predicate):
                    return predicate
                else:
                    return morph.base
            elif chunk.morphs[-1].pos == "名詞,サ変接続":
                sahen = [m.surface for m in chunk.morphs]
                predicate = "".join(sahen[-2:])
                if self.frames.is_frame(predicate):
                    return predicate
                predicate += "する"
                if self.frames.is_frame(predicate):
                    return predicate
                else:
                    return sahen[-1]
            else:
                raise ValueError("illegal state")
        elif ctype == "adjective":
            morph = [m for m in chunk.morphs if m.pos.find("形容詞") >= 0 or m.pos.find("形容詞,自立") >= 0 or m.pos.find("形容動詞語幹") >= 0][0]
            if morph.pos.find("形容詞") >= 0:
                return morph.base
            elif morph.pos.find("形容詞,自立") >= 0:
                return morph.base
            else:
                return "".join([m.surface for m in chunk.morphs if m.id == morph.id - 1]) + morph.base + "だ"
        elif ctype == "elem":
            return "".join([m.surface for m in chunk.morphs if m.pos.find("名詞") >= 0 or m.pos.find("副詞") >= 0])

    # 文節内の名詞につく格助詞の取得
    # @param chunk 文節
    # @return 文節内の格助詞or係助詞
    @staticmethod
    def _get_part(chunk):
        morphs = [m for m in chunk.morphs if m.pos.find("格助詞") >= 0 or m.pos.find("係助詞") >= 0 or m.pos2.find("連体化") >= 0 or m.pos.find("助動詞") >= 0 or m.pos.find("副助詞") >= 0 or m.pos.find("判定詞") >= 0]
        if len(morphs) > 0:
            return morphs[-1].base
        else:
            return ""
