# -*- coding: utf-8 -*-

# 追加詞を付与するためのクラス

class Adjunct(object):
    def parse(self, modifiedlinks):
        for modchunk in modifiedlinks:
            modchunk.adjunct = self._get_adjunct(modchunk)
            if modchunk.adjunct and (not modchunk.semrole or modchunk.similar <= 2.0):
                modchunk.semrole = [modchunk.adjunct]

    def _get_adjunct(self, chunk):
        adjunct = ""
        if not adjunct: adjunct = self._parse_time(chunk)
        if not adjunct: adjunct = self._parse_location(chunk)
        if not adjunct: adjunct = self._parse_scene(chunk)
        if not adjunct: adjunct = self._parse_instrument(chunk)
        if not adjunct: adjunct = self._parse_reason(chunk)
        if not adjunct: adjunct = self._parse_limit(chunk)
        if not adjunct: adjunct = self._parse_premise(chunk) # 未定義
        if not adjunct: adjunct = self._parse_purpose(chunk)
        if not adjunct: adjunct = self._parse_modificand(chunk) # 未定義
        if not adjunct: adjunct = self._parse_manner(chunk) # 未定義
        return adjunct

    @staticmethod
    def _parse_time(chunk):
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

    @staticmethod
    def _parse_location(chunk):
        if chunk.contains_category("場所"):
            return "場所" # "Location"
        else:
            return ""

    @staticmethod
    def _parse_scene(chunk):
        if chunk.contains_category("動作"):
            if any(m.surface in ["に", "で"] for m in chunk.morphs):
                return "場所（抽出）" # "Scene"
            else:
                return ""
        else:
            return ""

    @staticmethod
    def _parse_instrument(chunk):
        if chunk.contains_category("モノ"):
            if any(m.surface == "で" for m in chunk.morphs):
                return "手段" # "Instrument"
            else:
                return ""
        else:
            return ""

    @staticmethod
    def _parse_reason(chunk):
        if any(m.surface in ["ので", "で"] for m in chunk.morphs):
            return "原因" # "Reason"
        else:
            return ""

    @staticmethod
    def _parse_limit(chunk):
        if chunk.contains_category("数値"):
            if any(m.surface == "で" for m in chunk.morphs):
                return "限界" # "Limit"
            else:
                return ""
        else:
            return ""

    @staticmethod
    def _parse_purpose(chunk):
        if any(m.surface == "ため" for m in chunk.morphs):
            for modchunk in chunk.modifiedchunks:
                if any(m.surface == "の" for m in modchunk.morphs):
                    modchunk.semrole = ["目的"]  # "Purpose"
                return "目的" # "Purpose"
        else:
            return ""

    @staticmethod
    def _parse_as(chunk):
        morphs = chunk.morphs
        if any(m.surface.find("として") >= 0 for m in morphs):
            return "As"
        else:
            return ""

    @staticmethod
    def _parse_around(chunk):
        if chunk.surface == "ことを":
            for c in chunk.modifiedchunks:
                if c.morphs[-1].surface == "の":
                    c.semrole = ["Around"]
                    return "Around"
        elif any(m.surface == "について" for m in chunk.morphs):
            return "Around"
        else:
            return ""

    @staticmethod
    def _parse_premise(chunk):
        premise = ""
        return premise

    @staticmethod
    def _parse_citation(chunk):
        morphs = chunk.morphs
        if any(m.surface.find("引用") >= 0 for m in morphs):
            return "Citation"
        else:
            return ""

    @staticmethod
    def _parse_modificand(chunk):
        modify = ""
        return modify

    @staticmethod
    def _parse_manner(chunk):
        manner = ""
        return manner
