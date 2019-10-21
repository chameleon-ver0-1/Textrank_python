# -*- coding: utf-8 -*-

import networkx
import re
import math


def similarity(a, b):
    n = len(a.intersection(b))
    return n / float(len(a) + len(b) - n) / (math.log(len(a) + 1) * math.log(len(b) + 1))


class TextRank:
    def __init__(self, **kargs):
        self.graph = None
        self.window = kargs.get('window', 5)
        self.coef = kargs.get('coef', 1.0)
        self.threshold = kargs.get('threshold', 0.005)
        self.dictCount = {}
        self.dictBiCount = {}
        self.dictNear = {}
        self.nTotal = 0

    def load(self, sentenceIter, wordFilter=None):
        def insert_pair(a, b):
            if a > b:
                a, b = b, a
            elif a == b:
                return

            self.dictBiCount[a, b] = self.dictBiCount.get((a, b), 0) + 1

        def insert_near_pair(a, b):
            self.dictNear[a, b] = self.dictNear.get((a, b), 0) + 1

        for sent in sentenceIter:
            for i, word in enumerate(sent):
                if wordFilter and not wordFilter(word):
                    continue

                self.dictCount[word] = self.dictCount.get(word, 0) + 1
                self.nTotal += 1

                if i - 1 >= 0 and (not wordFilter or wordFilter(sent[i - 1])):
                    insert_near_pair(sent[i - 1], word)
                if i + 1 < len(sent) and (not wordFilter or wordFilter(sent[i + 1])):
                    insert_near_pair(word, sent[i + 1])

                for j in range(i + 1, min(i + self.window + 1, len(sent))):
                    if wordFilter and not wordFilter(sent[j]):
                        continue
                    if sent[j] != word:
                        insert_pair(word, sent[j])

    def load_sentences(self, sentenceIter, tokenizer=None):

        rgx_splitter = ''
        sentence_set = []

        if not tokenizer:
            rgx_splitter = re.compile('[\\s.,:;-?!()"\']+')

        for sent in filter(None, sentenceIter):
            if type(sent) == str:
                if tokenizer:
                    s = set(filter(None, tokenizer(sent)))
                else:
                    s = set(filter(None, rgx_splitter.split(sent)))

            else:
                s = set(sent)

            if len(s) < 2:
                continue

            self.dictCount[len(self.dictCount)] = sent
            sentence_set.append(s)

        for i in range(len(self.dictCount)):
            for j in range(i + 1, len(self.dictCount)):

                s = similarity(sentence_set[i], sentence_set[j])

                if s < self.threshold:
                    continue

                self.dictBiCount[i, j] = s

    def get_pmi(self, a, b):
        co = self.dictNear.get((a, b), 0)

        if not co:
            return None

        return math.log(float(co) * self.nTotal / self.dictCount[a] / self.dictCount[b])

    def get_i(self, a):
        if a not in self.dictCount:
            return None

        return math.log(self.nTotal / self.dictCount[a])

    def build(self):
        self.graph = networkx.Graph()
        self.graph.add_nodes_from(self.dictCount.keys())

        for (a, b), n in self.dictBiCount.items():
            self.graph.add_edge(a, b, weight=n * self.coef + (1 - self.coef))

    def rank(self):
        return networkx.pagerank(self.graph, weight='weight')

    def extract(self, ratio=0.1):
        ranks = self.rank()
        cand = sorted(ranks, key=ranks.get, reverse=True)[:int(len(ranks) * ratio)]
        pairness = {}
        start_of = {}
        tuples = {}
        for k in cand:
            tuples[(k,)] = self.get_i(k) * ranks[k]

            for l in cand:
                if k == l:
                    continue

                pmi = self.get_pmi(k, l)

                if pmi:
                    pairness[k, l] = pmi

        for (k, l) in sorted(pairness, key=pairness.get, reverse=True):
            print(k[0], l[0], pairness[k, l])
            if k not in start_of:
                start_of[k] = (k, l)

        for (k, l), v in pairness.items():
            pmi_s = v
            rs = ranks[k] * ranks[l]
            path = (k, l)
            tuples[path] = pmi_s / (len(path) - 1) * rs ** (1 / len(path)) * len(path)
            last = l

            while last in start_of and len(path) < 7:
                if last in path:
                    break

                pmi_s += pairness[start_of[last]]
                last = start_of[last][1]
                rs *= ranks[last]
                path += (last,)
                tuples[path] = pmi_s / (len(path) - 1) * rs ** (1 / len(path)) * len(path)

        used = set()
        both = {}

        for k in sorted(tuples, key=tuples.get, reverse=True):
            if used.intersection(set(k)):
                continue

            both[k] = tuples[k]

            for w in k:
                used.add(w)

        # for k in cand:
        #    if k not in used or True: both[k] = ranks[k] * self.getI(k)

        return both

    def summarize(self, ratio=0.333):
        r = self.rank()
        ks = sorted(r, key=r.get, reverse=True)[:int(len(r) * ratio)]
        return ' '.join(map(lambda k: self.dictCount[k], sorted(ks)))
