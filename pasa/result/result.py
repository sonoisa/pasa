# -*- coding: utf-8 -*-


class Result(object):
    def __init__(self, line = None):
        self.chunks = []
        self.surface = line

    def add_chunk(self, chunk):
        self.chunks.append(chunk)

    def to_dict(self):
        return {
            "surface": self.surface,
            "chunks": [c.to_dict() for c in self.chunks]
        }

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return str(self.to_dict())
