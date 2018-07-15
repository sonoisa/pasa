# -*- coding: utf-8 -*-

import CaboCha
from pasa.result import Chunk, Morph, Result


class Analyzer(object):
    def __init__(self):
        self.analyzer = CaboCha.Parser()

    def parse(self, line):
        result = Result(line)
        tree = self.analyzer.parse(line)
        for i in range(tree.chunk_size()):
            chunk = tree.chunk(i)
            cid = i
            clink = chunk.link
            chead = chunk.head_pos
            cfanc = chunk.func_pos
            cscore = chunk.score
            cchunk = Chunk(cid, clink, chead, cfanc, cscore)
            m_id = 0
            for j in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
                token = tree.token(j)
                surface = token.surface
                feature_list = token.feature_list
                pos = feature_list(0)
                pos1 = feature_list(1)
                pos2 = feature_list(2)
                pos3 = feature_list(3)
                cform = feature_list(4)
                ctype = feature_list(5)
                base = feature_list(6)
                read = feature_list(7) if token.feature_list_size >= 8 else surface
                ne = token.ne
                morph = Morph(m_id, surface, pos, pos1, pos2, pos3, cform, ctype, base, read, ne)
                cchunk.add_morph(morph)
                m_id += 1
            result.addChunk(cchunk)
        return result
