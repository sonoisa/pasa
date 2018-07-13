# -*- coding: utf-8 -*-


class Morph(object):
    def __init__(self, m_id, surface, pos1, pos2, pos3, pos4, cform, ctype, base, read, ne):
        self.id = m_id # 形態素のid
        self.surface = surface # 形態素の表層
        self.pos1 = ""
        self.pos2 = ""
        self.pos3 = ""
        self.pos4 = ""
        self.base = base # 基本形
        self.read = read # 読み
        self.cform = "" # 活用形
        self.ctype = "" # 活用型
        self.ne = "" # 固有表現解析
        self.tree = []
        self.chunk = None
        self.forms = []

        pos = ""
        if pos1 is not "*":
            self.pos1 = pos1
            pos += pos1
        if pos2 is not "*":
            self.pos2 = pos2
            pos += "," + pos2
        if pos3 is not "*":
            self.pos3 = pos3
            pos += "," + pos3
        if pos4 is not "*":
            self.pos4 = pos4
            pos += "," + pos4
        if ctype is not "*":
            self.cform = ctype
        if cform is not "*":
            self.ctype = cform
        self.pos = pos # 品詞，品詞細分類1，品詞細分類2，品詞細分類3
        if ne is not None:
            self.ne = ne

    def __str__(self):
        return str({
            "id": self.id,
            "surface": self.surface,
            "pos": self.pos,
            "pos1": self.pos1,
            "pos2": self.pos2,
            "pos3": self.pos3,
            "pos4": self.pos4,
            "cform": self.cform,
            "ctype": self.ctype,
            "base": self.base,
            "read": self.read,
            "ne": self.ne
        })

    def __repr__(self):
        return str(self)