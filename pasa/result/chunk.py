# -*- coding: utf-8 -*-


class Chunk(object):
    def __init__(self, id, link, head, fanc, score):
        # 必須な基本情報
        self.id = id #文節のid
        self.surface = "" #文節の表層
        self.morphs = [] #文節内の形態素
        self.modifyingchunk = None #係りの文節
        self.modifiedchunks = [] #受けの文節

        # あんまりいらない情報(?)
        self.link = link #係り先
        self.head = head #主要語
        self.fanc = fanc #機能語
        self.score = score #係り関係のスコア
        # 整理により付与する情報
        self.main = ""
        self.ctype = ""
        self.verb = ""
        self.part = "" #名詞につく格の情報

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

    def __repr__(self):
        if self.modifiedchunks:
            frame = [(str(modchunk.id) + "-" + "|".join(modchunk.semrole) + "-" + "|".join(modchunk.arg) if modchunk.semrole else str(modchunk.id) + "-" + modchunk.ctype) for modchunk in self.modifiedchunks]
        else:
            frame = []

        noun_agentiveRole = [
            str(modchunk.id) + "-" + modchunk.noun_arg + "-" + modchunk.noun_agentiveRole if modchunk.noun_agentiveRole else str(modchunk.id) + "-" + modchunk.noun_arg
            for modchunk in self.modifiedchunks if modchunk.noun_arg
        ]

        return str({
            "id": self.id,
            "surface": self.surface,
            "morphs": self.morphs,
            "link": self.link,
            "head": self.head,
            "fanc": self.fanc,
            "main": self.main,
            "ctype": self.ctype,
            "verb": self.verb,
            "part": self.part,
            "tense": self.tense,
            "voice": self.voice,
            "polarity": self.polarity,
            "sentelem": self.sentelem,
            "semantic": self.semantic,
            "semrole": self.semrole,
            "arg": self.arg,
            "category": self.category,
            "adjunct": self.adjunct,
            "similar": self.similar,
            "another_parts": self.another_parts,
            "idiom": self.idiom,
            "phrase": self.phrase,
            "idiom_morph": self.idiom_morph,
            "idiom_score": self.idiom_score,
            "frame": frame,
            "noun_agentiveL": self.noun_agentiveL,
            "noun_semantic": self.noun_semantic,
            "noun_semrole": self.noun_semrole,
            "noun_arg": self.noun_arg,
            "noun_agentiveRole": noun_agentiveRole
        })

    def addMorph(self, morph):
        self.morphs.append(morph)
