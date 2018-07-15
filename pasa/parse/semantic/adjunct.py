# -*- coding: utf-8 -*-

# 追加詞を付与するためのクラス

class Adjunct(object):
    def parse(self, modifiedlinks):
        for modchunk in modifiedlinks:
            modchunk.adjunct = self.getAdjunct(modchunk)
            if modchunk.adjunct and (not modchunk.semrole or modchunk.similar <= 2.0):
                modchunk.semrole = [modchunk.adjunct]

    def getAdjunct(self, chunk):
        adjunct = ""
        if not adjunct: adjunct = self.parseTime(chunk)
        if not adjunct: adjunct = self.parseLocation(chunk)
        if not adjunct: adjunct = self.parseScene(chunk)
        if not adjunct: adjunct = self.parseInstrument(chunk)
        if not adjunct: adjunct = self.parseReason(chunk)
        if not adjunct: adjunct = self.parseLimit(chunk)
        if not adjunct: adjunct = self.parsePremise(chunk) # 未定義
        if not adjunct: adjunct = self.parsePurpose(chunk)
        if not adjunct: adjunct = self.parseModificand(chunk) # 未定義
        if not adjunct: adjunct = self.parseManner(chunk) # 未定義
        return adjunct

    def parseTime(self, chunk):
        if not chunk.category:
            return ""

        category = chunk.category[0]
        morphs = chunk.morphs
        if category.name == "時間":
            if any(m.surface.find("間") >= 0 for m in morphs):
                return "場所（時）（間）" # "Time-Line"
            else:
                return "場所（時）（点）" # "Time-point"
        elif category.name == "動作":
            if any(m.surface.find("間") >= 0 for m in morphs):
                return "場所（時）（間）" # "Time-Line"
            elif any(m.base in ["前", "後", "まで", "から"] for m in morphs):
                return "場所（時）（点）" # "Time-point"
            else:
                return ""
        else:
            return ""

    def parseLocation(self, chunk):
        if chunk.contains_category("場所"):
            return "場所" # "Location"
        else:
            return ""

    def parseScene(self, chunk):
        if chunk.contains_category("動作"):
            if any(m.surface in ["に", "で"] for m in chunk.morphs):
                return "場所（抽出）" # "Scene"
            else:
                return ""
        else:
            return ""

    def parseInstrument(self, chunk):
        if chunk.contains_category("モノ"):
            if any(m.surface == "で" for m in chunk.morphs):
                return "手段" # "Instrument"
            else:
                return ""
        else:
            return ""

    def parseReason(self, chunk):
        if any(m.surface in ["ので", "で"] for m in chunk.morphs):
            return "原因" # "Reason"
        else:
            return ""

    def parseLimit(self, chunk):
        if chunk.contains_category("数値"):
            if any(m.surface == "で" for m in chunk.morphs):
                return "限界" # "Limit"
            else:
                return ""
        else:
            return ""

    def parsePurpose(self, chunk):
        if any(m.surface == "ため" for m in chunk.morphs):
            for modchunk in chunk.modifiedchunks:
                if any(m.surface == "の" for m in modchunk.morphs):
                    modchunk.semrole = ["目的"]  # "Purpose"
                return "目的" # "Purpose"
        else:
            return ""

    def parseAs(self, chunk):
        morphs = chunk.morphs
        if any(m.surface.find("として") >= 0 for m in morphs):
            return "As"
        else:
            return ""

    def parseAround(self, chunk):
        if chunk.surface == "ことを":
            for c in chunk.modifiedchunks:
                if c.morphs[-1].surface == "の":
                    c.semrole = ["Around"]
                    return "Around"
        elif any(m.surface == "について" for m in chunk.morphs):
            return "Around"
        else:
            return ""

    def parsePremise(self, chunk):
        premise = ""
        return premise

    def parseCitation(self, chunk):
        morphs = chunk.morphs
        if any(m.surface.find("引用") >= 0 for m in morphs):
            return "Citation"
        else:
            return ""

    def parseModificand(self, chunk):
        modify = ""
        return modify

    def parseManner(self, chunk):
        manner = ""
        return manner
