from operator import itemgetter
from pasa.utils import *


class NounStructure(object):
    def __init__(self, nouns, frames):
        self.nouns = nouns
        self.frames = frames

    def parse(self, chunk):
        frame = self.nouns.get_frame(chunk.main)
        if frame is not None:
            nounset = list(map(
                lambda instance: self._calculate_snt_similar(instance, chunk, instance.agent[0] if instance.agent else None),
                frame.instance))
            nounset = max(nounset, key=itemgetter(0))
            self._set_semantic(chunk, nounset[2])
            self._set_frame(nounset)

    def _calculate_snt_similar(self, instance, chunk, agent):
        comb = self._calculate_all_combinations(instance, chunk)
        insts = []
        while any(m[0] > 0 for m in comb):
            x = max(comb, key=itemgetter(0))
            insts.append(x)
            comb = list(filter(lambda arg: not (arg[1] == x[1] or arg[2] == x[2]), comb))

        similar = reduce(lambda s, i: s + i[0], insts, 0)
        return similar, insts, agent


    def _calculate_all_combinations(self, instance, chunk):
        chunks = [x for x in chunk.modifiedchunks]
        if chunk.modifyingchunk is not None:
            chunks.append(chunk.modifyingchunk)

        combinations = flatten(list(map(lambda c: list(map(
            lambda icase: (self._calculate_arg_similar(icase, c), icase, c),
            instance.cases)),
        chunks)))

        return combinations

    def _calculate_arg_similar(self, icase, chunk):
        partsimilar = self._get_part_similar(icase, chunk)
        surfsimilar = 0.0
        nounsimilar = 0.0
        similar = partsimilar + surfsimilar + nounsimilar
        return similar

    @staticmethod
    def _get_part_similar(icase, chunk):
        part = icase.part
        if part == "だ" and chunk.ctype == "copula":
            return 1.0
        elif part == "だ" and chunk.part in ["は", "が"]:
            return 1.0
        elif part == chunk.part:
            return 1.0
        else:
            return 0.0

    @staticmethod
    def _set_semantic(chunk, agent):
        if agent is not None:
            chunk.noun_agentiveL = agent.agentive
            chunk.noun_semantic = agent.semantic
        else:
            chunk.noun_semantic = "Null/Null/Null"

    @staticmethod
    def _set_frame(nounset):
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
