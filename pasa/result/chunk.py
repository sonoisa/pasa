# -*- coding: utf-8 -*-


class Chunk(object):
    def __init__(self, cid, link, head, fanc, score):
        # 必須な基本情報
        self.id = cid    # 文節のid
        self.surface = ""   # 文節の表層
        self.morphs = []   # 文節内の形態素
        self.modifyingchunk = None  # 係りの文節
        self.modifiedchunks = []    # 受けの文節

        # あんまりいらない情報(?)
        self.link = link    # 係り先
        self.head = head    # 主要語
        self.fanc = fanc    # 機能語
        self.score = score  # 係り関係のスコア
        # 整理により付与する情報
        self.main = ""
        self.ctype = ""
        self.verb = ""
        self.part = ""  # 名詞につく格の情報

        # 態などの情報
        self.tense = ""
        self.voice = ""
        self.polarity = ""
        self.sentelem = ""
        self.mood = ""

        # 語義や意味役割に必要な変数
        self.semantic = ""
        self.semrole = []
        self.arg = []
        self.category = []
        self.adjunct = ""
        self.similar = 0.0
        self.another_parts = []

        self.idiom = ""
        self.phrase = []
        self.idiom_morph = []
        self.idiom_score = 0.0

        self.noun_agentiveL = ""
        self.noun_semantic = ""
        self.noun_semrole = ""
        self.noun_arg = ""
        self.noun_agentiveRole = ""

    def to_dict(self):
        if self.modifiedchunks:
            frame = [(str(modchunk.id) + "-" + "|".join(modchunk.semrole) + "-" + "|".join(modchunk.arg) if modchunk.semrole else str(modchunk.id) + "-" + modchunk.ctype) for modchunk in self.modifiedchunks]
        else:
            frame = []

        noun_agentive_role = [
            str(modchunk.id) + "-" + modchunk.noun_arg + "-" + modchunk.noun_agentiveRole if modchunk.noun_agentiveRole else str(modchunk.id) + "-" + modchunk.noun_arg
            for modchunk in self.modifiedchunks if modchunk.noun_arg
        ]

        d = {
            "id": self.id,
            "link": self.link,
            "head": self.head,
            "fanc": self.fanc
        }

        if self.surface: d["surface"] = self.surface
        if [m.to_dict() for m in self.morphs]: d["morphs"] = [m.to_dict() for m in self.morphs]
        if self.main: d["main"] = self.main
        if self.ctype: d["ctype"] = self.ctype
        if self.verb: d["verb"] = self.verb
        if self.part: d["part"] = self.part
        if self.tense: d["tense"] = self.tense
        if self.voice: d["voice"] = self.voice
        if self.polarity: d["polarity"] = self.polarity
        if self.sentelem: d["sentelem"] = self.sentelem
        if self.semantic: d["semantic"] = self.semantic
        if self.semrole: d["semrole"] = self.semrole
        if self.arg: d["arg"] = self.arg
        if [c.to_dict() for c in self.category]: d["category"] = [c.to_dict() for c in self.category]
        if self.adjunct: d["adjunct"] = self.adjunct
        if self.similar > 0.0: d["similar"] = self.similar
        if self.another_parts: d["another_parts"] = self.another_parts
        if self.idiom: d["idiom"] = self.idiom
        if self.phrase: d["phrase"] = self.phrase
        if [m.to_dict() for m in self.idiom_morph]: d["idiom_morph"] = [m.to_dict() for m in self.idiom_morph]
        if self.idiom_score > 0.0: d["idiom_score"] = self.idiom_score
        if frame: d["frame"] = frame
        if self.noun_agentiveL: d["noun_agentiveL"] = self.noun_agentiveL
        if self.noun_semantic: d["noun_semantic"] = self.noun_semantic
        if self.noun_semrole: d["noun_semrole"] = self.noun_semrole
        if self.noun_arg: d["noun_arg"] = self.noun_arg
        if noun_agentive_role: d["noun_agentiveRole"] = noun_agentive_role

        return d

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return str(self.to_dict())

    def add_morph(self, morph):
        self.morphs.append(morph)

    def contains_category(self, category_name):
        """与えられたカテゴリ名を持つカテゴリがあるかどうかを返す。"""
        return any(category_name == c.name for c in self.category)

    def get_category(self, category_name):
        """与えられたカテゴリ名を持つカテゴリオブジェクトを返す。"""
        for c in self.category:
            if category_name == c.name:
                return c
        return None
