from operator import itemgetter
from pasa.utils import *


class NounStructure(object):
    def __init__(self, nouns, frames):
        self.nouns = nouns
        self.frames = frames

    def parse(self, chunk):
        frame = self.nouns.getFrame(chunk.main)
        if frame is not None:
            nounset = list(map(
                lambda instance: self.calculateSntSimilar(instance, chunk, instance.agent[0] if instance.agent else None),
                frame.instance))
            nounset = max(nounset, key=itemgetter(0))
            self.setSemantic(chunk, nounset[2])
            self.setFrame(nounset)

    def calculateSntSimilar(self, instance, chunk, agent):
        comb = self.calculateAllCombinations(instance, chunk)
        insts = []
        while any(m[0] > 0 for m in comb):
            x = max(comb, key=itemgetter(0))
            insts.append(x)
            comb = list(filter(lambda arg: not (arg[1] == x[1] or arg[2] == x[2]), comb))

        similar = reduce(lambda s, i: s + i[0], insts, 0)
        return similar, insts, agent


    def calculateAllCombinations(self, instance, chunk):
        chunks = [x for x in chunk.modifiedchunks]
        if chunk.modifyingchunk is not None:
            chunks.append(chunk.modifyingchunk)

        combinations = flatten(list(map(lambda c: list(map(
            lambda icase: (self.calculateArgSimilar(icase, c), icase, c),
            instance.cases)),
        chunks)))

        return combinations

    def calculateArgSimilar(self, icase, chunk):
        partsimilar = self.getPartSimilar(icase, chunk)
        surfsimilar = 0.0
        nounsimilar = 0.0
        similar = partsimilar + surfsimilar + nounsimilar
        return similar

    def getPartSimilar(self, icase, chunk):
        part = icase.part
        if part == "だ" and chunk.ctype == "copula":
            return 1.0
        elif part == "だ" and chunk.part in ["は", "が"]:
            return 1.0
        elif part == chunk.part:
            return 1.0
        else:
            return 0.0

    def setSemantic(self, chunk, agent):
        if agent is not None:
            chunk.noun_agentiveL = agent.agentive
            chunk.noun_semantic = agent.semantic
        else:
            chunk.noun_semantic = "Null/Null/Null"

    def setFrame(self, nounset):
        similar, insts, agent = nounset
        for pair in insts:
            argsimilar, icase, chunk = pair
            chunk.noun_semrole = icase.semrole
            chunk.noun_arg = icase.arg
            if agent is not None:
                if icase.arg == "ARG0":
                    chunk.noun_agentiveRole = agent.arg0
                elif icase.arg == "ARG1":
                    chunk.noun_agentiveRole = agent.arg1
                elif icase.arg == "ARG2":
                    chunk.noun_agentiveRole = agent.arg2
