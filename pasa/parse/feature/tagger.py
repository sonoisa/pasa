# -*- coding: utf-8 -*-
from pasa.utils import distinct


class Tagger(object):
    def __init__(self, ccharts):
        self.ccharts = ccharts

    def parse(self, result):
        for chunk in result.chunks:
            chunk.voice = self._parse_voice(chunk)
            chunk.tense = self._parse_tense(chunk)
            chunk.polarity = self._parse_polarity(chunk)
            chunk.sentelem = self._parse_sent_elem(chunk)
            chunk.mood = self._parse_mood(chunk)
            for morph in chunk.morphs:
                morph.forms = self._parse_cchart(morph)
        return result

    # 文節態を解析し取得
    # 付与する態
    #  - ACTIVE:   能動態
    #  - CAUSATIVE:使役態
    #  - PASSIVE:  受動態
    #  - POTENTIAL:可能態
    @staticmethod
    def _parse_voice(chunk):
        if any(morph.base in {"れる", "られる"} and morph.pos.find("動詞,接尾") >= 0 for morph in chunk.morphs):
            voice = "PASSIVE"
        elif any(morph.base == "できる" and morph.pos.find("動詞,自立") >= 0 for morph in chunk.morphs):
            voice = "POTENTIAL"
        elif any((morph.base == "せる" and morph.pos.find("動詞,接尾") >= 0) or
            (morph.base in {"もらう", "いただく"} and morph.pos.find("動詞,非自立") >= 0) for morph in chunk.morphs):
            voice = "CAUSATIVE"
        elif chunk.ctype is not "elem":
            voice = "ACTIVE"
        else:
            voice = ""
        return voice

    # 時制情報の解析と付与
    # 付与する時制の情報
    #  - PAST:過去
    @staticmethod
    def _parse_tense(chunk):
        if any(morph.pos.find("助動詞") >= 0 and morph.base in {"た", "き", "けり"} for morph in chunk.morphs):
            tense = "PAST"
        else:
            tense = "PRESENT" # saitoh 2016/09/06 "" -> "PRESENT"
        return tense

    # 極性情報の解析と取得
    # 付与する極性の情報
    # AFFIRMATIVE:肯定
    # NEGATIVE:   否定
    @staticmethod
    def _parse_polarity(chunk):
        if any(morph.pos.find("助動詞") >= 0 and (morph.base in {"ない", "ぬ"} or morph.base.find("まい") >= 0) for morph in chunk.morphs):
            polarity = "NEGATIVE"
        elif chunk.ctype != "elem":
            polarity = "AFFIRMATIVE"
        else:
            polarity = ""
        return polarity

    #  形態素の活用型の情報を解析し取得"
    def _parse_cchart(self, morph):
        if morph.cform:
            cchart = self.ccharts.get_cchart(morph.cform)
            if cchart is not None:
                forms = cchart.form
            else:
                forms = []
        else:
            forms = []
        return forms

    # 文要素の情報を解析し取得
    @staticmethod
    def _parse_sent_elem(chunk):
        last = chunk.morphs[-1]
        if last.cform.find("体言接続") >= 0 or last.pos.find("連体詞") >= 0 or last.pos.find("形容詞") >= 0 or (last.pos.find("助詞,連体化") >= 0 and last.base == "の"):
            sentelem = "ADNOMINAL"
        elif last.cform.find("連用") >= 0 or last.pos.find("副詞") >= 0 or (last.base == "に" and last.pos.find("助詞,格助詞") >= 0):
            sentelem = "ADVERBIAL"
        elif chunk.modifyingchunk is None:
            sentelem = "PREDICATE"
        else:
            sentelem = ""
        return sentelem

    # 法情報を解析し取得
    @staticmethod
    def _parse_mood(chunk):
        def mapper(morph):
            if morph.cform == "仮定":
                return "SUBJUNCTIVE"
            elif morph.cform == "命令":
                return "IMPERATIVE"
            elif morph.base == "な" and morph.pos.find("助詞,終助詞") >= 0:
                return "PROHIBITIVE"
            elif morph.base == "たい" and morph.pos.find("助動詞") >= 0:
                return "PROHIBITIVE"
            elif morph.base == "？" or (morph.base == "か" and morph.pos.find("／") >= 0):
                return "INTERROGATIVE"
            else:
                return None

        morphs = [mapper(morph) for morph in chunk.morphs if morph is not None]
        morphs = distinct([m for m in morphs if m is not None])

        if morphs:
            mood = ",".join(morphs)
        elif chunk.ctype != "elem":
            mood = "INDICATIVE"
        else:
            mood = ""
        return mood
