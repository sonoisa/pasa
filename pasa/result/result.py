# -*- coding: utf-8 -*-


class Result(object):
    def __init__(self, line = None):
        self.chunks = []
        self.surface = line

    def __repr__(self):
        return str({
            "surface": self.surface,
            "chunks": self.chunks
        })

    def add_chunk(self, chunk):
        self.chunks.append(chunk)
