# -*- coding: utf-8 -*-


class Basic(object):
    def __init__(self, frames):
        self.frames = frames

    def parse(self, result):
        for chunk in result.chunks:
            chunk.surface = self.getChunkSurface(chunk)
            chunk.modifyingchunk = self.getModifyingChunk(result, chunk)
            chunk.modifiedchunks = self.getModifiedChunks(result, chunk)
            chunk.ctype = self.getChunkType(chunk)
            chunk.main = self.getHead(chunk)
            chunk.part = self.getPart(chunk)
            for morph in chunk.morphs:
                morph.chunk = chunk
        return result

    # 文節内の形態素の表層をつなげて，文節の表層を取得
    # @param chunk 文節
    # @return 文節の表層
    def getChunkSurface(self, chunk):
        surface = "".join(map(lambda m: m.surface, chunk.morphs))
        return surface

    # 係っている文節を取得
    def getModifyingChunk(self, result, chunk):
        modifyingchunk = None if chunk.link == -1 else result.chunks[chunk.link]
        return modifyingchunk

    # 文節の係りを受けている文節を取得
    # @param chunk 文節
    # @return 係り元の文節集合
    def getModifiedChunks(self, result, depchunk):
        linkchunks = list(filter(lambda chunk: chunk.link == depchunk.id, result.chunks))
        return linkchunks

    # 文節のタイプを取得
    #  - verb:      動詞
    #  - adjective: 形容詞，形容動詞
    #  - copula:    コピュラ(AはBだ)
    #  - elem:      その他
    def getChunkType(self, chunk):
        morphs = chunk.morphs
        if any(m.pos.find("動詞,自立") >= 0 for m in morphs):
            return "verb"
        elif any(m.pos.find("形容詞") >= 0 or m.pos.find("形容詞,自立") >= 0 or m.pos.find("形容動詞語幹") >= 0 for m in morphs):
            return "adjective"
        elif any(m.cform.find("特殊・ダ") >= 0 or m.cform.find("特殊・デス") >= 0 or m.cform.find("判定詞") >= 0 for m in morphs):
            return "copula"
        else:
            return "elem"

    # その文節の主辞となるような語の取得(意味役割付与に使用)
    def getHead(self, chunk):
        ctype = chunk.ctype
        if ctype == "copula":
            return "".join(
                map(lambda m: m.surface if m.base == "*" else m.base,
                    filter(lambda m: m.pos.find("名詞") >= 0, chunk.morphs)))
        elif ctype == "verb":
            morphs = list(filter(lambda m: m.base == "する", chunk.morphs))
            if morphs:
                morph = morphs[0]
                sahen = list(map(lambda m: m.surface, filter(lambda m: m.id < morph.id, chunk.morphs)))
                if sahen:
                    predicate = "".join(sahen[len(sahen) - 2:len(sahen)]) + "する"
                    if self.frames.isFrame(predicate):
                        return predicate
                    else:
                        return sahen[-1] + "する"
                else:
                    return "する"
            else:
                morph = list(filter(lambda m: m.pos == "動詞,自立", chunk.morphs))[0]
                morphs = list(filter(lambda m: m.pos1 == "動詞" and m.id == morph.id + 1, chunk.morphs))
                if morphs:
                    predicate = morph.surface + morphs[0].base
                else:
                    predicate = "".join(
                        map(lambda m: m.surface,
                            filter(lambda m: m.id == morph.id - 1, chunk.morphs))
                    ) + morph.base
                if self.frames.isFrame(predicate):
                    return predicate
                else:
                    return morph.base
        elif ctype == "adjective":
            morph = list(filter(lambda m: m.pos.find("形容詞") >= 0 or m.pos.find("形容詞,自立") >= 0 or m.pos.find("形容動詞語幹") >= 0, chunk.morphs))[0]
            if morph.pos.find("形容詞") >= 0:
                return morph.base
            elif morph.pos.find("形容詞,自立") >= 0:
                return morph.base
            else:
                return "".join(map(lambda m: m.surface, filter(lambda m: m.id == morph.id - 1, chunk.morphs))) + morph.base + "だ"
        elif ctype == "elem":
            return "".join(
                map(lambda m: m.surface,
                    filter(lambda m: m.pos.find("名詞") >= 0 or m.pos.find("副詞") >= 0, chunk.morphs)))

    # 文節内の名詞につく格助詞の取得
    # @param chunk 文節
    # @return 文節内の格助詞or係助詞
    def getPart(self, chunk):
        morphs = list(filter(lambda m: m.pos.find("格助詞") >= 0 or m.pos.find("係助詞") >= 0 or m.pos2.find("連体化") >= 0 or m.pos.find("助動詞") >= 0 or m.pos.find("副助詞") >= 0 or m.pos.find("判定詞") >= 0, chunk.morphs))
        if len(morphs) > 0:
            return morphs[-1].base
        else:
            return ""
