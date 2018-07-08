# -*- coding: utf-8 -*-
from pasa.utils import distinct


class Tagger(object):
    def __init__(self, ccharts, categories):
        self.ccharts = ccharts
        self.categorys = categories

    def parse(self, result):
        for chunk in result.chunks:
            chunk.voice = self.parseVoice(chunk)
            chunk.tense = self.parseTense(chunk)
            chunk.polarity = self.parsePolarity(chunk)
            chunk.sentelem = self.parseSentElem(chunk)
            chunk.mood = self.parseMood(chunk)
            chunk.category = self.parseCategory(chunk)
            for morph in chunk.morphs:
                morph.forms = self.parseCchart(morph)
        return result

    # 文節中に名詞カテゴリが付与できるものがあればカテゴリの種類を返す
    # @param morphs 文節中の形態素の配列
    # @return カテゴリ
    def parseCategory(self, linkchunk):
        category = self.categorys.getCates(linkchunk.main)
        for morph in linkchunk.morphs:
            pos = morph.pos
            if pos in ["名詞,接尾,助数詞", "名詞,数"]:
                if morph.surface in ["年", "月", "日", "時", "分", "秒"]:
                    category.append("時間")
                else:
                    category.append("数値")
            elif pos in ["名詞,固有名詞,人名", "名詞,接尾,人名"]:
                category.append("人")
            elif pos in ["名詞,固有名詞,地域", "名詞,接尾,地域"]:
                category.append("場所")
            elif pos == "名詞,固有名詞,組織":
                category.append("組織")
        return distinct(category)

    # 文節態を解析し取得
    # 付与する態
    #  - ACTIVE:   能動態
    #  - CAUSATIVE:使役態
    #  - PASSIVE:  受動態
    #  - POTENTIAL:可能態
    def parseVoice(self, chunk):
        if any(morph.base in ["れる", "られる"] and morph.pos.find("動詞,接尾") >= 0 for morph in chunk.morphs):
            voice = "PASSIVE"
        elif any(morph.base == "できる" and morph.pos.find("動詞,自立") >= 0 for morph in chunk.morphs):
            voice = "POTENTIAL"
        elif any((morph.base == "せる" and morph.pos.find("動詞,接尾") >= 0) or
            (morph.base in ["もらう", "いただく"] and morph.pos.find("動詞,非自立") >= 0) for morph in chunk.morphs):
            voice = "CAUSATIVE"
        elif chunk.ctype is not "elem":
            voice = "ACTIVE"
        else:
            voice = ""
        return voice

    # 時制情報の解析と付与
    # 付与する時制の情報
    #  - PAST:過去
    def parseTense(self, chunk):
        if any(morph.pos.find("助動詞") >= 0 and morph.base in ["た", "き", "けり"] for morph in chunk.morphs):
            tense = "PAST"
        else:
            tense = "PRESENT" # saitoh 2016/09/06 "" -> "PRESENT"
        return tense

    # 極性情報の解析と取得
    # 付与する極性の情報
    # AFFIRMATIVE:肯定
    # NEGATIVE:   否定
    def parsePolarity(self, chunk):
        if any(morph.pos.find("助動詞") >= 0 and (morph.base in ["ない", "ぬ"] or morph.base.find("まい") >= 0) for morph in chunk.morphs):
            polarity = "NEGATIVE"
        elif chunk.ctype != "elem":
            polarity = "AFFIRMATIVE"
        else:
            polarity = ""
        return polarity

    #  形態素の活用型の情報を解析し取得"
    def parseCchart(self, morph):
        if morph.cform:
            cchart = self.ccharts.getCchart(morph.cform)
            if cchart is not None:
                forms = cchart.form
            else:
                forms = []
        else:
            forms = []
        return forms

    # 文要素の情報を解析し取得
    def parseSentElem(self, chunk):
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
    def parseMood(self, chunk):
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

        morphs = list(filter(lambda morph: morph is not None, map(mapper, chunk.morphs)))
        seen = set()
        morphs = [m for m in morphs if m not in seen and not seen.add(m)]

        if morphs:
            mood = ",".join(morphs)
        elif chunk.ctype != "elem":
            mood = "INDICATIVE"
        else:
            mood = ""
        return mood
