# -*- coding: utf-8 -*-

from cabocha.analyzer import CaboChaAnalyzer
from pasa.result import Chunk, Morph, Result


class Analyzer(object):
    def __init__(self):
        self.analyzer = CaboChaAnalyzer()

    def parse(self, line):
        result = Result(line)
        for chunk in self.analyzer.parse(line):
            cid = chunk.id
            clink = chunk.next_link_id
            chead = chunk.head_pos
            cfanc = chunk.func_pos
            cscore = chunk.score
            cchunk = Chunk(cid, clink, chead, cfanc, cscore)
            m_id = 0
            for token in chunk:
                surface = token.surface
                pos = token.pos
                pos1 = token.pos1
                pos2 = token.pos2
                pos3 = token.pos3
                cform = token.cform
                ctype = token.ctype
                base = token.genkei
                read = token.yomi
                ne = token.ne
                morph = Morph(m_id, surface, pos, pos1, pos2, pos3, cform, ctype, base, read, ne)
                cchunk.addMorph(morph)
                m_id += 1
            result.addChunk(cchunk)
        return result
